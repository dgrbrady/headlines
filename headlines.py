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

"""@app.route("/")
def get_home():
    return render_template("home.html")"""

@app.route("/")
def get_news():
    query = request.args.get("publication")
    if not query or query.lower() not in NYT_FEEDS:
        publication = "space"
    else:
        publication = query.lower()
    feed = feedparser.parse(NYT_FEEDS[publication])
    weather = get_weather("London,UK")

    return render_template("newsPage.html", headline=publication, articles=feed['entries'], weather=weather)

def get_weather(query):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=be89569744a2e70fd838a538a7e69cb9"
    query = urllib.parse.quote(query)
    url = api_url.format(query)
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