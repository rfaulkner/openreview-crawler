from iclr2025_crawler import ICLRCrawler

def main():
    crawler = ICLRCrawler()
    
    print("--- Basic Crawling Example ---")
    # Fetch top 5 papers
    for paper in crawler.crawl(limit=5):
        print(f"{paper.title} (Decision: {paper.decision}, Avg Rating: {paper.avg_rating})")

    print("\n--- Example 1: Fetch Top 5 Rated Accepted Papers ---")
    accepted_papers = []

    print("Searching for top rated accepted papers (scanning 100 papers)...")
    # Note: Scanning limit reduced to 100 for quicker demonstration
    for paper in crawler.crawl(limit=100):
        if paper.decision and 'Accept' in paper.decision and paper.avg_rating:
            accepted_papers.append(paper)

    # Sort by rating descending
    accepted_papers.sort(key=lambda p: p.avg_rating or 0, reverse=True)

    print("\n--- Top 5 Accepted Papers ---")
    for paper in accepted_papers[:5]:
        print(f"Rating: {paper.avg_rating:.2f} | Title: {paper.title}")

    print("\n--- Example 2: Fetch Lowest Rated Rejected Papers ---")
    rejected_papers = []

    print("Searching for lowest rated rejected papers (scanning 100 papers)...")
    # Note: Scanning limit reduced to 100 for quicker demonstration
    for paper in crawler.crawl(limit=100):
        if paper.decision and 'Reject' in paper.decision and paper.avg_rating:
            rejected_papers.append(paper)

    # Sort by rating ascending
    rejected_papers.sort(key=lambda p: p.avg_rating or 10)

    print("\n--- Top 5 Rejected Papers (Lowest Rated) ---")
    for paper in rejected_papers[:5]:
        print(f"Rating: {paper.avg_rating:.2f} | Title: {paper.title}")

if __name__ == "__main__":
    main()
