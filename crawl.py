import argparse
from openreview_crawler import OpenReviewCrawler, export_papers_to_json

# Mapping of friendly conference names to their OpenReview venue IDs.
CONFERENCE_IDS = {
    "ICLR2025":    "ICLR.cc/2025/Conference",
    "ICML2025":    "ICML.cc/2025/Conference",
    "NeurIPS2025": "NeurIPS.cc/2025/Conference",
    "ACL2025":     "aclweb.org/ACL/2025/Conference",
    "COLM2025":    "colmweb.org/COLM/2025/Conference",
    "AAAI2025":    "AAAI.org/2025",
    "EMNLP2025":   "EMNLP/2025/Conference",
}

DEFAULT_CONFERENCE = "ICLR2025"

def print_paper_details(paper):
    print(f"Title: {paper.title}")
    print(f"Decision: {paper.decision}")
    print(f"Avg Rating: {paper.avg_rating:.2f}" if paper.avg_rating else "Avg Rating: N/A")
    print("-" * 40)

def main():
    parser = argparse.ArgumentParser(description="Crawl OpenReview papers and export to JSON.")
    parser.add_argument(
        '--conference',
        type=str,
        default=DEFAULT_CONFERENCE,
        choices=list(CONFERENCE_IDS.keys()),
        help=f"Conference to crawl (default: {DEFAULT_CONFERENCE}). "
             f"Choices: {', '.join(CONFERENCE_IDS.keys())}"
    )
    parser.add_argument('--limit', type=int, default=5, help='Number of papers to find for each category (default: 5)')
    args = parser.parse_args()

    conference_id = CONFERENCE_IDS[args.conference]
    print(f"Conference: {args.conference}  →  venue ID: {conference_id}")

    crawler = OpenReviewCrawler(conference_id=conference_id)
    
    print(f"Scanning papers to find top {args.limit} accepted and bottom {args.limit} rejected...")
    
    # We need to crawl enough papers to find the requested amount of high/low quality ones.
    # Since we can't filter by decision/rating in the API query easily without fetching,
    # we'll fetch a larger batch. 
    # Heuristic: fetch 10x the limit to have a good chance, or up to 500 max to avoid taking forever.
    scan_limit = min(args.limit * 200, 25000) 

    papers = []
    for paper in crawler.crawl(limit=scan_limit):
        if paper.decision: 
             papers.append(paper)

    # Filter for accepted and rejected
    accepted = [p for p in papers if 'Accept' in p.decision and p.avg_rating is not None]
    rejected = [p for p in papers if 'Reject' in p.decision and p.avg_rating is not None]

    # Sort
    accepted.sort(key=lambda p: p.avg_rating, reverse=True)
    rejected.sort(key=lambda p: p.avg_rating) # Ascending for lowest rated

    # Slice to limit
    top_accepted = accepted[:args.limit]
    bottom_rejected = rejected[:args.limit]

    print("\n" + "="*50)
    print(f" TOP {len(top_accepted)} ACCEPTED PAPERS (Highest Rated)")
    print("="*50)
    for p in top_accepted:
        print_paper_details(p)

    # Export High Quality
    if top_accepted:
        export_papers_to_json(top_accepted, f"example_out/{args.conference}_{args.limit}_high_quality_papers.json")

    print("\n" + "="*50)
    print(f" TOP {len(bottom_rejected)} REJECTED PAPERS (Lowest Rated)")
    print("="*50)
    for p in bottom_rejected:
        print_paper_details(p)

    # Export Low Quality
    if bottom_rejected:
        export_papers_to_json(bottom_rejected, f"example_out/{args.conference}_{args.limit}_low_quality_papers.json")

if __name__ == "__main__":
    main()
