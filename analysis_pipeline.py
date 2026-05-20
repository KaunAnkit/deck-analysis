import json

from pdf_to_image import pdf_to_images
from ocr_pdf import ocr_slides
from llm_client import analyze_slide, analyse_slide2
from deck_judge import judge_deck


PDF_PATH = "fusion_pitch.pdf"


def run_pipeline():

    pdf_to_images(PDF_PATH)

    print("\nPDF conversion done")

    slides = ocr_slides()

    print(f"\nFound {len(slides)} slides")


    all_analysis = []

    for slide in slides:

        image_path = f"slides/{slide['slide']}"

        print(f"\nAnalyzing {slide['slide']}")

        llama_analysis = analyze_slide(slide["text"], image_path)
        gemini_analysis = analyse_slide2(slide["text"], image_path)

        all_analysis.append({
            "slide": slide["slide"],
            "image_path": image_path,
            "ocr_text": slide["text"],
            "llama_analysis": llama_analysis,
            "gemini_analysis": gemini_analysis
        })

    with open(
        "analysis.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            all_analysis,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("\nSaved analysis.json agents work done")


    compressed_analysis = [
        {
            "slide": slide["slide"],
            "llama": slide["llama_analysis"],
            "gemini": slide["gemini_analysis"]
        }
        for slide in all_analysis
    ]

    deck_report = judge_deck(
        compressed_analysis
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