import json
from collections import defaultdict
from pathlib import Path

def group_words_into_paragraphs(pdf_name, target_width=696, target_height=900, original_width=612, original_height=792):
    project_dir = Path("project") / pdf_name
    merged_word_data_path = project_dir / "merged_word_data.json"
    output_json_path = project_dir / "grouped_paragraphs.json"

    # Load merged word data
    with open(merged_word_data_path, "r", encoding="utf-8") as f:
        merged_word_data = json.load(f)

    paragraphs = defaultdict(list)
    current_paragraph = []
    last_bottom = None
    last_page = None

    for word in sorted(merged_word_data, key=lambda w: (w["page"], w["top"], w["x0"])):
        page = word["page"]
        top = word["top"]
        bottom = word["bottom"]

        # Check if the word belongs to the same paragraph
        if last_page is not None and (page != last_page or (last_bottom is not None and top > last_bottom + 10)):
            # Save the current paragraph and start a new one
            paragraphs[last_page].append(current_paragraph)
            current_paragraph = []

        current_paragraph.append(word)
        last_bottom = bottom
        last_page = page

    # Add the last paragraph
    if current_paragraph:
        paragraphs[last_page].append(current_paragraph)

    # Save grouped paragraphs as JSON
    with open(output_json_path, "w", encoding="utf-8") as json_file:
        json.dump(paragraphs, json_file, indent=4)

    print(f"Grouped paragraphs saved to {output_json_path}")
    return output_json_path




