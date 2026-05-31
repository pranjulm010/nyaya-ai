import os

import pytesseract
from pdf2image import convert_from_path
from dotenv import load_dotenv

load_dotenv()

pytesseract.pytesseract.tesseract_cmd = os.getenv(
    "TESSERACT_CMD",
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text_with_ocr(
    file_path: str,
    page_number: int | None = None
) -> str:
    try:
        images = convert_from_path(
            file_path,
            first_page=page_number,
            last_page=page_number,
            dpi=300
        )

        extracted_text = []

        for image in images:
            text = pytesseract.image_to_string(
                image,
                lang="eng"
            )

            if text.strip():
                extracted_text.append(text)

        final_text = "\n".join(extracted_text).strip()

        print(
            f"OCR PAGE {page_number} TEXT LENGTH:",
            len(final_text)
        )

        return final_text

    except Exception as error:
        print("OCR ERROR:", error)
        return ""