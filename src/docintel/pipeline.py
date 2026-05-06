"""Document ingestion and OCR processing pipeline."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Iterable

from .models import OCRLine, OCRPage, OCRResult, OCRWord

SUPPORTED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"}
SUPPORTED_PDF_EXTENSIONS = {".pdf"}


class ProcessingError(RuntimeError):
    """Raised when OCR processing cannot complete."""


class DocumentProcessor:
    """Convert image/PDF inputs to layout-aware OCR pages."""

    def __init__(self, tesseract_config: str = "--psm 6") -> None:
        self.tesseract_config = tesseract_config

    def process(
        self, document_id: str, filename: str, content_type: str, path: str | Path
    ) -> OCRResult:
        pages = []
        for index, image in enumerate(self._load_pages(Path(path)), start=1):
            pages.append(self._ocr_image(image, index))
        return OCRResult(
            document_id=document_id,
            filename=filename,
            content_type=content_type,
            pages=pages,
        )

    def _load_pages(self, path: Path) -> Iterable[object]:
        suffix = path.suffix.lower()
        if suffix in SUPPORTED_IMAGE_EXTENSIONS:
            yield self._read_image(path)
            return
        if suffix in SUPPORTED_PDF_EXTENSIONS:
            yield from self._read_pdf(path)
            return
        raise ProcessingError(f"Unsupported document type: {suffix or 'unknown'}")

    @staticmethod
    def _read_image(path: Path):
        try:
            import cv2
        except ImportError as exc:
            raise ProcessingError("OpenCV is required for image processing") from exc
        image = cv2.imread(str(path))
        if image is None:
            raise ProcessingError(f"Could not read image: {path}")
        return image

    @staticmethod
    def _read_pdf(path: Path):
        try:
            import cv2
            import numpy as np
            from pdf2image import convert_from_path
        except ImportError as exc:
            raise ProcessingError(
                "PDF processing requires pdf2image, Pillow, NumPy, and OpenCV"
            ) from exc
        try:
            pil_pages = convert_from_path(str(path), dpi=200)
        except Exception as exc:
            raise ProcessingError(
                "Could not render PDF. Ensure Poppler is installed and available on PATH."
            ) from exc
        for page in pil_pages:
            yield cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)

    def _ocr_image(self, image, page_number: int) -> OCRPage:
        try:
            import cv2
            import pytesseract
            from pytesseract import Output
        except ImportError as exc:
            raise ProcessingError("pytesseract and OpenCV are required for OCR") from exc

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        denoised = cv2.medianBlur(gray, 3)
        _, thresholded = cv2.threshold(
            denoised, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU
        )
        data = pytesseract.image_to_data(
            thresholded, output_type=Output.DICT, config=self.tesseract_config
        )
        height, width = thresholded.shape[:2]
        lines = self._group_words_into_lines(data)
        text = "\n".join(line.text for line in lines)
        return OCRPage(
            page_number=page_number,
            width=width,
            height=height,
            text=text,
            lines=lines,
        )

    @staticmethod
    def _group_words_into_lines(data: dict) -> list[OCRLine]:
        grouped: dict[tuple[int, int, int], list[OCRWord]] = defaultdict(list)
        total = len(data.get("text", []))
        for i in range(total):
            text = str(data["text"][i]).strip()
            if not text:
                continue
            confidence = _parse_confidence(data.get("conf", [])[i])
            if confidence < 0:
                continue
            key = (
                int(data.get("page_num", [1] * total)[i]),
                int(data.get("block_num", [0] * total)[i]),
                int(data.get("line_num", [0] * total)[i]),
            )
            grouped[key].append(
                OCRWord(
                    text=text,
                    confidence=confidence,
                    bbox={
                        "x": int(data["left"][i]),
                        "y": int(data["top"][i]),
                        "width": int(data["width"][i]),
                        "height": int(data["height"][i]),
                    },
                )
            )
        lines = []
        for _, words in sorted(grouped.items()):
            words = sorted(words, key=lambda word: word.bbox["x"])
            x1 = min(word.bbox["x"] for word in words)
            y1 = min(word.bbox["y"] for word in words)
            x2 = max(word.bbox["x"] + word.bbox["width"] for word in words)
            y2 = max(word.bbox["y"] + word.bbox["height"] for word in words)
            lines.append(
                OCRLine(
                    text=" ".join(word.text for word in words),
                    bbox={"x": x1, "y": y1, "width": x2 - x1, "height": y2 - y1},
                    words=words,
                )
            )
        return sorted(lines, key=lambda line: (line.bbox["y"], line.bbox["x"]))


def _parse_confidence(value: object) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return -1.0
