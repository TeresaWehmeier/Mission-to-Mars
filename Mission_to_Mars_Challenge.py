#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_test', wait_time=1)


# In[4]:


html= browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


# Assign title and summary text to variables
slide_elem.find('div',class_='content_title')


# In[6]:


# Use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()


# In[7]:


news_title


# In[8]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[9]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[10]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[11]:


# parse teh resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[12]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[13]:


# use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'


# In[14]:


img_url


# In[15]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns = ['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[16]:


df.to_html()


# In[17]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

browser.visit(url)


# In[18]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# Parse the html with soup
html = browser.html
main_page_soup = soup(html, 'html.parser')

# for loop over the link of each sample picture
for i in range(4):
    # Create an empty dict to hold the search results
    results = {}
    # Find link to picture and open it
    link_image = main_page_soup.select("div.description a")[i].get('href')
    browser.visit(f'https://astrogeology.usgs.gov{link_image}')
    
    # Parse the new html page with soup
    html = browser.html
    sample_image_soup = soup(html, 'html.parser')
    # Get the full image link
    img_url = sample_image_soup.select_one("div.downloads ul li a").get('href')
    # Get the full image title
    img_title = sample_image_soup.select_one("h2.title").get_text()
    # Add extracts to the results dict
    results = {
        'img_url': img_url,
        'title': img_title}
    
    # Append results dict to hemisphere image urls list
    hemisphere_image_urls.append(results)
    
    # Return to main page
    browser.back()


# In[19]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[20]:


# 5. Quit browser
browser.quit()

