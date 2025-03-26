from flask import Flask, jsonify, render_template
from scraper import NewsScraper
from datetime import datetime

app = Flask(__name__)
scraper = NewsScraper()

@app.route('/')
def index():
    """Ruta principal que muestra la página web"""
    news = scraper.get_news()
    return render_template('index.html', news=news, last_updated=datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

@app.route('/news')
def get_news():
    """API endpoint que devuelve las noticias en formato JSON"""
    news = scraper.get_news()
    return jsonify({
        'status': 'success',
        'timestamp': datetime.now().isoformat(),
        'count': len(news),
        'news': news
    })

if __name__ == '__main__':
    app.run(debug=True)