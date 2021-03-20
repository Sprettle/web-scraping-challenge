# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# NASA Mars News

# %%
# Dependencies
import os
import requests
import pandas as pd
import pymongo
import time
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

# %%
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.mars_db

# %%
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=True)

def scrape_info():
    browser = init_browser()


# %%
# URL of NASA Mars News
url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

# visit URl to determine variables


# %%
# Retrieve page with the requests module
response = requests.get(url)


# %%
# Create BeautifulSoup object; parse with 'html.parser'
soup = bs(response.text, 'html.parser')


# %%
# return the title of the news
news_title = soup.find('div', class_='content_title').text
print(news_title)


# %%
# return the paragraph of the news
news_p = soup.find('div', class_='rollover_description_inner').text
print(news_p)

# %% [markdown]
# JPL Mars Space Images - Featured Image

# %%



# %%
# URL of the page to be scraped
jpl_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'


# %%
browser = init_browser()

browser.visit(jpl_url)

# %%
html = browser.html
soup = bs(html, "html.parser")


# %%
# Save the hero image url as variable
base_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'


# %%
#Find the src of the correct image (hero Image)
relative_image_path = soup.find_all('img')[1]["src"]


# %%
# Complete the featured image url by adding the base url ---
featured_image_url = base_url + relative_image_path
featured_image_url

# %% [markdown]
# Mars Facts

# %%
# URL from Mars Facts webpage
mars_url = 'https://space-facts.com/mars/'


# %%
# Read from URL
mars_table = pd.read_html(mars_url)
mars_table


# %%

mars_df = mars_table[0]
mars_df


# %%
mars_df = mars_table[0]

# Change the columns name
mars_df.columns = ['Description','Value']


# %%
# Save the HTML file
mars_df.to_html('mars_html')

# %% [markdown]
# Mars Hemispheres

# %%
# Visit hemispheres website through splinter module 
hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


# %%
# Retrieve page with the requests module
response = requests.get(hemispheres_url)


# %%
# Create BeautifulSoup object; parse with 'html.parser'
soup = bs(response.text, "html.parser")


# %%
# Retreive all items that contain mars hemispheres information
items = soup.find_all('div', class_='item')


# %%
# Create empty list for hemisphere urls 
hemisphere_image_urls = []

# Loop through the items previously stored
for x in items: 
    # Store title
    title = x.find('h3').text
    
      # Set up to go to hemisphere pages to get full image url
    end_url = x.find("a")["href"]
    image_link = "https://astrogeology.usgs.gov/" + end_url

       
    # Visit the link that contains the full image website 
    browser.visit(image_link)
    
    # HTML Object of individual hemisphere information website 
    partial_img_html = browser.html
    
    # Parse HTML with Beautiful Soup for every hemisphere site
    soup = bs( partial_img_html, 'html.parser')
       
    # Get full image url
    downloads = soup.find("div", class_="downloads")
    image_url = downloads.find("a")["href"]

    # Append the link and title to the empty link created at the beginning 
    hemisphere_image_urls.append({"title" : title, "image_url" : image_url})
    
 


# %%
# Display hemisphere_image_urls
hemisphere_image_urls


# %%
browser.quit()

# %%
# Store data in a dictionary
mars_results = {
    "news_title": news_title,
    "news_p": news_p,
    "featured_image_url": featured_image_url,
    "mars_facts": mars_df,
    "hemisphere_image_urls": hemisphere_image_urls
}
# %%
# return mars_results
# print(scrape_info())
mars_results
  # %%