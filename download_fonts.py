import fitz  # PyMuPDF
import os
import json
from pathlib import Path
from fontTools.ttLib import TTFont
import requests




def convert_all_cff_to_otf(fonts_dir):
    from pathlib import Path
from fontTools.ttLib import TTFont, newTable

def convert_all_cff_to_otf(fonts_dir: Path):
    if not fonts_dir.exists() or not fonts_dir.is_dir():
        print(f"❌ Folder not found: {fonts_dir}")
        return

    for font_path in fonts_dir.glob("*"):
        if font_path.suffix.lower() in [".ttf", ".otf"]:
            print(f"✅ Already usable font: {font_path.name}")
        else:
            print(f"🔁 Not TTF/OTF — checking: {font_path.name}")

            try:
                font = TTFont(font_path, recalcBBoxes=False, recalcTimestamp=False)

                if "CFF " not in font:
                    print(f"⚠️ Skipped: No CFF table in {font_path.name}")
                    continue

                # Add a basic name table if missing
                if "name" not in font:
                    name_table = newTable("name")
                    name_table.names = []
                    font["name"] = name_table

                # Save as .otf
                otf_path = fonts_dir / (font_path.stem + ".otf")
                font.save(otf_path)
                print(f"✅ Converted to OTF: {otf_path.name}")

            except Exception as e:
                print(f"❌ Error with {font_path.name}: {e}")

# ✅ Example usage:
# convert_all_cff_to_otf(Path("project/Y65893_BK/fonts"))




def extract_fonts_from_pdf(pdf_name):
    project_dir = Path("project") / pdf_name
    pdf_path = project_dir / "pdf"/f"{pdf_name}.pdf"
    fonts_dir = project_dir / "fonts"
    fonts_dir.mkdir(parents=True, exist_ok=True)
    fonts_json_path = project_dir / "fonts.json"
    
    

    doc = fitz.open(pdf_path)
    fonts_info = {}

    for page_index in range(len(doc)):
        page = doc[page_index]
        for font in page.get_fonts(full=True):
            xref = font[0]
            font_name = font[3]
            font_key = f"{font_name}_{xref}"

            # Skip duplicates
            if font_key in fonts_info:
                fonts_info[font_key]["pages"].append(page_index + 1)
                continue

            try:
                result = doc.extract_font(xref)

                # Handle all possible result formats
                if isinstance(result, dict):
                    font_bytes = result["file"]
                    ext = result["ext"]
                elif isinstance(result, tuple) and len(result) == 2:
                    font_bytes, ext = result
                elif isinstance(result, tuple) and len(result) == 4:
                    _, ext, _, font_bytes = result

                else:
                    raise ValueError("Unexpected return format from extract_font")
                 


                safe_name = font_name.replace("+", "_").replace(" ", "_")
                filename = f"{safe_name}_{xref}.{ext}"
                font_path = fonts_dir / filename

                # Save font
                if not font_path.exists():
                    with open(font_path, "wb") as f:
                        f.write(font_bytes)
                    print(f"✅ Saved: {filename}")

                

                    # Validate only TTF/OTF fonts
                    if ext.lower() in ("ttf", "otf"):
                        try:
                            TTFont(font_path)
                        except Exception as e:
                            print(f"❌ Invalid font: {filename}, error: {e}")
                            font_path.unlink()
                            continue
                    elif ext.lower() == "cff":
                        
                        print(f"⚠️ Saved CFF font: {filename} (not usable in browser)")

                        

                # Record metadata
                fonts_info[font_key] = {
                    "original_name": font_name,
                    "file": filename,
                    "type": font[2],
                    "encoding": font[1],
                    "pages": [page_index + 1],
                    "ext": ext
                }

            except Exception as e:
                print(f"❌ Failed to extract {font_name}: {e}")
                continue

    # Save metadata
    with open(fonts_json_path, "w", encoding="utf-8") as f:
        json.dump(fonts_info, f, indent=2)

    print(f"\n📦 Fonts saved to: {fonts_dir}")
    print(f"📑 Metadata written to: {fonts_json_path}")

    # Convert CFF fonts to OTF
    convert_all_cff_to_otf(fonts_dir)

    # Clean up unsupported formats
    clean_fonts_folder(fonts_dir)
    


# ✅ Example usage:
# extract_fonts_from_pdf("project/Y65893_BK/Y65893_BK.pdf")


def download_google_font(font_name, output_dir):
    """Download a font from Google Fonts."""
    base_url = "https://fonts.googleapis.com/css2"
    params = {
        "family": font_name.replace(" ", "+")
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        css_content = response.text
        font_urls = [line.split("url(")[1].split(")")[0] for line in css_content.splitlines() if "url(" in line]

        for font_url in font_urls:
            font_response = requests.get(font_url)
            if font_response.status_code == 200:
                font_filename = font_url.split("/")[-1]
                font_path = output_dir / font_filename
                with open(font_path, "wb") as f:
                    f.write(font_response.content)
                print(f"✅ Downloaded: {font_filename}")
            else:
                print(f"❌ Failed to download font from: {font_url}")
    else:
        print(f"❌ Failed to fetch CSS for font: {font_name}")

# Example usage:
# download_google_font("Roboto", Path("project/fonts"))

def clean_fonts_folder(fonts_dir):
    """Remove unsupported font formats from the fonts folder."""
    for font_path in fonts_dir.glob("*"):
        if font_path.suffix.lower() not in [".ttf", ".otf"]:
            print(f"❌ Removing unsupported font: {font_path.name}")
            font_path.unlink()
