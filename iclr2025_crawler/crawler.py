from typing import Generator, List, Optional
from .client import OpenReviewClient
from .models import Paper, Review
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable, **kwargs):
        return iterable

class ICLRCrawler:
    CONFERENCE_ID = 'ICLR.cc/2025/Conference'
    SUBMISSION_INVITATION = f'{CONFERENCE_ID}/-/Submission'
    
    def __init__(self, client: Optional[OpenReviewClient] = None):
        self.client = client or OpenReviewClient()

    def _parse_paper(self, note) -> Paper:
        content = note.content
        return Paper(
            id=note.id,
            title=content.get('title', ''),
            authors=content.get('authors', []),
            abstract=content.get('abstract', ''),
            pdf_url=f"https://openreview.net/pdf?id={note.id}",
            keywords=content.get('keywords', []),
            status="Submitted" # Default, can be updated if decision is found
        )

    def _parse_review(self, note) -> Review:
        content = note.content
        return Review(
            id=note.id,
            reviewer=note.signatures[0] if note.signatures else "Anonymous",
            rating=int(content['rating'].split(':')[0]) if 'rating' in content else None,
            confidence=int(content['confidence'].split(':')[0]) if 'confidence' in content else None,
            title=content.get('title'),
            review_text=content.get('review', ''),
            invitation=note.invitation,
            reply_to=note.replyto
        )

    def get_papers(self, limit: int = 100, offset: int = 0) -> List[Paper]:
        notes = self.client.get_submissions(self.SUBMISSION_INVITATION)
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
            if 'Official_Review' in note.invitation: 
                reviews.append(self._parse_review(note))
        return reviews

    def _get_decision(self, notes: List[any]) -> Optional[str]:
        for note in notes:
            if 'Decision' in note.invitation:
                return note.content.get('decision', None)
        return None

    def _enrich_paper(self, paper: Paper):
        notes = self.client.get_notes(forum=paper.id)
        
        # Parse reviews
        reviews = []
        for note in notes:
            if 'Official_Review' in note.invitation:
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
        submissions = self.client.get_submissions(self.SUBMISSION_INVITATION)
        
        for note in tqdm(submissions[:limit], desc="Crawling Papers"):
            paper = self._parse_paper(note)
            try:
                self._enrich_paper(paper)
            except Exception as e:
                print(f"Error enriching paper {paper.id}: {e}")
            yield paper
