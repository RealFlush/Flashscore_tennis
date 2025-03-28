import requests
from bs4 import BeautifulSoup
import re
import time


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_match_links():
    """Получаем список ссылок на матчи с flashscore.mobi"""
    url = "https://www.flashscore.mobi/tennis/?d=0"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Находим все ссылки на матчи
        match_links = []
        for match in soup.find_all('a', href=re.compile(r'/match/')):
            match_id = match['href'].split('/')[-2]  # Извлекаем ID матча
            if match_id:
                match_url = f"https://www.flashscore.com/match/tennis/{match_id}/#/match-summary"
                match_links.append(match_url)
        
        return match_links
    except Exception as e:
        print(f"Ошибка при получении списка матчей: {e}")
        return []

def parse_match_page(url):
    """Парсим страницу матча на flashscore.com"""
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        
        
        # Извлекаем игроков
        og_title = soup.find('meta', property='og:title')
        if og_title:
            players = og_title['content'].split(' - ')
            player1, player2 = players[0], players[1] if len(players) > 1 else 'N/A'
        else:
            player1, player2 = 'N/A', 'N/A'
        
        # Извлекаем турнир
        og_desc = soup.find('meta', property='og:description')
        tournament = og_desc['content'] if og_desc else 'N/A'
        
        # Извлекаем время начала
        start_time = ''
        
        return {
            'start_time': start_time,
            'tournament': tournament,
            'player1': player1,
            'player2': player2,
            'url': url
        }
    except Exception as e:
        print(f"Ошибка при парсинге {url}: {str(e)[:100]}...")
        return None

def main():
    print("Получаю список матчей...")
    matches = get_match_links()
    
    if not matches:
        print("Не удалось получить список матчей")
        return
    
    print(f"\nНайдено {len(matches)} матчей. Начинаю парсинг...\n")
    
    results = []
    for i, url in enumerate(matches, 1):
        print(f"Парсинг матча {i}/{len(matches)}... URL: {url}")
        match_data = parse_match_page(url)
        if match_data:
            results.append(match_data)
            print(f"  {match_data['start_time']} | {match_data['tournament']}")
            print(f"  {match_data['player1']} vs {match_data['player2']}\n")
        time.sleep(2)  # Увеличенная задержка
    
    # Сохраняем в файл
    if results:
        with open('tennis_matches_results.txt', 'w', encoding='utf-8') as f:
            for match in results:
                f.write(f"Время: {match['start_time']}\n")
                f.write(f"Турнир: {match['tournament']}\n")
                f.write(f"Игроки: {match['player1']} vs {match['player2']}\n")
                f.write(f"Ссылка: {match['url']}\n\n")
        print("\nРезультаты сохранены в tennis_matches_results.txt")

if __name__ == "__main__":
    main()