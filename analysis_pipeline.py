import json
import os

from concurrent.futures import ThreadPoolExecutor

from pdf_to_image import pdf_to_images
from ocr_pdf import ocr_slides
from image_analysis import describe_slide

from agents.llm_client import analyze_slide
from agents.llm_client2 import analyze_slide_c
from agents.llm_client3 import analyze_slide_d

from deck_judge import judge_deck

REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)


def compress_analysis(analysis_list):

    compressed = []

    for x in analysis_list:

        a = x.get("analysis", {})

        compressed.append({
            "type": a.get("slide_type", ""),
            "score": a.get("overall_score", 0),
            "strengths": a.get("strengths", [])[:2],
            "weaknesses": a.get("weaknesses", [])[:2],
            "concerns": a.get("investor_concerns", [])[:2]
        })

    return compressed


def run_pipeline(pdf_path, deck_context):

    pdf_to_images(pdf_path)

    print("PDF conversion done")

    slides = ocr_slides()

    print(f"\nFound {len(slides)} slides")

    analysis_a = []
    analysis_c = []
    analysis_d = []

    for slide in slides:

        image_path = f"slides/{slide['slide']}"

        visual_details = describe_slide(
            image_path,
            slide["text"]
        )

        with ThreadPoolExecutor(max_workers=3) as executor:

            future_a = executor.submit(
                analyze_slide,
                slide["text"],
                image_path,
                deck_context
            )

            future_c = executor.submit(
                analyze_slide_c,
                slide["text"],
                visual_details,
                deck_context
            )

            future_d = executor.submit(
                analyze_slide_d,
                slide["text"],
                visual_details,
                deck_context
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

    print("\nAnalyzed all slides")

    with open(f"{REPORT_DIR}/analysis_a.json", "w", encoding="utf-8") as f:
        json.dump(analysis_a, f, ensure_ascii=False)

    with open(f"{REPORT_DIR}/analysis_c.json", "w", encoding="utf-8") as f:
        json.dump(analysis_c, f, ensure_ascii=False)

    with open(f"{REPORT_DIR}/analysis_d.json", "w", encoding="utf-8") as f:
        json.dump(analysis_d, f, ensure_ascii=False)

    print("\nSaved analysis_a.json")
    print("Saved analysis_c.json")
    print("Saved analysis_d.json")

    deck_report = judge_deck(
        compress_analysis(analysis_a),
        compress_analysis(analysis_c),
        compress_analysis(analysis_d),
        deck_context
    )

    with open(f"{REPORT_DIR}/deck_report.json", "w", encoding="utf-8") as f:
        json.dump(deck_report, f, indent=4, ensure_ascii=False)

    print("\nSaved deck_report.json")

    return deck_report


if __name__ == "__main__":

    sample_context = {
        "deck_goal": "investor_meeting",
        "deck_type": "pitch",
        "fund_size": "$2M",
        "growth_focus": "international",
        "deck_timeline": "within_1_month"
    }

    result = run_pipeline(
        "sample.pdf",
        sample_context
    )

    print("\nFINAL REPORT\n")
    print(json.dumps(result, indent=4))