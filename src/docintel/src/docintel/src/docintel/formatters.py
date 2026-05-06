"""Output formatters for OCR results."""

from __future__ import annotations

from html import escape

from .models import OCRPage, OCRResult


def result_to_json(result: OCRResult) -> dict:
    """Return a structured JSON-serializable OCR payload."""

    return result.to_dict()


def page_to_html(page: OCRPage) -> str:
    """Render one OCR page as positioned HTML to preserve simple layout."""

    line_nodes = []
    for line in page.lines:
        bbox = line.bbox
        style = (
            f"left:{bbox['x']}px;top:{bbox['y']}px;"
            f"width:{bbox['width']}px;height:{bbox['height']}px;"
        )
        line_nodes.append(
            f'<div class="ocr-line" style="{style}">{escape(line.text)}</div>'
        )
    page_style = f"position:relative;width:{page.width}px;height:{page.height}px;"
    return (
        f'<section class="ocr-page" data-page="{page.page_number}" style="{page_style}">'
        + "".join(line_nodes)
        + "</section>"
    )


def result_to_html(result: OCRResult) -> str:
    """Render OCR result as a standalone HTML document with positioned lines."""

    pages = "\n".join(page_to_html(page) for page in result.pages)
    title = escape(result.filename)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>OCR: {title}</title>
  <style>
    body {{ font-family: system-ui, sans-serif; background:#f6f7f9; }}
    .ocr-page {{ margin: 1rem auto; background:white; border:1px solid #d8dee9; }}
    .ocr-line {{ position:absolute; white-space:pre; font-family:monospace; }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  {pages}
</body>
</html>"""
