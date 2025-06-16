import json
from pathlib import Path

def bbox_overlap_ratio(word_bbox, span_bbox):
    if not span_bbox or len(span_bbox) != 4:
        return 0
    x0 = max(word_bbox[0], span_bbox[0])
    y0 = max(word_bbox[1], span_bbox[1])
    x1 = min(word_bbox[2], span_bbox[2])
    y1 = min(word_bbox[3], span_bbox[3])
    if x0 >= x1 or y0 >= y1:
        return 0
    intersect_area = (x1 - x0) * (y1 - y0)
    word_area = (word_bbox[2] - word_bbox[0]) * (word_bbox[3] - word_bbox[1])
    return intersect_area / word_area if word_area else 0

def smart_match(word, entry):
    if not isinstance(word, dict) or "page" not in word:
        print(f"[Warning] Skipping word without 'page': {word}")
        return False
    if not isinstance(entry, dict) or "page" not in entry:
        print(f"[Warning] Skipping font entry without 'page': {entry}")
        return False
    if word["page"] != entry.get("page"):
        return False
    if word.get("text") not in entry.get("text", ""):
        return False
    word_bbox = [word["x0"], word["top"], word["x1"], word["bottom"]]
    span_bbox = entry.get("bbox", [])
    return bbox_overlap_ratio(word_bbox, span_bbox) > 0.5

def merge_text_and_font_data(pdf_name):
    project_dir = Path("project") / pdf_name
    coords_path = project_dir / "text_coordinates.json"
    fontdata_path = project_dir / "detailed_font_data.json"
    metadata_path = project_dir / "fonts.json"
    merged_path = project_dir / "merged_word_data.json"

    with open(coords_path, "r", encoding="utf-8") as f:
        coords_pages = json.load(f)
    with open(fontdata_path, "r", encoding="utf-8") as f:
        fontdata = json.load(f)
    with open(metadata_path, "r", encoding="utf-8") as f:
        font_metadata = json.load(f)

    merged = []

    for page in coords_pages:
        page_num = page.get("page")
        for word in page.get("words", []):
            if "text" not in word or not word["text"]:
                continue

            # Inject page number into each word
            word["page"] = page_num

            text = word["text"].strip()
            merged_word = word.copy()

            # Try smart match using span text + bbox overlap
            font_info = next((entry for entry in fontdata if smart_match(word, entry)), None)

            if font_info:
                merged_word.update({
                    "font_name": font_info.get("font_name"),
                    "font_size": font_info.get("font_size"),
                    "font_color": font_info.get("font_color"),
                    "bbox": font_info.get("bbox")
                })

                # Merge font metadata
                font_name = font_info.get("font_name")
                if font_name in font_metadata:
                    merged_word.update(font_metadata[font_name])
                else:
                    print(f"⚠️ Font '{font_name}' not found in fonts.json (page {page_num}, word: '{text}')")
            else:
                # Fallback values
                print(f"⚠️ No font match for word '{text}' on page {page_num}. Using fallback font.")
                merged_word.update({
                    "font_name": "sans-serif",
                    "font_size": 12.0,
                    "font_color": "#000000"
                })

            merged.append(merged_word)

    with open(merged_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2)

    print(f"\n✅ Merged word data written to: {merged_path}\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        merge_text_and_font_data(sys.argv[1])
    else:
        print("Usage: python merge_text_and_font_data.py <PDF_NAME>")
