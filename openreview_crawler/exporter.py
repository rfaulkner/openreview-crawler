import json
from typing import List
from .models import Paper

def export_papers_to_json(papers: List[Paper], filename: str, venue: str = "ICLR 2025"):
    output_data = {}
    
    for paper in papers:
        # Link construction
        link = f"https://openreview.net/forum?id={paper.id}"
        
        # Collect scores and aggregate text
        scores = []
        strengths_list = []
        weaknesses_list = []
        
        if paper.reviews:
            for review in paper.reviews:
                if review.rating:
                    scores.append(review.rating)
                
                if review.strengths:
                    strengths_list.append(f"- {review.strengths.strip()}")
                if review.weaknesses:
                    weaknesses_list.append(f"- {review.weaknesses.strip()}")
        
        # strengths_summary = "\n\n".join(strengths_list)
        # weaknesses_summary = "\n\n".join(weaknesses_list)

        paper_data = {
            "venue": venue,
            "title": paper.title,
            "link": link,
            "abstract": paper.abstract,
            "decision": paper.decision if paper.decision else "Pending",
            "review scores": scores,
            "strengths": strengths_list,
            "weaknesses": weaknesses_list,
        }
        
        output_data[paper.id] = paper_data

    print(f"Exporting {len(output_data)} papers to {filename}...")
    with open(filename, 'w') as f:
        json.dump(output_data, f, indent=4)
    print(f"Done writing to {filename}.")
