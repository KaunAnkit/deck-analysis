import pymupdf as fitz
import os
import shutil

def pdf_to_images(pdf_path, output_folder="slides"):
    
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    os.makedirs(output_folder)

    doc = fitz.open(pdf_path)

    for x in range(len(doc)):

        page = doc.load_page(x)

        pix = page.get_pixmap(matrix=fitz.Matrix(1.2, 1.2))

        path = f"{output_folder}/page_{x + 1}.png"

        pix.save(path)

    doc.close()