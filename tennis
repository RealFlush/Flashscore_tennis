from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time
import re

def get_match_links(driver):
    """Получаем список ссылок на матчи с flashscore.mobi"""
    url = "https://www.flashscore.mobi/tennis/?d=0"
    try:
        driver.get(url)
        time.sleep(3) 
        
        # Находим все ссылки на матчи
        match_elements = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/match/"]')
        match_links = []
        
        for match in match_elements:
            href = match.get_attribute('href')
            match_id = re.search(r'/match/([^/]+)/', href)
            if match_id:
                match_url = f"https://www.flashscore.com/match/tennis/{match_id.group(1)}/#/match-summary"
                match_links.append(match_url)
        
        return match_links
    except WebDriverException as e:
        print(f"Ошибка при получении списка матчей: {e}")
        return []

def parse_match_page(driver, url):
    """Парсим страницу матча на flashscore.com"""
    try:
        driver.get(url)
        time.sleep(3)  
        
        # Извлекаем игроков из title страницы
        title = driver.title
        player1, player2 = 'N/A', 'N/A'
        if ' | ' in title:
            # Разбиваем заголовок по символу '|'
            parts = [part.strip() for part in title.split('|')]
            if len(parts) >= 2:
                # Берем часть с именами игроков (второй элемент)
                players_part = parts[1]
                if ' - ' in players_part:
                    players = [p.strip() for p in players_part.split(' - ')]
                    player1, player2 = players[0], players[1] if len(players) > 1 else 'N/A'
        
        # Извлекаем турнир
        tournament = 'N/A'
            # Пробуем первый селектор
        tournament_element = driver.find_element(
            By.CSS_SELECTOR, 
            '#detail > div.detail__breadcrumbs > nav > ol > li:nth-child(2)'
        )
        tournament = tournament_element.text
        tournament_element2 = driver.find_element(
            By.CSS_SELECTOR, 
            '#detail > div.detail__breadcrumbs > nav > ol > li:nth-child(3)'
        )
        tournament = tournament +' '+tournament_element2.text
   
        
        # Извлекаем время начала
        start_time = 'N/A'
        try:
            time_element = driver.find_element(By.CSS_SELECTOR, '.duelParticipant__startTime')
            start_time = time_element.text
        except NoSuchElementException:
            pass
        
        return {
            'start_time': start_time,
            'tournament': tournament,
            'player1': player1,
            'player2': player2,
            'url': url
        }
    except WebDriverException as e:
        print(f"Ошибка при парсинге {url}: {str(e)[:100]}...")
        return None

def main():

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    try:
        print("Получаю список матчей...")
        matches = get_match_links(driver)
        
        if not matches:
            print("Не удалось получить список матчей")
            return
        
        print(f"\nНайдено {len(matches)} матчей. Начинаю парсинг...\n")
        
        results = []
        for i, url in enumerate(matches, 1):
            print(f"Парсинг матча {i}/{len(matches)}... URL: {url}")
            match_data = parse_match_page(driver, url)
            if match_data:
                results.append(match_data)
                print(f"  {match_data['start_time']} | {match_data['tournament']}")
                print(f"  {match_data['player1']} vs {match_data['player2']}\n")
            time.sleep(2)  
        
        # Сохраняем в файл
        if results:
            with open('tennis_matches_results_selenium.txt', 'w', encoding='utf-8') as f:
                for match in results:
                    f.write(f"Время: {match['start_time']}\n")
                    f.write(f"Турнир: {match['tournament']}\n")
                    f.write(f"Игроки: {match['player1']} vs {match['player2']}\n")
                    f.write(f"Ссылка: {match['url']}\n\n")
            print("\nРезультаты сохранены в tennis_matches_results_selenium.txt")
    finally:
        driver.quit()  # Закрываем драйвер в любом случае

if __name__ == "__main__":
    main()
