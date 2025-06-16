import streamlit as st
import sys
from pathlib import Path
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from io import BytesIO
import json

def load_pdf_page_image(pdf_path, page_number):
    images = convert_from_path(
        pdf_path,
        first_page=page_number,
        last_page=page_number,
        fmt='png'
    )
    img_byte_arr = BytesIO()
    images[0].save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

def mark_special_pages(pdf_name):
    """
    Streamlit app: display a single page from PDF as image (converted in memory),
    with dropdown to assign label, and save to JSON.
    """
    project_dir = Path("project") / pdf_name
    pdf_path = project_dir / "pdf" / f"{pdf_name}.pdf"

    if not pdf_path.exists():
        st.error(f"PDF file not found: {pdf_path}")
        st.stop()

    reader = PdfReader(str(pdf_path))
    num_pages = len(reader.pages)

    st.title("📑 Mark Special Pages")

    col1, col2 = st.columns([2, 1])

    with col2:
        st.write("### Select a Page and Label")
        selected_page_index = st.selectbox("Select Page", list(range(1, num_pages + 1)))  # Page numbers start from 1
        selected_label = st.selectbox("Select Label", [
            "Front Cover",
            "Inside Front Cover",
            "Inside Back Cover",
            "Back Cover",
            "Table of Contents"
        ])

        if st.button("➕ Mark Page"):
            selection_path = project_dir / "special_pages_selection.json"
            selection = {"page": f"Page {selected_page_index}", "label": selected_label}

            if selection_path.exists():
                with open(selection_path, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
            else:
                existing_data = []

            existing_data.append(selection)

            with open(selection_path, "w", encoding="utf-8") as f:
                json.dump(existing_data, f, indent=2)

            st.success(f"✅ Page {selected_page_index} marked as {selected_label}")

        if st.button("✅ Done"):
            with open("streamlit_done.signal", "w") as f:
                f.write("done")
            st.success("✅ Marking completed. You can now close this window.")

    with col1:
        st.write(f"### Preview: Page {selected_page_index}")
        try:
            img_bytes = load_pdf_page_image(str(pdf_path), selected_page_index)
            st.image(img_bytes, use_column_width=True)
        except Exception as e:
            st.error(f"Error rendering page image: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pdf_name = sys.argv[-1]
    else:
        st.error("❌ PDF name argument missing.")
        st.stop()

    mark_special_pages(pdf_name)
