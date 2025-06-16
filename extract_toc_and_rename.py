import json
from pathlib import Path

def extract_toc_and_rename(project_dir):
    detailed_font_path = project_dir / "detailed_font_data.json"
    html_dir = project_dir / "html"

    # Load detailed font data
    with open(detailed_font_path, "r", encoding="utf-8") as f:
        font_data = json.load(f)

    # Extract TOC entries based on refined criteria
    toc_entries = []
    toc_heading_found = False
    for item in font_data:
        text = item.get("text", "").strip()

        # Check for TOC heading
        if "Table of Contents" in text:
            toc_heading_found = True
            continue

        # Extract entries after TOC heading is found
        if toc_heading_found and item.get("font_size", 0) > 20:
            toc_entries.append({
                "page": item["page"],
                "text": text
            })

    # Debugging: Print extracted TOC entries
    print("Extracted TOC entries:", toc_entries)

    # Rename HTML files based on TOC entries
    for idx, entry in enumerate(toc_entries, 1):
        page_num = entry["page"]
        old_html_path = html_dir / f"page{page_num:03}" / f"page{page_num:03}.html"
        new_html_path = html_dir / f"toc{idx}.html"

        if old_html_path.exists():
            old_html_path.rename(new_html_path)
            print(f"Renamed {old_html_path} to {new_html_path}")

    return toc_entries

# Example usage
project_dir = Path("project/X103745")
toc_entries = extract_toc_and_rename(project_dir)
print("Extracted TOC entries:", toc_entries)
