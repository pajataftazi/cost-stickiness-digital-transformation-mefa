# Document Intelligence OCR MVP

A local document intelligence OCR tool inspired by Chandra. The project now
provides a thin Python SDK over a SQLite-backed document processing store plus a
FastAPI service for uploading images/PDFs, running OCR with OpenCV + Tesseract,
and retrieving layout-aware JSON or HTML output.

## MVP scope

### Included

- Image upload and PDF upload support.
- Local persistence for uploaded files, document metadata, and OCR outputs.
- OpenCV preprocessing before Tesseract OCR.
- Structured JSON output with page, line, word, confidence, and bounding-box
  metadata.
- HTML output with positioned OCR lines to preserve simple source layout.
- Minimal Python SDK for upload, processing, listing, and result retrieval.
- Tests for storage, SDK flow, layout grouping, and HTML layout preservation

### Deferred

- Batch processing.
- Improved OCR models or custom accuracy tuning.
- User accounts, authentication, and authorization.

## Requirements

- Python 3.10+
- Tesseract OCR installed on your system and available on `PATH`
- Poppler installed on your system for PDF rendering through `pdf2image`

Python dependencies are listed in `requirements.txt` and `pyproject.toml`.

## Install

```
pip install -r requirements.txt
```

## Run the API

```
uvicorn docintel.api:app --reload
```

By default, uploads and SQLite metadata are stored under `.docintel/`. Override
this with:

```
DOCINTEL_STORE=/tmp/docintel uvicorn docintel.api:app --reload
```

## API quick start

Upload a document:

```
curl -F "file=@sample.png" http://localhost:8000/documents
```

Process the document:

```
curl -X POST http://localhost:8000/documents/{document_id}/process
```

Fetch JSON output:

```
curl http://localhost:8000/documents/{document_id}/result?format=json
```

Fetch layout-preserving HTML:

```
curl http://localhost:8000/documents/{document_id}/result?format=html
```

See [`docs/api.md`](docs/api.md) for endpoint documentation and SDK examples.

## SDK quick start

```python
from docintel import DocumentIntelligenceClient

client = DocumentIntelligenceClient()
record = client.upload_file("sample.png")
json_result = client.process_document(record.id)
html_result = client.get_result(record.id, output_format="html")
```

## Project layout

```text
src/docintel/
  api.py         FastAPI app and endpoints
  formatters.py  JSON/HTML output formatting
  models.py      OCR and document data models
  pipeline.py    Image/PDF loading, OpenCV preprocessing, Tesseract OCR
  sdk.py         Thin Python SDK
  store.py       SQLite document store
tests/           Unit tests for core MVP behavior
docs/api.md      API documentation
```

## Testing

```bash
pytest
```

The default tests avoid external OCR binaries by validating the local store,
formatters, SDK orchestration, and layout grouping logic with small deterministic
fixtures. End-to-end OCR requires Tesseract and, for PDFs, Poppler.
