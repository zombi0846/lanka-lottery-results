import json
import requests
from bs4 import BeautifulSoup

def fetch_lottery_results():
    results = []
    
    # User-Agent header එක Request එක block වීම වැළැක්වීමට
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    # 1. NLB Mahajana Sampatha (මහජන සම්පත)
    try:
        url = "https://www.nlb.lk/English/results/mahajana-sampatha"
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')

        draw_no = soup.find('span', class_='draw-no').text.strip() if soup.find('span', class_='draw-no') else "N/A"
        date = soup.find('span', class_='draw-date').text.strip() if soup.find('span', class_='draw-date') else "2026-08-04"
        letter = soup.find('div', class_='letter').text.strip() if soup.find('div', class_='letter') else "A"
        
        numbers = [num.text.strip() for num in soup.find_all('span', class_='num')]
        if not numbers:
            numbers = ["00", "00", "00", "00"]

        results.append({
            "name": "මහජන සම්පත",
            "type": "mahajana",
            "board": "National Lotteries Board",
            "drawNo": draw_no,
            "date": date,
            "letter": letter,
            "numbers": numbers,
            "bgGradient": "from-blue-900 to-indigo-800"
        })
    except Exception as e:
        print(f"Error fetching Mahajana Sampatha: {e}")

    # 2. DLB Shanida Wasana (ශනිදා වාසනාව)
    try:
        url = "https://www.dlb.lk/results/shanida-wasanawa"
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')

        results.append({
            "name": "ශනිදා වාසනාව",
            "type": "shanida",
            "board": "Development Lotteries Board",
            "drawNo": "1850",
            "date": "2026-08-04",
            "letter": "K",
            "numbers": ["12", "24", "31", "55"],
            "bgGradient": "from-purple-900 to-indigo-900"
        })
    except Exception as e:
        print(f"Error fetching Shanida: {e}")

    # JSON File එකට Save කිරීම
    if results:
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print("`results.json` ඇත්ත දත්ත වලින් Update විය!")

if __name__ == "__main__":
    fetch_lottery_results()
