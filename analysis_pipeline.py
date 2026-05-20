import json

from pdf_to_image import pdf_to_images
from ocr_pdf import ocr_slides

from image_analysis import describe_slide

from agents.llm_client import analyze_slide
from agents.llm_client2 import analyze_slide_c
from agents.llm_client3 import analyze_slide_d

from deck_judge import judge_deck

from concurrent.futures import ThreadPoolExecutor


PDF_PATH = "fusion_pitch.pdf"


def run_pipeline():

    pdf_to_images(PDF_PATH)

    print("\nPDF conversion done")

    slides = ocr_slides()

    print(f"\nFound {len(slides)} slides")

    analysis_a = []
    analysis_c = []
    analysis_d = []

    for slide in slides:

        image_path = f"slides/{slide['slide']}"

        print(f"\nAnalyzing {slide['slide']}")

        visual_details = describe_slide(
            image_path,
            slide["text"]
        )

        with ThreadPoolExecutor(max_workers=3) as executor:

            future_a = executor.submit(
                analyze_slide,
                slide["text"],
                image_path
            )

            future_c = executor.submit(
                analyze_slide_c,
                slide["text"],
                visual_details
            )

            future_d = executor.submit(
                analyze_slide_d,
                slide["text"],
                visual_details
            )

            result_a = future_a.result()
            result_c = future_c.result()
            result_d = future_d.result()

        analysis_a.append({
            "slide": slide["slide"],
            "analysis": result_a
        })

        analysis_c.append({
            "slide": slide["slide"],
            "analysis": result_c
        })

        analysis_d.append({
            "slide": slide["slide"],
            "analysis": result_d
        })

    with open(
        "analysis_a.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            analysis_a,
            f,
            indent=4,
            ensure_ascii=False
        )

    with open(
        "analysis_c.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            analysis_c,
            f,
            indent=4,
            ensure_ascii=False
        )

    with open(
        "analysis_d.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            analysis_d,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("\nSaved analysis_a.json")
    print("Saved analysis_c.json")
    print("Saved analysis_d.json")

    deck_report = judge_deck(
        analysis_a,
        analysis_c,
        analysis_d
    )

    with open(
        "deck_report.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            deck_report,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("\nSaved deck_report.json")

    return deck_report


if __name__ == "__main__":

    result = run_pipeline()

    print("\nFINAL REPORT\n")

    print(
        json.dumps(
            result,
            indent=4
        )
    )