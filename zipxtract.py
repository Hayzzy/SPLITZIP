import zipfile
import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import json

def extract_ocr_from_zip(zip_path, output_json):
    temp_dir = "unzipped_scanned"
    os.makedirs(temp_dir, exist_ok=True)

    # Unzip the PDFs
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    files = sorted([f for f in os.listdir(temp_dir) if f.endswith(".pdf")])
    total_files = len(files)
    page_data = {}

    print(f"🟡 Starting OCR for {total_files} scanned PDFs...\n")

    for idx, filename in enumerate(files, 1):
        pdf_path = os.path.join(temp_dir, filename)
        doc = fitz.open(pdf_path)
        text = ""

        for page_num, page in enumerate(doc):
            pix = page.get_pixmap(dpi=150) #change wrt payload (pdf size)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            ocr_text = pytesseract.image_to_string(img)
            text += ocr_text

        page_id = filename.replace(".pdf", "")
        page_data[f"Page {page_id}"] = text.strip()

        percent = round((idx / total_files) * 100)
        print(f"✅ Processed {filename} ({percent}%)")

    # Save to JSON
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(page_data, f, indent=4, ensure_ascii=False)

    print(f"\n🎉 Done! OCR results saved to: {output_json}")

# === USAGE ===
zip_path = "split_pages_output.zip"   # Your zipped PDFs
output_json = "output.json"

extract_ocr_from_zip(zip_path, output_json)
