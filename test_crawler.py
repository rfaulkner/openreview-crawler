from iclr2025_crawler import ICLRCrawler
from pprint import pprint

def main():
    print("Initializing ICLR 2025 Crawler...")
    crawler = ICLRCrawler()
    
    print("Crawling top 5 papers and their reviews...")
    try:
        count = 0
        for paper in crawler.crawl(limit=5):
            count += 1
            print(f"\n--- Paper {count} ---")
            print(f"ID: {paper.id}")
            print(f"Title: {paper.title}")
            print(f"Authors: {', '.join(paper.authors)}")
            print(f"Abstract: {paper.abstract[:100]}...")
            print(f"Reviews: {len(paper.reviews)}")
            
            if paper.reviews:
                print("\tFirst Review sample:")
                pprint(paper.reviews[0])
                
    except Exception as e:
        print(f"An error occurred during crawling: {e}")

if __name__ == "__main__":
    main()
