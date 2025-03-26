import requests
from bs4 import BeautifulSoup
from typing import List, Dict

class NewsScraper:
    def __init__(self):
        # Cambiamos a otro sitio de noticias en español más accesible
        self.url = "https://www.20minutos.es"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def get_news(self) -> List[Dict]:
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            # Ajustamos los selectores para 20minutos.es
            articles = soup.find_all('article', class_='media')
            
            news_list = []
            for article in articles[:10]:
                headline = article.find('h1') or article.find('h2')
                link = article.find('a')
                
                if headline and link:
                    title = headline.text.strip()
                    url = link.get('href', '')
                    if not url.startswith('http'):
                        url = self.url + url
                        
                    news_list.append({
                        'title': title,
                        'url': url
                    })
            
            if not news_list:
                # Fallback: intentar con otros selectores comunes
                headlines = soup.find_all(['h1', 'h2'], class_=['headline', 'title'])
                for headline in headlines[:10]:
                    link = headline.find('a')
                    if link:
                        news_list.append({
                            'title': headline.text.strip(),
                            'url': link.get('href', '')
                        })
            
            return news_list
        except Exception as e:
            print(f"Error al obtener noticias: {str(e)}")
            return []