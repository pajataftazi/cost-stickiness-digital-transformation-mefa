"""FastAPI application for the document intelligence OCR MVP."""

from __future__ import annotations

import os

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse

from .pipeline import ProcessingError
from .sdk import DocumentIntelligenceClient
from .store import DocumentStore

STORE_ROOT = os.getenv("DOCINTEL_STORE", ".docintel")
client = DocumentIntelligenceClient(store=DocumentStore(STORE_ROOT))
app = FastAPI(
    title="Document Intelligence OCR MVP",
    version="0.1.0",
    description="Upload images/PDFs, run local Tesseract OCR, and retrieve layout-aware JSON or HTML.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/documents", status_code=201)
async def upload_document(file: UploadFile = File(...)) -> dict:
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")
    record = client.upload_bytes(file.filename or "upload", data, file.content_type)
    return record.to_dict()


@app.get("/documents")
def list_documents() -> list[dict]:
    return client.list_documents()


@app.post("/documents/{document_id}/process")
def process_document(document_id: str) -> dict:
    try:
        return client.process_document(document_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ProcessingError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/documents/{document_id}/result")
def get_result(
    document_id: str,
    output_format: str = Query("json", pattern="^(json|html)$", alias="format"),
):
    result = client.get_result(document_id, output_format)
    if result is None:
        raise HTTPException(status_code=404, detail="Processed result not found")
    if output_format == "html":
        return HTMLResponse(str(result))
    return JSONResponse(result)
