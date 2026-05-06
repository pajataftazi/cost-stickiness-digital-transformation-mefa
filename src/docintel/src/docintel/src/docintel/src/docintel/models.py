"""Data models for document OCR results."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utcnow_iso() -> str:
    """Return a timezone-aware UTC timestamp in ISO-8601 format."""

    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class OCRWord:
    text: str
    confidence: float
    bbox: dict[str, int]

    def to_dict(self) -> dict[str, Any]:
        return {"text": self.text, "confidence": self.confidence, "bbox": self.bbox}


@dataclass(frozen=True)
class OCRLine:
    text: str
    bbox: dict[str, int]
    words: list[OCRWord] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "bbox": self.bbox,
            "words": [word.to_dict() for word in self.words],
        }


@dataclass(frozen=True)
class OCRPage:
    page_number: int
    width: int
    height: int
    text: str
    lines: list[OCRLine] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "page_number": self.page_number,
            "width": self.width,
            "height": self.height,
            "text": self.text,
            "lines": [line.to_dict() for line in self.lines],
        }


@dataclass(frozen=True)
class OCRResult:
    document_id: str
    filename: str
    content_type: str
    pages: list[OCRPage]
    created_at: str = field(default_factory=utcnow_iso)

    @property
    def text(self) -> str:
        return "\n\n".join(page.text for page in self.pages)

    def to_dict(self) -> dict[str, Any]:
        return {
            "document_id": self.document_id,
            "filename": self.filename,
            "content_type": self.content_type,
            "created_at": self.created_at,
            "text": self.text,
            "pages": [page.to_dict() for page in self.pages],
        }


@dataclass(frozen=True)
class DocumentRecord:
    id: str
    filename: str
    content_type: str
    storage_path: Path
    status: str
    created_at: str
    processed_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "filename": self.filename,
            "content_type": self.content_type,
            "storage_path": str(self.storage_path),
            "status": self.status,
            "created_at": self.created_at,
            "processed_at": self.processed_at,
        }
