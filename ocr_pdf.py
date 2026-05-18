import easyocr
import os

reader = easyocr.Reader(['en'])

slides_folder = "slides"

all_slides_text = []

for filename in os.listdir(slides_folder):

    path = os.path.join(slides_folder, filename)

    result = reader.readtext(path)

    texts = []

    for detection in result:

        text = detection[1]
        confidence = detection[2]

        if confidence > 0.3:
            texts.append(text)

    slide_text = "\n".join(texts)

    all_slides_text.append({
        "slide": filename,
        "text": slide_text
    })

print(all_slides_text)