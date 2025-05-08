import os
import zipfile
from PyPDF2 import PdfReader, PdfWriter

def split_pdf_to_zip(input_pdf_path, output_zip_path):
    temp_folder = "split_pages"
    os.makedirs(temp_folder, exist_ok=True)

    reader = PdfReader(input_pdf_path)
    total_pages = len(reader.pages)
    print(f"\n🔄 Splitting {total_pages} pages...\n")

    page_paths = []
    for i in range(total_pages):
        writer = PdfWriter()
        writer.add_page(reader.pages[i])

        filename = f"page_{i+1}.pdf"
        filepath = os.path.join(temp_folder, filename)

        with open(filepath, "wb") as f:
            writer.write(f)
        page_paths.append(filepath)

        # ✅ Show progress
        print(f"✅ Saved page {i+1} of {total_pages}")

    print("\n📦 Zipping pages...")
    with zipfile.ZipFile(output_zip_path, "w") as zipf:
        for file_path in page_paths:
            zipf.write(file_path, os.path.basename(file_path))

    print(f"\n✅ Created ZIP: {output_zip_path}")

    # Cleanup
    for file_path in page_paths:
        os.remove(file_path)
    os.rmdir(temp_folder)

    print("🧹 Temporary files cleaned up.")

input_pdf = "input.pdf"  # Replace with actual file name
output_zip = "split_pages_output.zip"

split_pdf_to_zip(input_pdf, output_zip)
