import os
from typing import Dict, Any

from pypdf import PdfReader
from docx import Document

from rag.chunker import create_chunks_with_metadata
from rag.ocr_extractor import extract_text_with_ocr


def extract_document_text(
    file_path: str,
    user_id: str,
    document_id: str,
    source_name: str
) -> Dict[str, Any]:

    try:
        document_type = detect_document_type(file_path)

        print("DOCUMENT TYPE:", document_type)
        print("DOCUMENT PATH:", file_path)

        if document_type == "pdf":
            return extract_pdf_text(
                file_path=file_path,
                user_id=user_id,
                document_id=document_id,
                source_name=source_name
            )

        if document_type == "docx":
            return extract_docx_text(
                file_path=file_path,
                user_id=user_id,
                document_id=document_id,
                source_name=source_name
            )

        if document_type in ["txt", "md"]:
            return extract_plain_text(
                file_path=file_path,
                user_id=user_id,
                document_id=document_id,
                source_name=source_name,
                document_type=document_type
            )

        return {
            "success": False,
            "error": "Unsupported document type."
        }

    except Exception as error:
        print("DOCUMENT EXTRACTION ERROR:", error)
        return {
            "success": False,
            "error": str(error)
        }


def detect_document_type(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return "pdf"

    if ext == ".docx":
        return "docx"

    if ext == ".txt":
        return "txt"

    if ext == ".md":
        return "md"

    return "unknown"


def extract_pdf_text(
    file_path: str,
    user_id: str,
    document_id: str,
    source_name: str
) -> Dict[str, Any]:

    reader = PdfReader(file_path)

    chunks = []
    total_pages = len(reader.pages)

    print("PDF TOTAL PAGES:", total_pages)

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):
        raw_text = page.extract_text() or ""

        print(
            f"PAGE {page_number} PYPDF TEXT LENGTH:",
            len(raw_text)
        )

        if raw_text.strip():
            print(
                f"PAGE {page_number} PREVIEW:",
                raw_text[:300]
            )

        if not raw_text.strip():
            print(
                f"PAGE {page_number}: No text found, trying OCR..."
            )

            raw_text = extract_text_with_ocr(
                file_path=file_path,
                page_number=page_number
            )

            print(
                f"PAGE {page_number} OCR TEXT LENGTH:",
                len(raw_text)
            )

        metadata = {
            "user_id": user_id,
            "document_id": document_id,
            "source": source_name,
            "document_type": "pdf",
            "page": page_number,
            "total_pages": total_pages,
        }

        page_chunks = create_chunks_with_metadata(
            text=raw_text,
            metadata=metadata
        )

        chunks.extend(page_chunks)

    print("TOTAL PDF CHUNKS:", len(chunks))

    return {
        "success": True,
        "document_type": "pdf",
        "chunks": chunks,
        "total_pages": total_pages,
        "total_chunks": len(chunks),
    }


def extract_docx_text(
    file_path: str,
    user_id: str,
    document_id: str,
    source_name: str
) -> Dict[str, Any]:

    doc = Document(file_path)

    text = "\n".join(
        para.text
        for para in doc.paragraphs
        if para.text.strip()
    )

    print("DOCX TEXT LENGTH:", len(text))

    metadata = {
        "user_id": user_id,
        "document_id": document_id,
        "source": source_name,
        "document_type": "docx",
        "page": None,
        "total_pages": None,
    }

    chunks = create_chunks_with_metadata(
        text=text,
        metadata=metadata
    )

    return {
        "success": True,
        "document_type": "docx",
        "chunks": chunks,
        "total_pages": None,
        "total_chunks": len(chunks),
    }


def extract_plain_text(
    file_path: str,
    user_id: str,
    document_id: str,
    source_name: str,
    document_type: str
) -> Dict[str, Any]:

    with open(
        file_path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as file:
        text = file.read()

    print("TEXT FILE LENGTH:", len(text))

    metadata = {
        "user_id": user_id,
        "document_id": document_id,
        "source": source_name,
        "document_type": document_type,
        "page": None,
        "total_pages": None,
    }

    chunks = create_chunks_with_metadata(
        text=text,
        metadata=metadata
    )

    return {
        "success": True,
        "document_type": document_type,
        "chunks": chunks,
        "total_pages": None,
        "total_chunks": len(chunks),
    }