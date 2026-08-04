import json
import requests
from bs4 import BeautifulSoup
import re

def fetch_lottery_results():
    results = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    # ලංකාවේ ප්‍රධාන ලොතරැයි ලැයිස්තුව
    lotteries = [
        # --- National Lotteries Board (NLB) ---
        {"name": "මහජන සම්පත", "type": "mahajana", "board": "NLB", "url": "https://www.nlb.lk/English/results/mahajana-sampatha", "bg": "from-blue-900 to-indigo-800"},
        {"name": "ගොවිසෙත", "type": "govisetha", "board": "NLB", "url": "https://www.nlb.lk/English/results/govisetha", "bg": "from-rose-900 to-pink-800"},
        {"name": "මෙගා පවර්", "type": "mega-power", "board": "NLB", "url": "https://www.nlb.lk/English/results/mega-power", "bg": "from-amber-900 to-yellow-800"},
        {"name": "ධන නිධානය", "type": "dhana-nidhanaya", "board": "NLB", "url": "https://www.nlb.lk/English/results/dhana-nidhanaya", "bg": "from-emerald-900 to-teal-800"},
        {"name": "වාසනාවේ සැඳෑව", "type": "wasana-sada", "board": "NLB", "url": "https://www.nlb.lk/English/results/handahana", "bg": "from-purple-900 to-violet-800"},
        {"name": "සුපිරි වාසනා", "type": "supiri-wasana", "board": "NLB", "url": "https://www.nlb.lk/English/results/supiri-wasana", "bg": "from-cyan-900 to-blue-800"},

        # --- Development Lotteries Board (DLB) ---
        {"name": "ශනිදා වාසනාව", "type": "shanida", "board": "DLB", "url": "https://www.dlb.lk/results/shanida-wasanawa", "bg": "from-purple-900 to-indigo-900"},
        {"name": "ලග්න වාසනාව", "type": "lagna-wasanawa", "board": "DLB", "url": "https://www.dlb.lk/results/lagna-wasanawa", "bg": "from-orange-900 to-red-800"},
        {"name": "කෝටිපති කප්රුක", "type": "kotipathi-kapruka", "board": "DLB", "url": "https://www.dlb.lk/results/kotipathi-kapruka", "bg": "from-green-900 to-emerald-800"},
        {"name": "ජයෝදා", "type": "jayoda", "board": "DLB", "url": "https://www.dlb.lk/results/jayoda", "bg": "from-fuchsia-900 to-pink-900"},
        {"name": "අද කෝටිපති", "type": "ada-kotipathi", "board": "DLB", "url": "https://www.dlb.lk/results/ada-kotipathi", "bg": "from-indigo-900 to-blue-900"}
    ]

    for lot in lotteries:
        try:
            res = requests.get(lot["url"], headers=headers, timeout=12)
            soup = BeautifulSoup(res.text, 'html.parser')

            draw_no = ""
            date = ""
            letter = ""
            numbers = []

            # General parsing logic for draw number & date
            text_content = soup.get_text()
            
            # Find Draw Number
            draw_match = re.search(r'(?:Draw|Draw No|වර|වාරය)\s*[:.-]?\s*(\d+)', text_content, re.I)
            if draw_match:
                draw_no = draw_match.group(1)

            # Find Date
            date_match = re.search(r'\b(20\d{2}[-/.]\d{1,2}[-/.]\d{1,2})\b', text_content)
            if date_match:
                date = date_match.group(1)

            # Extract numbers and letters from specific tags/lists
            spans = soup.find_all(['span', 'div', 'li', 'td'])
            for s in spans:
                txt = s.text.strip()
                if len(txt) == 1 and txt.isalpha() and not letter:
                    letter = txt
                elif txt.isdigit() and 1 <= len(txt) <= 2 and txt not in numbers:
                    # Exclude draw number from numbers list
                    if txt != draw_no:
                        numbers.append(txt)

            # Keep only the first 4-5 winning numbers
            numbers = numbers[:4] if len(numbers) >= 4 else numbers

            results.append({
                "name": lot["name"],
                "type": lot["type"],
                "board": lot["board"],
                "drawNo": draw_no if draw_no else "N/A",
                "date": date if date else "Latest",
                "letter": letter if letter else "-",
                "numbers": numbers if numbers else ["-", "-", "-", "-"],
                "bgGradient": lot["bg"]
            })
            print(f"Fetched {lot['name']}: {draw_no} - {letter} {numbers}")

        except Exception as e:
            print(f"Error fetching {lot['name']}: {e}")

    if results:
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print("Scraping finished!")

if __name__ == "__main__":
    fetch_lottery_results()
