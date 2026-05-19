from ocr_pdf import ocr_slides
from llm_client import analyze_slide , analyse_slide2
from multiprocessing import Process

import json



def llamaloop():

    slides = ocr_slides()

    all_analysis = []

    for slide in slides:

        image_path = f"slides/{slide['slide']}"

        result = analyze_slide(
            slide["text"],
            image_path
        )

        all_analysis.append({
            "slide": slide["slide"],
            "image_path": image_path,
            "ocr_text": slide["text"],
            "analysis": result
        })
    

    with open("analysis.json", "w", encoding="utf-8") as f:

        json.dump(all_analysis, f, indent=4)

    print("Saved analysis.json")


def geminiloop():

    slides = ocr_slides()

    all_analysis = []

    for slide in slides:

        image_path = f"slides/{slide['slide']}"

        result = analyze_slide2(
            slide["text"],
            image_path
        )

        all_analysis.append({
            "slide": slide["slide"],
            "image_path": image_path,
            "ocr_text": slide["text"],
            "analysis": result
        })
    

    with open("analysis2.json", "w", encoding="utf-8") as f:

        json.dump(all_analysis, f, indent=4)

    print("Saved analysis.json")


if __name__ == '__main__':
    Process(target=llamaloop).start()
    Process(target=geminiloop).start()
