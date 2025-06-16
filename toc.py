import pdfplumber
import re
from pathlib import Path

def is_toc_page(text):
    text_lower = text.lower()

    # Check if it contains 'contents' or similar keyword
    has_toc_keyword = any(keyword in text_lower for keyword in ["contents", "table of contents", "toc"])

    # Check for dotted leader lines like "Chapter 1 ........ 5"
    has_dots_lines = bool(re.findall(r"\.{2,}\s*\d+", text))

    # Count lines that end in a number (likely page numbers)
    lines = text.splitlines()
    page_number_lines = sum(1 for line in lines if re.search(r"\d+$", line.strip()))

    return has_toc_keyword or (has_dots_lines and page_number_lines > 3)

def find_toc_pages(pdf_path):
    toc_pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            if is_toc_page(text):
                toc_pages.append(i)  # 0-based index for replacement
    return toc_pages

def generate_and_replace_toc(pdf_path, output_dir):
    toc_pages = find_toc_pages(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            if i in toc_pages:
                # Generate new TOC HTML content
                new_toc_content = f"<h1>Table of Contents - Page {i + 1}</h1>"
                html_content = f"""<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <title>TOC Page {i + 1}</title>
  <link rel='stylesheet' href='../css/toc.css'>  <!-- Ensure correct CSS path -->
</head>
<body>
  {new_toc_content}
</body>
</html>"""
                html_path = output_dir / f"toc_page_{i + 1}.html"
                html_path.write_text(html_content, encoding='utf-8')
                print(f"Generated TOC HTML: {html_path}")
            else:
                # Generate regular HTML content for non-TOC pages
                text = page.extract_text() or "[No text found]"
                html_content = f"""<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <title>Page {i + 1}</title>
  <link rel='stylesheet' href='../css/page.css'>  <!-- Ensure correct CSS path -->
</head>
<body>
  <pre>{text}</pre>
</body>
</html>"""
                html_path = output_dir / f"page_{i + 1}.html"
                html_path.write_text(html_content, encoding='utf-8')
                print(f"Generated HTML: {html_path}")

# Example usage
generate_and_replace_toc("d:\\zz\\project\\Y65893_BK.pdf", "d:\\zz\\project\\html_output")

     
