from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any


@dataclass
class SourceDocument:
    source_type: str
    source_name: str
    title: str
    content: str

    url: Optional[str] = None
    page: Optional[int] = None
    citation: Optional[str] = None
    court: Optional[str] = None
    date: Optional[str] = None
    language: str = "en"

    trust_score: float = 0.5
    relevance_score: float = 0.5
    final_score: float = 0.0

    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)