import json
import re
from playwright.sync_api import sync_playwright

def fetch_lottery_results():
    results = []
    
    lotteries = [
        # --- NLB ---
        {"name": "මහජන සම්පත", "type": "mahajana", "board": "NLB", "url": "https://www.nlb.lk/English/results/mahajana-sampatha", "bg": "from-blue-900 to-indigo-800"},
        {"name": "ගොවිසෙත", "type": "govisetha", "board": "NLB", "url": "https://www.nlb.lk/English/results/govisetha", "bg": "from-rose-900 to-pink-800"},
        {"name": "මෙගා පවර්", "type": "mega-power", "board": "NLB", "url": "https://www.nlb.lk/English/results/mega-power", "bg": "from-amber-900 to-yellow-800"},
        {"name": "ධන නිධානය", "type": "dhana-nidhanaya", "board": "NLB", "url": "https://www.nlb.lk/English/results/dhana-nidhanaya", "bg": "from-emerald-900 to-teal-800"},
        {"name": "වාසනාවේ සැඳෑව", "type": "wasana-sada", "board": "NLB", "url": "https://www.nlb.lk/English/results/handahana", "bg": "from-purple-900 to-violet-800"},
        {"name": "සුපිරි වාසනා", "type": "supiri-wasana", "board": "NLB", "url": "https://www.nlb.lk/English/results/supiri-wasana", "bg": "from-cyan-900 to-blue-800"},

        # --- DLB ---
        {"name": "ශනිදා වාසනාව", "type": "shanida", "board": "DLB", "url": "https://www.dlb.lk/results/shanida-wasanawa", "bg": "from-purple-900 to-indigo-900"},
        {"name": "ලග්න වාසනාව", "type": "lagna-wasanawa", "board": "DLB", "url": "https://www.dlb.lk/results/lagna-wasanawa", "bg": "from-orange-900 to-red-800"},
        {"name": "කෝටිපති කප්රුක", "type": "kotipathi-kapruka", "board": "DLB", "url": "https://www.dlb.lk/results/kotipathi-kapruka", "bg": "from-green-900 to-emerald-800"},
        {"name": "ජයෝදා", "type": "jayoda", "board": "DLB", "url": "https://www.dlb.lk/results/jayoda", "bg": "from-fuchsia-900 to-pink-900"},
        {"name": "අද කෝටිපති", "type": "ada-kotipathi", "board": "DLB", "url": "https://www.dlb.lk/results/ada-kotipathi", "bg": "from-indigo-900 to-blue-900"}
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for lot in lotteries:
            try:
                page.goto(lot["url"], timeout=30000, wait_until="domcontentloaded")
                page.wait_for_timeout(2000)

                content = page.content()
                text = page.inner_text('body')

                draw_no = "N/A"
                date = "Latest"
                letter = ""
                numbers = []

                # Draw Number & Date Matching
                draw_match = re.search(r'(?:Draw No|Draw|වාරය)\s*[:.-]?\s*(\d+)', text, re.I)
                if draw_match:
                    draw_no = draw_match.group(1)

                date_match = re.search(r'\b(20\d{2}[-/.]\d{1,2}[-/.]\d{1,2})\b', text)
                if date_match:
                    date = date_match.group(1)

                # Numbers Extraction via Page Elements
                elements = page.query_selector_all('span, div, li')
                for elem in elements:
                    t = elem.inner_text().strip()
                    if len(t) == 1 and t.isalpha() and not letter:
                        letter = t
                    elif t.isdigit() and 1 <= len(t) <= 2 and t != draw_no and t not in numbers:
                        numbers.append(t)

                numbers = numbers[:4]

                results.append({
                    "name": lot["name"],
                    "type": lot["type"],
                    "board": lot["board"],
                    "drawNo": draw_no,
                    "date": date,
                    "letter": letter if letter else "-",
                    "numbers": numbers if numbers else ["-", "-", "-", "-"],
                    "bgGradient": lot["bg"]
                })
                print(f"Scraped {lot['name']}: Draw {draw_no} | Letter {letter} | Nums {numbers}")

            except Exception as e:
                print(f"Error loading {lot['name']}: {e}")

        browser.close()

    if results:
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print("Scraping with Playwright finished!")

if __name__ == "__main__":
    fetch_lottery_results()
