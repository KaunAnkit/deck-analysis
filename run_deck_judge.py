import json

from deck_judge import judge_deck

with open("analysis.json", "r", encoding="utf-8") as f:
    analysis = json.load(f)

compressed_analysis = [
    slide["analysis"]
    for slide in analysis
]

result = judge_deck(compressed_analysis)

print(json.dumps(result, indent=4))

with open("deck_report.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4)

print("\nSaved deck_report.json")