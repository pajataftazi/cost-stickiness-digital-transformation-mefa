# Document Intelligence OCR API

This MVP exposes a local FastAPI service for uploading image/PDF documents,
processing them with OpenCV + Tesseract, and returning layout-aware OCR output.

## Run locally

```bash
pip install -r requirements.txt
uvicorn docintel.api:app --reload
```

Set `DOCINTEL_STORE=/path/to/store` to change where uploads and SQLite metadata
are persisted. The default is `.docintel/` in the current working directory.

## Endpoints

### `GET /health`

Returns service status.

### `POST /documents`

Multipart upload endpoint.

```bash
curl -F "file=@sample.png" http://localhost:8000/documents
```

Response includes `id`, `filename`, `content_type`, `storage_path`, and status.

### `POST /documents/{document_id}/process`

Runs OCR for an uploaded document and stores both JSON and HTML outputs.

```bash
curl -X POST http://localhost:8000/documents/{document_id}/process
```

### `GET /documents/{document_id}/result?format=json`

Returns structured JSON with document text, pages, lines, words, confidence, and
bounding boxes.

### `GET /documents/{document_id}/result?format=html`

Returns standalone HTML with absolutely positioned OCR lines so simple document
layout is preserved.

## SDK example

```python
from docintel import DocumentIntelligenceClient

client = DocumentIntelligenceClient()
record = client.upload_file("sample.png")
json_result = client.process_document(record.id)
html_result = client.get_result(record.id, output_format="html")
```
