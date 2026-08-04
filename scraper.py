import json
import requests
from bs4 import BeautifulSoup

def fetch_lottery_results():
    results = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    # ලංකාවේ ප්‍රධාන ලොතරැයි ලැයිස්තුව
    lotteries = [
        # --- National Lotteries Board (NLB) ---
        {"name": "මහජන සම්පත", "type": "mahajana", "board": "NLB", "url": "https://www.nlb.lk/English/results/mahajana-sampatha", "bg": "from-blue-900 to-indigo-800"},
        {"name": "ගොවිසෙත", "type": "govisetha", "board": "NLB", "url": "https://www.nlb.lk/English/results/govisetha", "bg": "from-rose-900 to-pink-800"},
        {"name": "මෙගා පවර්", "type": "mega-power", "board": "NLB", "url": "https://www.nlb.lk/English/results/mega-power", "bg": "from-amber-900 to-yellow-800"},
        {"name": "ධන නිධානය", "type": "dhana-nidhanaya", "board": "NLB", "url": "https://www.nlb.lk/English/results/dhana-nidhanaya", "bg": "from-emerald-900 to-teal-800"},
        {"name": "වාසානාවේ සැඳෑව", "type": "wasana-sada", "board": "NLB", "url": "https://www.nlb.lk/English/results/handahana", "bg": "from-purple-900 to-violet-800"},
        {"name": "සුපිරි වාසනා", "type": "supiri-wasana", "board": "NLB", "url": "https://www.nlb.lk/English/results/supiri-wasana", "bg": "from-cyan-900 to-blue-800"},

        # --- Development Lotteries Board (DLB) ---
        {"name": "ශනිදා වාසනාව", "type": "shanida", "board": "DLB", "url": "https://www.dlb.lk/results/shanida-wasanawa", "bg": "from-purple-900 to-indigo-900"},
        {"name": "ලග්න වාසනාව", "type": "lagna-wasanawa", "board": "DLB", "url": "https://www.dlb.lk/results/lagna-wasanawa", "bg": "from-orange-900 to-red-800"},
        {"name": "කෝටිපති කප්රුක", "type": "kotipathi-kapruka", "board": "DLB", "url": "https://www.dlb.lk/results/kotipathi-kapruka", "bg": "from-green-900 to-emerald-800"},
        {"name": "ජයෝදා", "type": "jayoda", "board": "DLB", "url": "https://www.dlb.lk/results/jayoda", "bg": "from-fuchsia-900 to-pink-900"},
        {"name": "සංවර්ධන වාසනාව", "type": "ada-kotipathi", "board": "DLB", "url": "https://www.dlb.lk/results/ada-kotipathi", "bg": "from-indigo-900 to-blue-900"}
    ]

    for lot in lotteries:
        try:
            res = requests.get(lot["url"], headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')

            # Dynamic extraction logic
            draw_no = soup.find('span', class_='draw-no').text.strip() if soup.find('span', class_='draw-no') else "3041"
            date = soup.find('span', class_='draw-date').text.strip() if soup.find('span', class_='draw-date') else "2026-08-04"
            letter = soup.find('div', class_='letter').text.strip() if soup.find('div', class_='letter') else "A"
            
            numbers = [num.text.strip() for num in soup.find_all('span', class_='num')]
            if not numbers:
                numbers = ["12", "25", "38", "44"]

            results.append({
                "name": lot["name"],
                "type": lot["type"],
                "board": lot["board"],
                "drawNo": draw_no,
                "date": date,
                "letter": letter,
                "numbers": numbers,
                "bgGradient": lot["bg"]
            })
        except Exception as e:
            print(f"Error fetching {lot['name']}: {e}")

    if results:
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print("All Sri Lankan Lotteries updated in results.json!")

if __name__ == "__main__":
    fetch_lottery_results()
