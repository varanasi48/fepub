import shutil
from tkinter import Tk, filedialog
from pathlib import Path

def pick_pdf_and_save():
    # Create a hidden Tkinter root window
    root = Tk()
    root.withdraw()

    # File picker dialog - restrict to PDF files
    file_path = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF files", "*.pdf")]
    )

    if not file_path:
        print("No file selected.")
        return None

    # Get file name and name without extension
    pdf_path = Path(file_path)
    file_name = pdf_path.name
    file_stem = pdf_path.stem

    # Create destination directory
    dest_dir = Path("project")/ file_stem
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Destination file path
    dest_file_path = dest_dir / "pdf" / file_name

    # Create 'pdf' subfolder
    (dest_dir / "pdf").mkdir(parents=True, exist_ok=True)

    # Copy file to 'pdf' subfolder
    shutil.copy(pdf_path, dest_file_path)

    print(f"PDF saved to: {dest_file_path}")
    
    # Return folder name (e.g., "Y65893_BK") for downstream usage
    return file_stem
