import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from pdf_pick import pick_pdf_and_save
from mark_special_pages import mark_special_pages
from generate_coords import extract_text_coordinates
from extract_fonts import extract_fonts_and_text_details
from paragraph import group_words_into_paragraphs
from generate_css import generate_paragraph_css
from align import generate_html_pages_with_text
from merge_text_and_font_data import merge_text_and_font_data
from generate_template_css import generate_template_css  # Import for template.css generation


def process_pdf(pdf_name, status_label, finish_button):
    def update_status(text):
        status_label.config(text=text)
        status_label.update_idletasks()

    update_status(f"Processing: {pdf_name}")

    # Step 1: Pick file
    update_status("Picking file...")
    pdf_path = pick_pdf_and_save()

    # Step 2: Mark special pages
  #  update_status("Marking special pages...")
  #  mark_special_pages(pdf_path)

    # Step 3: Extract text coordinates
    update_status("Extracting text coordinates...")
    extract_text_coordinates(pdf_path)

    # Step 4: Extract fonts
    update_status("Extracting fonts...")
    extract_fonts_and_text_details(pdf_path)

    # Step 5: Merge text and font data
    update_status("Merging text and font data...")
    merge_text_and_font_data(pdf_path)

    # Step 6: Group words into paragraphs
    update_status("Grouping words into paragraphs...")
    grouped_paragraphs_json_path = group_words_into_paragraphs(pdf_name)

    # Step 7: Generate template.css
    

    # Step 8: Generate CSS
    update_status("Generating CSS...")
    generate_paragraph_css(pdf_name)

    update_status("Generating template.css...")
    generate_template_css(pdf_name)

    # Step 9: Generate HTML
    update_status("Generating HTML...")
    generate_html_pages_with_text(pdf_name)

    update_status("✅ Processing completed.")
    finish_button.pack(pady=10)  # Show the finish button


def start_pipeline(status_label, finish_button):
    pdf_name = pick_pdf_and_save()
    if pdf_name:
        process_pdf(pdf_name, status_label, finish_button)
        messagebox.showinfo("Success", f"Processing of {pdf_name} completed.")
    else:
        messagebox.showwarning("Cancelled", "No file was selected.")


def main():
    root = tk.Tk()
    root.title("PDF Processor")

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack()

    process_button = tk.Button(frame, text="Select and Process PDF", width=30)
    process_button.pack(pady=10)

    status_label = tk.Label(frame, text="Waiting for PDF...", fg="blue")
    status_label.pack(pady=10)

    finish_button = tk.Button(frame, text="Finish and Exit", command=lambda: root.destroy())

    # Bind function with required arguments
    process_button.config(command=lambda: start_pipeline(status_label, finish_button))

    root.mainloop()


if __name__ == "__main__":
    main()
