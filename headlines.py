import datetime
import feedparser
from flask import Flask, render_template, request, make_response
import pdb
from flask_bootstrap import Bootstrap
import json
from urllib.request import urlopen
import urllib.parse

app = Flask(__name__)
bootstrap = Bootstrap(app)

"""
URLs used to fetch data from remote APIs with the API key in the string.
"""
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=be89569744a2e70fd838a538a7e69cb9"
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=db10a7e8ae884d21bffefc165b1c0960"

"""
Dictionary of registered RSS feeds the user can view.
"""
NYT_FEEDS = {
    'space': 'http://rss.nytimes.com/services/xml/rss/nyt/Space.xml',
    'tech': 'http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml',
    'travel': 'http://rss.nytimes.com/services/xml/rss/nyt/Travel.xml'
}

"""
Settings for what publication, city and currency exchange are loaded by default.
"""
DEFAULTS = {
    'publication': 'space',
    'city': 'London, UK',
    'currency_from': 'GBP',
    'currency_to': 'USD'
}

def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]

@app.route("/")
def home():
    # Get customized headlines, based on user input or default
    publication = get_value_with_fallback("publication")
    articles = get_news(publication)

    # Get customized weather based on user input or default
    city = get_value_with_fallback("city")
    weather = get_weather(city)

    # Get customized currency based on user input or default
    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")
    rate, currencies = get_rate(currency_from, currency_to)

    # Wrap make_response() around render_template() to return the rendered Jinja template as a response object
    response = make_response(render_template(
                            "newsPage.html",
                            articles=articles,
                            weather=weather,
                            currency_from=currency_from,
                            currency_to=currency_to,
                            rate=rate,
                            currencies=sorted(currencies)))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)

    # Set cookies
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response

def get_news(query):
    if not query or query.lower() not in NYT_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(NYT_FEEDS[publication])
    return feed['entries']

def get_weather(query):
    query = urllib.parse.quote(query)
    url = WEATHER_URL.format(query) #api_url.format(query)
    data = urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {
            'description': parsed["weather"][0]["description"],
            'temperature': parsed["main"]["temp"],
            'city': parsed["name"],
            'country': parsed['sys']['country']
        }
        return weather

def get_rate(frm, to):
    all_currency = urlopen(CURRENCY_URL).read()
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())

    return (to_rate / frm_rate, parsed.keys())

if __name__ == '__main__':
    app.run(port=5000, debug=True)