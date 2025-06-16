import fitz  # PyMuPDF
import json
from pathlib import Path

def extract_fonts_and_text_details(pdf_name):
    # Setup paths
    project_dir = Path("project") / pdf_name
    pdf_path = project_dir / "pdf"/f"{pdf_name}.pdf"
    font_json_path = project_dir / "fonts.json"
    detail_json_path = project_dir / "detailed_font_data.json"
    output_dir = project_dir / "fonts"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Open PDF
    doc = fitz.open(pdf_path)

    # Initialize containers
    fonts_dict = {}
    detailed_info = []

    for page_num in range(len(doc)):
        page = doc[page_num]

        # --- Extract Font Metadata ---
        fonts = page.get_fonts(full=True)
        for font in fonts:
            font_id = font[0]
            font_encoding = font[1]
            font_type = font[2]
            raw_font_name = font[3]
            is_embedded = font[6]

            # Remove font subset prefix (e.g., "ABCD+FontName")
            font_name = raw_font_name.split('+')[-1] if '+' in raw_font_name else raw_font_name

            if font_name not in fonts_dict:
                fonts_dict[font_name] = {
                    "type": font_type,
                    "encoding": font_encoding,
                    "embedded": is_embedded,
                    "pages": []
                }

            if (page_num + 1) not in fonts_dict[font_name]["pages"]:
                fonts_dict[font_name]["pages"].append(page_num + 1)

        # --- Extract Detailed Text & Font Info ---
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        detailed_info.append({
                            "page": page_num + 1,
                            "text": span["text"],
                            "font_name": span.get("font", "Unknown"),
                            "font_size": span.get("size", "Unknown"),
                            "font_color": "#{:06x}".format(span.get("color", 0)),
                            "bbox": span.get("bbox", [])
                        })

    # Save font metadata JSON
    with open(font_json_path, "w", encoding="utf-8") as f:
        json.dump(fonts_dict, f, indent=2)

    # Save detailed text/font info JSON
    with open(detail_json_path, "w", encoding="utf-8") as f:
        json.dump(detailed_info, f, indent=2)

    # Close PDF
    doc.close()

    return {
        "font_metadata_path": str(font_json_path),
        "detailed_text_path": str(detail_json_path)
    }
