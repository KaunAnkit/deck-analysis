import easyocr
import os

def ocr_slides():

    reader = easyocr.Reader(['en'])

    folder = "slides"

    all_slides_text = []

    for x in sorted(os.listdir(folder)):

        if not x.endswith('.png'):

            continue

        path = os.path.join(folder, x)

        result = reader.readtext(path)

        texts = []

        for y in result:

            text = y[1]
            confidence = y[2]

            if confidence > 0.3:
                texts.append(text)

        slide_text = "\n".join(texts)

        all_slides_text.append({
            "slide": x,
            "text": slide_text
        })
    
    return all_slides_text