import json
import requests

def fetch_lottery_results():
    results = []
    
    # Custom headers to bypass bot blocks
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.nlb.lk/'
    }

    lotteries = [
        # --- NLB ---
        {"name": "මහජන සම්පත", "type": "mahajana", "board": "NLB", "id": "1", "bg": "from-blue-900 to-indigo-800"},
        {"name": "ගොවිසෙත", "type": "govisetha", "board": "NLB", "id": "2", "bg": "from-rose-900 to-pink-800"},
        {"name": "මෙගා පවර්", "type": "mega-power", "board": "NLB", "id": "11", "bg": "from-amber-900 to-yellow-800"},
        {"name": "ධන නිධානය", "type": "dhana-nidhanaya", "board": "NLB", "id": "7", "bg": "from-emerald-900 to-teal-800"},
        {"name": "වාසනාවේ සැඳෑව", "type": "wasana-sada", "board": "NLB", "id": "5", "bg": "from-purple-900 to-violet-800"},
        {"name": "සුපිරි වාසනා", "type": "supiri-wasana", "board": "NLB", "id": "3", "bg": "from-cyan-900 to-blue-800"},

        # --- DLB ---
        {"name": "ශනිදා වාසනාව", "type": "shanida", "board": "DLB", "id": "2", "bg": "from-purple-900 to-indigo-900"},
        {"name": "ලග්න වාසනාව", "type": "lagna-wasanawa", "board": "DLB", "id": "3", "bg": "from-orange-900 to-red-800"},
        {"name": "කෝටිපති කප්රුක", "type": "kotipathi-kapruka", "board": "DLB", "id": "12", "bg": "from-green-900 to-emerald-800"},
        {"name": "ජයෝදා", "type": "jayoda", "board": "DLB", "id": "5", "bg": "from-fuchsia-900 to-pink-900"},
        {"name": "අද කෝටිපති", "type": "ada-kotipathi", "board": "DLB", "id": "10", "bg": "from-indigo-900 to-blue-900"}
    ]

    session = requests.Session()

    for lot in lotteries:
        try:
            draw_no = "N/A"
            date = "Latest"
            letter = ""
            numbers = []

            if lot["board"] == "NLB":
                url = f"https://www.nlb.lk/English/results/get-latest-result/{lot['id']}"
                res = session.get(url, headers=headers, timeout=10)
                if res.status_code == 200:
                    data = res.json()
                    draw_no = str(data.get('draw_number', 'N/A'))
                    date = str(data.get('draw_date', 'Latest'))
                    letter = str(data.get('letter', ''))
                    
                    # Extract winning numbers
                    raw_nums = data.get('numbers', [])
                    if isinstance(raw_nums, list):
                        numbers = [str(n) for n in raw_nums]
                    elif isinstance(raw_nums, dict):
                        numbers = [str(v) for v in raw_nums.values()]

            elif lot["board"] == "DLB":
                url = f"https://www.dlb.lk/api/get-latest-result?lottery_id={lot['id']}"
                res = session.get(url, headers=headers, timeout=10)
                if res.status_code == 200:
                    data = res.json()
                    draw_no = str(data.get('draw_no', 'N/A'))
                    date = str(data.get('draw_date', 'Latest'))
                    letter = str(data.get('letter', ''))
                    numbers = [str(n) for n in data.get('winning_numbers', [])]

            results.append({
                "name": lot["name"],
                "type": lot["type"],
                "board": lot["board"],
                "drawNo": draw_no,
                "date": date,
                "letter": letter,
                "numbers": numbers if numbers else ["-", "-", "-", "-"],
                "bgGradient": lot["bg"]
            })
            print(f"Success: {lot['name']} -> {draw_no} | {letter} | {numbers}")

        except Exception as e:
            print(f"Error fetching {lot['name']}: {e}")

    if results:
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print("Scraping completed!")

if __name__ == "__main__":
    fetch_lottery_results()
