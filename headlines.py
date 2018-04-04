import feedparser
from flask import Flask, render_template, request
import pdb
from flask_bootstrap import Bootstrap
import json
from urllib.request import urlopen
import urllib.parse

app = Flask(__name__)
bootstrap = Bootstrap(app)

NYT_FEEDS = {
    'space': 'http://rss.nytimes.com/services/xml/rss/nyt/Space.xml',
    'tech': 'http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml',
    'travel': 'http://rss.nytimes.com/services/xml/rss/nyt/Travel.xml'
}

DEFAULTS = {
    'publication': 'space',
    'city': 'London, UK'
}

@app.route("/")
def home():
    # Get customized headlines, based on user input or default
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    # Get customized weather based on user input or default
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)

    return render_template("newsPage.html", articles=articles, weather=weather)

def get_news(query):
    if not query or query.lower() not in NYT_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(NYT_FEEDS[publication])
    return feed['entries']

def get_weather(query):
    WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=be89569744a2e70fd838a538a7e69cb9"
    query = urllib.parse.quote(query)
    url = WEATHER_URL.format(query) #api_url.format(query)
    data = urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {
            'description': parsed["weather"][0]["description"],
            'temperature': parsed["main"]["temp"],
            'city': parsed["name"]
        }
        return weather

if __name__ == '__main__':
    app.run(port=5000, debug=True)