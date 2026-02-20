# OpenReview Crawler

A Python library to crawl papers, reviews, and decisions from OpenReview conferences (ICLR, ICML, NeurIPS, ACL, COLM, AAAI, EMNLP, and more).

## Quick Start

You can easily set up the environment and run examples using the provided scripts.

### 1. Setup

Run the setup script to create a virtual environment and install dependencies:

```bash
./setup.sh
```

### 2. Run Crawler

Each conference has a dedicated launch script inside the `launch/` folder. Run the one for your target conference:

```bash
# ICLR 2025 (default)
./launch/iclr_2025.sh

# Other supported conferences
./launch/icml_2025.sh
./launch/neurips_2025.sh
./launch/acl_2025.sh
./launch/colm_2025.sh
./launch/aaai_2025.sh
./launch/emnlp_2025.sh
```

Or run `crawl.py` directly with the `--conference` and `--limit` flags:

```bash
# Fetch top/bottom 10 papers from NeurIPS 2025
python crawl.py --conference NeurIPS2025 --limit 10

# Available conference keys:
# ICLR2025, ICML2025, NeurIPS2025, ACL2025, COLM2025, AAAI2025, EMNLP2025
```

## Manual Installation

If you prefer manual installation:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Crawling (ICLR 2025 Default)

```python
from openreview_crawler import OpenReviewCrawler

crawler = OpenReviewCrawler()

# Fetch top 10 papers
for paper in crawler.crawl(limit=10):
    print(f"{paper.title} (Decision: {paper.decision}, Avg Rating: {paper.avg_rating})")
```

### Crawling Other Conferences

Use the `--conference` flag when calling `crawl.py` to target a specific conference:

```bash
python crawl.py --conference ICML2025 --limit 20
```

The supported conference keys and their OpenReview venue IDs are defined in `crawl.py`:

| Key | OpenReview Venue ID |
|---|---|
| `ICLR2025` | `ICLR.cc/2025/Conference` |
| `ICML2025` | `ICML.cc/2025/Conference` |
| `NeurIPS2025` | `NeurIPS.cc/2025/Conference` |
| `ACL2025` | `aclweb.org/ACL/2025/Conference` |
| `COLM2025` | `colmweb.org/COLM/2025/Conference` |
| `AAAI2025` | `AAAI.org/2025/Conference` |
| `EMNLP2025` | `aclweb.org/EMNLP/2025/Conference` |

You can also pass a `conference_id` directly when using the library:

```python
from openreview_crawler import OpenReviewCrawler

crawler = OpenReviewCrawler(conference_id='ICML.cc/2025/Conference')
```

### Advanced Examples

#### 1. Fetch Top 5 Rated Accepted Papers (ICLR 2025)

```python
from openreview_crawler import OpenReviewCrawler

crawler = OpenReviewCrawler()
accepted_papers = []

print("Searching for top rated accepted papers...")
# Note: In a real scenario, you might need to crawl more.
for paper in crawler.crawl(limit=500):
    if paper.decision and 'Accept' in paper.decision and paper.avg_rating:
        accepted_papers.append(paper)

# Sort by rating descending
accepted_papers.sort(key=lambda p: p.avg_rating or 0, reverse=True)

print("\n--- Top 5 Accepted Papers ---")
for paper in accepted_papers[:5]:
    print(f"Rating: {paper.avg_rating:.2f} | Title: {paper.title}")
```

#### 2. Fetch Lowest Rated Rejected Papers

```python
from openreview_crawler import OpenReviewCrawler

crawler = OpenReviewCrawler()
rejected_papers = []

print("Searching for lowest rated rejected papers...")
for paper in crawler.crawl(limit=500):
    if paper.decision and 'Reject' in paper.decision and paper.avg_rating:
        rejected_papers.append(paper)

# Sort by rating ascending
rejected_papers.sort(key=lambda p: p.avg_rating or 10)

print("\n--- Top 5 Rejected Papers (Lowest Rated) ---")
for paper in rejected_papers[:5]:
    print(f"Rating: {paper.avg_rating:.2f} | Title: {paper.title}")
```

## Data Models

### Paper
- `id`: OpenReview ID
- `title`: Paper title
- `authors`: List of authors
- `abstract`: Abstract text
- `pdf_url`: URL to the PDF
- `decision`: Decision (e.g., "Accept (Poster)", "Reject")
- `avg_rating`: Average rating from reviews
- `reviews`: List of `Review` objects

### Review
- `rating`: Rating score
- `confidence`: Reviewer confidence
- `review_text`: Main review content

## Example Output

```bash
==================================================
 TOP 3 ACCEPTED PAPERS (Highest Rated)
==================================================
Title: Probabilistic Learning to Defer: Handling Missing Expert Annotations and Controlling Workload Distribution
Decision: Accept (Oral)
Avg Rating: 8.00
Review Summary:
  - Review 1: Rating 8/10.
  - Review 2: Rating 8/10.
  - Review 3: Rating 8/10.
  - Review 4: Rating 8/10.
----------------------------------------
Title: Kinetix: Investigating the Training of General Agents through Open-Ended Physics-Based Control Tasks
Decision: Accept (Oral)
Avg Rating: 8.00
Review Summary:
  - Review 1: Rating 8/10.
  - Review 2: Rating 8/10.
  - Review 3: Rating 8/10.
  - Review 4: Rating 8/10.
----------------------------------------
Title: Joint Graph Rewiring and Feature Denoising via Spectral Resonance
Decision: Accept (Oral)
Avg Rating: 8.00
Review Summary:
  - Review 1: Rating 8/10.
  - Review 2: Rating 8/10.
  - Review 3: Rating 8/10.
  - Review 4: Rating 8/10.
  - Review 5: Rating 8/10.
----------------------------------------

==================================================
 TOP 3 REJECTED PAPERS (Lowest Rated)
==================================================
Title: Differentiable Implicit Solver on Graph Neural Networks for Forward and Inverse Problems
Decision: Reject
Avg Rating: 2.00
Review Summary:
  - Review 1: Rating 3/10.
  - Review 2: Rating 1/10.
  - Review 3: Rating 3/10.
  - Review 4: Rating 1/10.
----------------------------------------
Title: From Counseling Transcript to Mind Map: Leveraging LLMs for Effective Summarization in Mental Health Counseling
Decision: Reject
Avg Rating: 2.00
Review Summary:
  - Review 1: Rating 3/10.
  - Review 2: Rating 1/10.
  - Review 3: Rating 1/10.
  - Review 4: Rating 3/10.
----------------------------------------
Title: Quantized Approximately Orthogonal Recurrent Neural Networks
Decision: Reject
Avg Rating: 3.00
Review Summary:
  - Review 1: Rating 3/10.
  - Review 2: Rating 3/10.
  - Review 3: Rating 5/10.
  - Review 4: Rating 1/10.
----------------------------------------
```
