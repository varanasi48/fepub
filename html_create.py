import os

def generate_html(page_number, words):
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Page {page_number}</title>
  <meta name="viewport" content="width=624, height=900, user-scalable=no">
  <style>
    body {{
      margin: 0;
      width: 100vw;
      height: 100vh;
      overflow: hidden;
      background: #fff;
      font-family: sans-serif;
    }}
    .page {{
      position: relative;
      width: 612px;
      height: 792px;
      transform: scale(1.02); /* adjust if needed */
      transform-origin: top left;
    }}
    .word {{
      position: absolute;
      font-size: 10px;
      white-space: nowrap;
    }}
  </style>
</head>
<body>
  <div class="page">
    {"".join([f"<div class='word' style='left:{w['x']}px; top:{w['y']}px;'>{w['text']}</div>" for w in words])}
  </div>
</body>
</html>
"""
    output_path = f"project/html/page_{page_number}.html"
    os.makedirs("project", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"[✓] Created HTML: {output_path}")
