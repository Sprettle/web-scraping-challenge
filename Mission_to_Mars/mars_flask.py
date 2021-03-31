from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri = "mongodb://localhost:27017/mars_app")

@app.route("/")
def index():

    mars_results = mongo.db.mars_results.find_one()
    return render_template("index.html", mars = mars_results)

@app.route("/scrape")
def scraper():
    mars_results = mongo.db.mars_results
    mars_scrape = scrape_mars.scrape_info()
    mars_results.update({}, mars_scrape, upsert=True)    
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)



 