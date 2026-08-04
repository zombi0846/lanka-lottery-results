import json
import requests
from bs4 import BeautifulSoup

def fetch_lottery_results():
    results = []

    # 1. Sample NLB Data Fetching Logic (Mahajana Sampatha)
    # (NLB/DLB වෙබ් අඩවිවල අලුත්ම results page එකෙන් data scrap කිරීම)
    try:
        # මෙතනට NLB/DLB site එකෙන් scrap කරන data dynamic ලෙස එකතු වෙනවා
        results = [
            {
                "name": "මහජන සම්පත",
                "type": "mahajana",
                "board": "National Lotteries Board",
                "drawNo": "3042",
                "date": "2026-08-04",
                "letter": "B",
                "numbers": ["05", "18", "29", "42"],
                "bgGradient": "from-blue-900 to-indigo-800"
            },
            {
                "name": "ශනිදා වාසනාව",
                "type": "shanida",
                "board": "Development Lotteries Board",
                "drawNo": "1850",
                "date": "2026-08-04",
                "letter": "K",
                "numbers": ["12", "24", "31", "55"],
                "bgGradient": "from-purple-900 to-indigo-900"
            },
            {
                "name": "ගොවිසෙත",
                "type": "govisetha",
                "board": "National Lotteries Board",
                "drawNo": "2210",
                "date": "2026-08-04",
                "letter": "H",
                "numbers": ["02", "14", "20", "39"],
                "bgGradient": "from-rose-900 to-pink-800"
            }
        ]

        # results.json file එකට auto-write කිරීම
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print("`results.json` සාර්ථකව Update විය!")

    except Exception as e:
        print(f"Error updating results: {e}")

if __name__ == "__main__":
    fetch_lottery_results()