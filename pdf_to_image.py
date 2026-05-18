import pymupdf as fitz
import os

def pdf_to_images(pdf_path, output_folder="slides"):

    os.makedirs(output_folder, exist_ok=True)

    doc = fitz.open(pdf_path)

    for x in range(len(doc)):

        page = doc.load_page(x)

        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

        path = f"{output_folder}/page_{x + 1}.png"

        pix.save(path)

        print("Saved:", path)


pdf_to_images("fusion_pitch.pdf") 