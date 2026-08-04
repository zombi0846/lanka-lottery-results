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
            res = requests.get(lot["url"], headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')

            draw_no = ""
            date = ""
            letter = ""
            numbers = []

            if lot["board"] == "NLB":
                # NLB Data Scraping
                draw_elem = soup.find(text=re.compile(r'Draw No', re.I))
                if draw_elem:
                    parent = draw_elem.parent.parent if draw_elem.parent else None
                    if parent:
                        draw_no = re.sub(r'\D', '', parent.text)

                date_elem = soup.find('h3') or soup.find('h4')
                if date_elem:
                    date = date_elem.text.strip()

                # Numbers & English Letter
                balls = soup.select('.res-number span, .number-ball, .ball')
                for b in balls:
                    val = b.text.strip()
                    if val.isalpha() and not letter:
                        letter = val
                    elif val.isdigit():
                        numbers.append(val)

            elif lot["board"] == "DLB":
                # DLB Data Scraping
                draw_elem = soup.find(class_=re.compile(r'draw|number', re.I))
                if draw_elem:
                    draw_no = re.sub(r'\D', '', draw_elem.text)

                balls = soup.select('.ball, .res-ball, .number, li')
                for b in balls:
                    val = b.text.strip()
                    if len(val) <= 2 and val.isalpha() and not letter:
                        letter = val
                    elif val.isdigit() and len(val) <= 2:
                        numbers.append(val)

            # Fallback if scraping empty
            if not numbers:
                # Page එකෙන් කෙලින්ම ඉලක්කම් සොයා ගැනීම
                raw_nums = re.findall(r'\b\d{2}\b', res.text)
                if raw_nums:
                    numbers = list(dict.fromkeys(raw_nums))[:4]

            results.append({
                "name": lot["name"],
                "type": lot["type"],
                "board": lot["board"],
                "drawNo": draw_no if draw_no else "N/A",
                "date": date if date else "Latest",
                "letter": letter if letter else "",
                "numbers": numbers,
                "bgGradient": lot["bg"]
            })
            print(f"Fetched {lot['name']}: {draw_no} - {numbers}")

        except Exception as e:
            print(f"Error fetching {lot['name']}: {e}")

    if results:
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print("Updated results.json with real data!")

if __name__ == "__main__":
    fetch_lottery_results()
