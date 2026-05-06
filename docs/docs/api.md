[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "cost-stickiness-document-intelligence"
version = "0.1.0"
description = "Local document intelligence OCR MVP with FastAPI, OpenCV, Tesseract, and SQLite."
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
  "fastapi>=0.110",
  "uvicorn[standard]>=0.27",
  "python-multipart>=0.0.9",
  "opencv-python-headless>=4.9",
  "pytesseract>=0.3.10",
  "Pillow>=10.0",
  "pdf2image>=1.17"
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "httpx>=0.27", "reportlab>=4.0"]

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
