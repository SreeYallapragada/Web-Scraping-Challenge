from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

# def init_browser():
#      #Path
#     executable_path = {'executable_path': 'chromedriver.exe'}
#     browser = Browser('chrome', headless = False)


#Scrape Function (main func) 
def scrape_all():

    browser = Browser("chrome", executable_path="chromedriver.exe", headless = True)
    news_title, news_paragraph = mars_news_data(browser)
     #Global dictionary for MongoDB

    martian_data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "weather": mars_weather(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemispheres(browser)
    }
    browser.quit()
   
    return martian_data
   
    
    #NASA Mars Missions News Site
def mars_news_data(browser):

     #URL to visit
    mars_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(mars_url)

    #Allow for time delay to reduce loading
    time.sleep(5)

    #HTML object parsed with BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

     #Search through html code to find a "div" list
    article_results = soup.find("div", class_="list_text")
    
    #Initiate variables that allow you to grab the title and paragraph snippet for the latest news article
    news_title = article_results.find("div", class_="content_title").get_text()
    news_paragraph = article_results.find("div", class_="article_teaser_body").get_text()

    #Closes the browser when scraping is completed
    #browser.quit()
    
    return news_title, news_paragraph


    #Jet Propulsion Lab Space Images    
def featured_image(browser):

    #URL to visit
    jpl_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_image_url)
    
    #Time delay
    time.sleep(5)

    full_image_elem = browser.find_by_id("full_image")
    full_image_elem.click()

    #Finding the location of the featured image
    browser.is_element_present_by_text("more info", wait_time=0.5)
    #image_footer = browser.find_by_tag("footer").click()
    
    more_info_button = browser.find_link_by_partial_text("more info")
    more_info_button.click()
    
    #HTML object parsed with BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

     #Sort through tags to go from parent to child to "grandchild" tag, in order to find the image url
    image_results = soup.find("figure", class_ = "lede").a.img

    #Searching the properties for the image url
    featured_mars_image_url = image_results["src"]
    entire_jpl_image_url = "https://www.jpl.nasa.gov" + featured_mars_image_url
    featured_image = entire_jpl_image_url

    #Quits browser after scraping
    browser.quit()
    
    return featured_image


    #Martian Sol Weather 
def mars_weather(browser):    

    #URL

    url = "http://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    #Time delay
    time.sleep(10)

    #HTML object and BS
    html = browser.html
    weather_soup = BeautifulSoup(html, "html.parser")

    #Sorts from the parent tag
    sol_weather_result = weather_soup.find_all('article')

    #Loop through the tweets for the Sol info
    weather_list = []
    for data in sol_weather_result:
        tweets = data.find("div")
        #print(tweets)
        
        for tweet in tweets.find("div", class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0"):
            weather_list.append(tweet.parent.text)
        
    weather_list[0] 

    mars_weather = weather_list[0]
    #mars_weather

    #Quit Browser
    browser.quit()

    return mars_weather


    #Mars Facts 
def mars_facts():    
    
    #URL
    mars_facts_url = "https://space-facts.com/mars/"
    browser.visit(mars_facts_url)

    #Time delay
    time.sleep(5)
    #HTML object and BS
    html = browser.html
    facts_soup = BeautifulSoup(html, "html.parser")

    #Displays all the indexes available from this page
    mars_facts_table = facts_soup.find("table", id="tablepress-p-mars-no-2").prettify()
    
    mars_facts = pd.read_html(mars_facts_url)
    
    mars_facts.columns = ["Planet Profile", "Information"]
    mars_facts.set_index("Planet Profile", inplace=True)

    return mars_facts.to_html(classes="table table-striped")

    #Martian Hemispheres
def mars_hemispheres(browser):

    #URL
    mars_hemis_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemis_url)
    
    #Time Delay
    time.sleep(5)
    
    #HTML object and BS
    hemis_soup = BeautifulSoup(html, "html.parser")
    html = browser.html

    #Create an empty list to store the results from the scraping of the USGS site
    mars_hemisphere_images = []

    #From the url above, look for and list all four of the hemispheres. Then loop through the html code
    for hemis in range(4):
        mars_hemispheres = {}
    
        #Finds each element tag in the code
        browser.find_by_css("a.product-item h3")[hemis].click()
    
        #Finds the image titles
        mars_hemispheres["Image Title"] = browser.find_by_css("h2.title").get_text()
    
        #Since the images are under "Sample" on each individual page, this finds the anchor and takes the href
        element_sample = browser.links.find_by_text("Sample").first
        mars_hemispheres["Image URL"] = element_sample["href"]
    
        #Appends the hemisphere titles and images to the list created from above
        mars_hemisphere_images.append(mars_hemispheres)
    
    #Quit browser
    browser.quit()

    return mars_hemispheres
  