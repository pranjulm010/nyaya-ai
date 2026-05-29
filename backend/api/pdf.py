import re

from pypdf import PdfReader


# =========================================
# CLEAN TEXT
# =========================================
def clean_text(text):

    if not text:
        return ""

    # remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================
# CHUNK TEXT
# =========================================
def chunk_text(
    text,
    chunk_size=1000,
    overlap=200
):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# =========================================
# EXTRACT PDF TEXT
# =========================================
def extract_pdf_text(pdf_file):

    try:

        reader = PdfReader(pdf_file)

        final_chunks = []

        total_pages = len(reader.pages)

        # =================================
        # LOOP THROUGH PAGES
        # =================================
        for page_number, page in enumerate(
            reader.pages,
            start=1
        ):

            try:

                raw_text = page.extract_text()

                cleaned_text = clean_text(
                    raw_text
                )

                if not cleaned_text:
                    continue

                # =========================
                # CREATE CHUNKS
                # =========================
                chunks = chunk_text(
                    cleaned_text
                )

                # =========================
                # STORE METADATA
                # =========================
                for chunk in chunks:

                    final_chunks.append({

                        "page": page_number,

                        "total_pages": total_pages,

                        "content": chunk,

                        "source":
                        getattr(
                            pdf_file,
                            "name",
                            "uploaded_pdf"
                        )
                    })

            except Exception as page_error:

                print(
                    f"Error on page "
                    f"{page_number}: "
                    f"{str(page_error)}"
                )

        return {
            "success": True,
            "chunks": final_chunks,
            "total_chunks": len(final_chunks),
            "total_pages": total_pages
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }