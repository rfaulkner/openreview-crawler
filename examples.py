from iclr2025_crawler import ICLRCrawler

def print_paper_details(paper):
    print(f"Title: {paper.title}")
    print(f"Decision: {paper.decision}")
    print(f"Avg Rating: {paper.avg_rating:.2f}" if paper.avg_rating else "Avg Rating: N/A")
    print("Review Summary:")
    if paper.reviews:
        for i, review in enumerate(paper.reviews, 1):
            rating = review.rating if review.rating else "N/A"
            # Truncate review text for summary
            text_snippet = review.review_text[:100].replace('\n', ' ') + "..." if review.review_text else ""
            print(f"  - Review {i}: Rating {rating}/10. {text_snippet}")
    else:
        print("  No reviews found.")
    print("-" * 40)

def main():
    crawler = ICLRCrawler()
    
    print("Scanning papers (limit 200)...")
    papers = []
    # Fetch a batch of papers to process
    for paper in crawler.crawl(limit=200):
        if paper.decision: # Only interested in papers with decisions for this example
            papers.append(paper)

    # Filter for accepted and rejected
    accepted = [p for p in papers if 'Accept' in p.decision and p.avg_rating is not None]
    rejected = [p for p in papers if 'Reject' in p.decision and p.avg_rating is not None]

    # Sort
    accepted.sort(key=lambda p: p.avg_rating, reverse=True)
    rejected.sort(key=lambda p: p.avg_rating) # Ascending for lowest rated

    print("\n" + "="*50)
    print(" TOP 3 ACCEPTED PAPERS (Highest Rated)")
    print("="*50)
    for p in accepted[:3]:
        print_paper_details(p)

    print("\n" + "="*50)
    print(" TOP 3 REJECTED PAPERS (Lowest Rated)")
    print("="*50)
    for p in rejected[:3]:
        print_paper_details(p)

if __name__ == "__main__":
    main()
