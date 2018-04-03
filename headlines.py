import feedparser
from flask import Flask, render_template, request
import pdb
from flask_bootstrap import Bootstrap

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

    return render_template("newsPage.html", headline=publication, articles=feed['entries'])

if __name__ == '__main__':
    app.run(port=5000, debug=True)