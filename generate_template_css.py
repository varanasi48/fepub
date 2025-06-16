import json
from pathlib import Path

def find_font_file(fonts_dir, clean_name):
    """
    Search for a font file in fonts_dir matching clean_name with .otf, .ttf, or .cff extension (case-insensitive).
    Returns the Path object and extension, or (None, None) if not found.
    """
    for ext in ['otf', 'ttf', 'cff']:
        for file in fonts_dir.glob(f"*.{ext}"):
            if file.stem.lower() == clean_name.lower():
                return file, ext
    return None, None

def generate_template_css(pdf_name):
    project_dir = Path("project") / pdf_name
    json_path = project_dir / "fonts.json"
    css_dir = project_dir / "css"
    temp_path = css_dir / "template.css"
    fonts_dir = project_dir / "fonts"

    css_dir.mkdir(parents=True, exist_ok=True)

    with json_path.open('r', encoding='utf-8') as f:
        fonts_data = json.load(f)

    css_content = []

    for font_name in fonts_data:
        print(f"Processing font: {font_name}")
        clean_name = font_name.split('+')[1] if '+' in font_name else font_name
        print(f"Cleaned font name: {clean_name}")

        font_file, ext = find_font_file(fonts_dir, clean_name)
        if not font_file:
            print(f"⚠️ Font file not found for: {clean_name}")
            continue

        css_content.append(
            f'@font-face {{font-family: "{clean_name}"; font-style: normal; font-weight: normal; src: url(\'../fonts/{font_file.name}\'); }}'
        )
        print(f"✅ Added @font-face for {clean_name}")

    # Static CSS
    css_content.append("""
body {
    width: 624px;
    height: 900px;
    position: relative;
    overflow: hidden;
    margin: 0 auto;
}
img {
    width: 624px;
    height: 900px;
    position: absolute;
    top: 0px;
    left: 0px;
    z-index: 0;
}
* {
    margin: 0px;
    font-weight: normal;
}
a {
    text-decoration: none;
    color: inherit;
}
.text-hidden {
    position: absolute;
    left: -10000px;
    top: auto;
    width: 1pt;
    height: 1px;
    overflow: hidden;
}
.-epub-media-overlay-active {
    color: #DE1717 !important;
    background-color: #f8f012 !important;
}
.-epub-media-overlay-active * {
    color: #DE1717 !important;
    background-color: #f8f012 !important;
}
.para span {
    position: relative;
}
.para {
    position: absolute !important;
    margin-top: 0px;
}
.img_container {
    margin: 0;
    width: 624px;
    height: 900px;
}
""")

    # Write to template.css
    with temp_path.open('w', encoding='utf-8') as f:
        f.write('\n\n'.join(css_content))
    print(f"\n✅ CSS written to: {temp_path}")

# Example usage
if __name__ == "__main__":
    generate_template_css()  # Replace with your actual folder name
