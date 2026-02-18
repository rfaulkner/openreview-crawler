from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Review:
    id: str
    reviewer: str
    rating: Optional[int] = None
    confidence: Optional[int] = None
    title: Optional[str] = None
    review_text: Optional[str] = None
    strengths: Optional[str] = None
    weaknesses: Optional[str] = None
    invitation: str = ""
    reply_to: str = ""

@dataclass
class Paper:
    id: str
    title: str
    authors: List[str]
    abstract: str
    pdf_url: str
    keywords: List[str] = field(default_factory=list)
    reviews: List[Review] = field(default_factory=list)
    decision: Optional[str] = None
    avg_rating: Optional[float] = None
    status: str = "Unknown"
    
