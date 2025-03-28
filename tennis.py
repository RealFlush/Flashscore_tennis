import requests
from bs4 import BeautifulSoup
import re
import time


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_match_links():
    """�������� ������ ������ �� ����� � flashscore.mobi"""
    url = "https://www.flashscore.mobi/tennis/?d=0"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # ������� ��� ������ �� �����
        match_links = []
        for match in soup.find_all('a', href=re.compile(r'/match/')):
            match_id = match['href'].split('/')[-2]  # ��������� ID �����
            if match_id:
                match_url = f"https://www.flashscore.com/match/tennis/{match_id}/#/match-summary"
                match_links.append(match_url)
        
        return match_links
    except Exception as e:
        print(f"������ ��� ��������� ������ ������: {e}")
        return []

def parse_match_page(url):
    """������ �������� ����� �� flashscore.com"""
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        
        
        # ��������� �������
        og_title = soup.find('meta', property='og:title')
        if og_title:
            players = og_title['content'].split(' - ')
            player1, player2 = players[0], players[1] if len(players) > 1 else 'N/A'
        else:
            player1, player2 = 'N/A', 'N/A'
        
        # ��������� ������
        og_desc = soup.find('meta', property='og:description')
        tournament = og_desc['content'] if og_desc else 'N/A'
        
        # ��������� ����� ������
        start_time = ''
        
        return {
            'start_time': start_time,
            'tournament': tournament,
            'player1': player1,
            'player2': player2,
            'url': url
        }
    except Exception as e:
        print(f"������ ��� �������� {url}: {str(e)[:100]}...")
        return None

def main():
    print("������� ������ ������...")
    matches = get_match_links()
    
    if not matches:
        print("�� ������� �������� ������ ������")
        return
    
    print(f"\n������� {len(matches)} ������. ������� �������...\n")
    
    results = []
    for i, url in enumerate(matches, 1):
        print(f"������� ����� {i}/{len(matches)}... URL: {url}")
        match_data = parse_match_page(url)
        if match_data:
            results.append(match_data)
            print(f"  {match_data['start_time']} | {match_data['tournament']}")
            print(f"  {match_data['player1']} vs {match_data['player2']}\n")
        time.sleep(2)  # ����������� ��������
    
    # ��������� � ����
    if results:
        with open('tennis_matches_results.txt', 'w', encoding='utf-8') as f:
            for match in results:
                f.write(f"�����: {match['start_time']}\n")
                f.write(f"������: {match['tournament']}\n")
                f.write(f"������: {match['player1']} vs {match['player2']}\n")
                f.write(f"������: {match['url']}\n\n")
        print("\n���������� ��������� � tennis_matches_results.txt")

if __name__ == "__main__":
    main()