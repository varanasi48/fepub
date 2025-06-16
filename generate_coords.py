import pdfplumber
from pathlib import Path
import json

def extract_text_coordinates(pdf_name):
    project_dir = Path("project") / pdf_name
    pdf_path = project_dir /"pdf"/f"{pdf_name}.pdf"
    output_json_path = project_dir / "text_coordinates.json"

    all_pages_data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            words = page.extract_words()
            page_data = {
                "page": page_num,
                "words": []
            }

            for word in words:
                page_data["words"].append({
                    "text": word["text"],
                    "x0": word["x0"],
                    "x1": word["x1"],
                    "top": word["top"],
                    "bottom": word["bottom"]
                })

            all_pages_data.append(page_data)

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(all_pages_data, f, indent=2)

    print(f"Text coordinates saved to: {output_json_path}")
