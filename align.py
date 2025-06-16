import json
from pathlib import Path

def generate_html_pages_with_text(pdf_name, target_width=696, target_height=900, original_width=612, original_height=792):
    scale_x = target_width / original_width
    scale_y = target_height / original_height

    project_dir = Path("project") / pdf_name
    grouped_paragraphs_path = project_dir / "grouped_paragraphs.json"
    html_dir = project_dir / "html"
    html_dir.mkdir(parents=True, exist_ok=True)

    # Load grouped paragraphs data
    with open(grouped_paragraphs_path, "r", encoding="utf-8") as f:
        grouped_paragraphs = json.load(f)

    for page, paragraphs in grouped_paragraphs.items():
        page_label = f"page{str(page).zfill(3)}"

        html_lines = [
            "<?xml version=\"1.0\" encoding=\"utf-8\"?>",
            "<!DOCTYPE html>",
            "<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:ibooks=\"http://apple.com/ibooks/html-extensions\" xmlns:epub=\"http://www.idpf.org/2007/ops\">",
            "<head>",
            f"<meta name=\"viewport\" content=\"width={target_width}, height={target_height}\" />",
            f"<title>Page {page}</title>",
            f"<link rel=\"stylesheet\" type=\"text/css\" href=\"../../css/css_{page_label}.css\" />",
            "<link rel=\"stylesheet\" type=\"text/css\" href=\"../../css/template.css\" />",
            "</head>",
            "<body>",
            f"<div class=\"X103745_{page_label}\">",
            "<div class=\"page\">",
            f"<div class=\"{page_label}Container sec\">",
            "<div class=\"section\">",
            # Add the <img> tag for the background image
            f"<img src=\"../../images/{page_label}.jpg\" alt=\"Page {page}\" />"
        ]

        for para_idx, paragraph in enumerate(paragraphs, 1):
            # Get the position of the first word in the paragraph
            first_word = paragraph[0]
            para_top = first_word["top"] * scale_y
            para_left = first_word["x0"] * scale_x

            # Add a paragraph wrapper with absolute positioning
            html_lines.append(f"<p class=\"{page_label}para{para_idx}\"  top:{int(round(para_top))}px; left:{int(round(para_left))}px; margin:0; padding:0;\">")
            
            # Add words inside the paragraph
            for word_idx, word in enumerate(paragraph, 1):
                word_class = f"{page_label}para{para_idx}word{word_idx}"
                html_lines.append(f"<span class=\"{word_class}\">{word['text']}</span>")
            
            # Close the paragraph wrapper
            html_lines.append("</p>")

        html_lines.extend([
            "</div>",  # Close section
            "</div>",  # Close page container
            "</div>",  # Close page
            "</body>",
            "</html>"
        ])

        # Create a subdirectory for each page
        page_dir = html_dir / page_label
        page_dir.mkdir(parents=True, exist_ok=True)

        html_path = page_dir / f"{page_label}.html"
        html_path.write_text("\n".join(html_lines), encoding="utf-8")
        print(f"✅ Generated HTML: {html_path}")

    return "✅ All HTML pages generated."