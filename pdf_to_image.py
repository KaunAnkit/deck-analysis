import pymupdf as fitz
import os

def pdf_to_images(pdf_path, output_folder="slides"):

    os.makedirs(output_folder, exist_ok=True)

    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):

        page = doc.load_page(page_num)

        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

        image_path = f"{output_folder}/page_{page_num + 1}.png"

        pix.save(image_path)

        print("Saved:", image_path)


pdf_to_images("fusion_pitch.pdf") 