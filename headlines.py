import feedparser
from flask import Flask, render_template
import pdb

app = Flask(__name__)

NYT_FEEDS = {
    'space': 'http://rss.nytimes.com/services/xml/rss/nyt/Space.xml',
    'tech': 'http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml',
    'travel': 'http://rss.nytimes.com/services/xml/rss/nyt/Travel.xml'
}

@app.route("/")
def get_home():
    return render_template("home.html")

@app.route("/<publication>")
def get_news(publication):
    feed = feedparser.parse(NYT_FEEDS[publication])
    first_article = feed['entries'][0]

    return render_template("newsPage.html", title=first_article.get("title"), published=first_article.get("published"), summary=first_article.get("summary"))

if __name__ == '__main__':
    app.run(port=5000, debug=True)