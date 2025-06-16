import json
from pathlib import Path

def generate_paragraph_css(pdf_name, target_width=696, target_height=900, original_width=612, original_height=792):
    scale_x = target_width / original_width
    scale_y = target_height / original_height

    project_dir = Path("project") / pdf_name
    grouped_paragraphs_path = project_dir / "grouped_paragraphs.json"
    output_dir = project_dir / "css"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load grouped paragraphs data
    with open(grouped_paragraphs_path, "r", encoding="utf-8") as f:
        grouped_paragraphs = json.load(f)

    generated_css_files = []

    for page, paragraphs in grouped_paragraphs.items():
        page_label = f"page{str(page).zfill(3)}"
        css_lines = [
            f".section {{ height: {target_height}px; width: {target_width}px; position: absolute; padding: 0; margin: 0; top: 19px; left: 0; display: contents; overflow: hidden; }}",
            f"img {{ width: {target_width}px; height: {target_height}px; position: absolute; top: 0px; left: 0px; z-index: 0; }}",
            f".{page_label}Container {{ width: {target_width}px; height: {target_height}px; position: absolute; left: 0px; top: 0px; z-index: 0; }}",
            f".para {{ margin: 0; padding: 0; display: block; unicode-bidi: isolate; }}"
        ]

        for para_idx, paragraph in enumerate(paragraphs, 1):
            if not paragraph:
                continue

            # Extract font styles from the first word in the paragraph
            first_word = paragraph[0]
            font_family = first_word.get("font_name", "sans-serif")
            font_size = round(first_word.get("font_size", 12) * scale_y, 2)
            font_color = first_word.get("font_color", "#000000")
            font_weight = first_word.get("font_weight", "normal")
            font_style = first_word.get("font_style", "normal")

            for word_idx, word in enumerate(paragraph, 1):
                x0 = word.get("x0", 0)
                x1 = word.get("x1", 0)
                top = word.get("top", 0)
                bottom = word.get("bottom", 0)

                left = x0 * scale_x
                top_scaled = top * scale_y
                width = (x1 - x0) * scale_x
                height = (bottom - top) * scale_y

                css_lines.append(f""".{page_label}para{para_idx}word{word_idx} {{
                    position: absolute;
                    top: {int(round(top_scaled))}px;
                    left: {int(round(left))}px;
                    width: {int(round(width))}px;
                    height: {int(round(height))}px;
                    font-family: "{font_family}";
                    font-size: {font_size}px;
                    color: {font_color};
                    font-weight: {font_weight};
                    font-style: {font_style};
                }}""")

        css_file = output_dir / f"css_{page_label}.css"
        css_file.write_text("\n".join(css_lines), encoding="utf-8")
        generated_css_files.append(str(css_file))

    return generated_css_files
