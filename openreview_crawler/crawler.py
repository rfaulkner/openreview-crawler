from typing import Generator, List, Optional, Any
from .client import OpenReviewClient
from .models import Paper, Review
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable, **kwargs):
        return iterable

class OpenReviewCrawler:
    
    def __init__(self, conference_id: str = 'ICLR.cc/2025/Conference', submission_invitation: Optional[str] = None, client: Optional[OpenReviewClient] = None):
        self.conference_id = conference_id
        self.submission_invitation = submission_invitation or f'{conference_id}/-/Submission'
        self.client = client or OpenReviewClient()

    def _get_content_value(self, content: dict, key: str, default: Any = None) -> Any:
        if key in content:
            return content[key].get('value', default)
        return default

    def _parse_paper(self, note) -> Paper:
        content = note.content
        return Paper(
            id=note.id,
            title=self._get_content_value(content, 'title', ''),
            authors=self._get_content_value(content, 'authors', []),
            abstract=self._get_content_value(content, 'abstract', ''),
            pdf_url=f"https://openreview.net/pdf?id={note.id}",
            keywords=self._get_content_value(content, 'keywords', []),
            status="Submitted"
        )

    def _parse_review(self, note) -> Review:
        content = note.content
        rating_val = self._get_content_value(content, 'rating')
        confidence_val = self._get_content_value(content, 'confidence')
        
        # Rating format might be "8: ..." or just integer in V2. 
        # Safely handle string split if it's a string, or direct int.
        rating = None
        if isinstance(rating_val, str):
            rating = int(rating_val.split(':')[0])
        elif isinstance(rating_val, (int, float)):
            rating = int(rating_val)
            
        confidence = None
        if isinstance(confidence_val, str):
            confidence = int(confidence_val.split(':')[0])
        elif isinstance(confidence_val, (int, float)):
            confidence = int(confidence_val)

        return Review(
            id=note.id,
            reviewer=note.signatures[0] if note.signatures else "Anonymous",
            rating=rating,
            confidence=confidence,
            title=self._get_content_value(content, 'title'),
            review_text=self._get_content_value(content, 'review', ''),
            strengths=self._get_content_value(content, 'strengths'),
            weaknesses=self._get_content_value(content, 'weaknesses'),
            invitation=note.invitations[0] if note.invitations else "",
            reply_to=note.replyto
        )

    def get_papers(self, limit: int = 100, offset: int = 0) -> List[Paper]:
        notes = self.client.get_submissions(self.submission_invitation)
        papers = []
        
        for note in notes[offset : offset + limit]:
            paper = self._parse_paper(note)
            try:
                self._enrich_paper(paper)
            except Exception as e:
                print(f"Error enriching paper {paper.id}: {e}")
            papers.append(paper)
        return papers

    def get_reviews(self, paper_id: str) -> List[Review]:
        notes = self.client.get_notes(forum=paper_id)
        reviews = []
        for note in notes:
            # Check if any invitation matches 'Official_Review'
            if note.invitations and any('Official_Review' in inv for inv in note.invitations): 
                reviews.append(self._parse_review(note))
        return reviews

    def _get_decision(self, notes: List[any]) -> Optional[str]:
        for note in notes:
            # Check if any invitation matches 'Decision'
            if note.invitations and any('Decision' in inv for inv in note.invitations):
                return self._get_content_value(note.content, 'decision', None)
        return None

    def _enrich_paper(self, paper: Paper):
        notes = self.client.get_notes(forum=paper.id)
        
        # Parse reviews
        reviews = []
        for note in notes:
            # Check if any invitation matches 'Official_Review'
            if note.invitations and any('Official_Review' in inv for inv in note.invitations):
                reviews.append(self._parse_review(note))
        paper.reviews = reviews
        
        # Parse decision
        paper.decision = self._get_decision(notes)
        
        # Calculate average rating
        ratings = [r.rating for r in reviews if r.rating is not None]
        if ratings:
            paper.avg_rating = sum(ratings) / len(ratings)

    def crawl(self, limit: int = 100) -> Generator[Paper, None, None]:
        """
        Crawls papers and their reviews.
        Yields Paper objects with the 'reviews', 'decision', and 'avg_rating' fields populated.
        """
        submissions = self.client.get_submissions(self.submission_invitation)
        
        for note in tqdm(submissions[:limit], desc="Crawling Papers"):
            paper = self._parse_paper(note)
            try:
                self._enrich_paper(paper)
            except Exception as e:
                print(f"Error enriching paper {paper.id}: {e}")
            yield paper
