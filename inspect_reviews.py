from openreview_crawler import OpenReviewCrawler
from pprint import pprint

def main():
    crawler = OpenReviewCrawler()
    
    print("Fetching papers and reviews to inspect structure...")
    # Fetch a few papers until we find one with reviews
    for paper in crawler.crawl(limit=10):
        if paper.reviews:
            print(f"\nPaper: {paper.title}")
            # We need to get the RAW note content to see keys that aren't in our Review model yet
            # Since crawler returns Review objects, we might need to peek using the client directly 
            # or just look at what we are parsing in crawler.py.
            # Actually, let's use the client to get raw notes for this paper to be sure.
            
            print(f"Fetching raw notes for forum: {paper.id}")
            notes = crawler.client.get_notes(forum=paper.id)
            for note in notes:
                if note.invitations and any('Official_Review' in inv for inv in note.invitations):
                    print("\n--- Review Note Content Keys ---")
                    pprint(list(note.content.keys()))
                    print("\n--- Full Content Sample ---")
                    pprint(note.content)
                    break # Just looking at one review is enough
            break

if __name__ == "__main__":
    main()
