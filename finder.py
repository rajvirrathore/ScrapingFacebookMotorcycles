# Import necessary libraries
from splinter import Browser
from bs4 import BeautifulSoup as soup
from selenium.webdriver.chrome.options import Options
import re
import pandas as pd 
import matplotlib.pyplot as plt
import time


user_email = " "
user_pass = " "

chrome_options = Options()
prefs = {
    "profile.default_content_setting_values.notifications": 2  # 1=allow, 2=block
}
chrome_options.add_experimental_option("prefs", prefs)

# Launch browser with options
browser = Browser("chrome", options=chrome_options)
browser.visit('https://www.facebook.com/')

browser.visit("https://www.facebook.com/marketplace/110945412261374/search?minPrice=4000&maxPrice=7500&daysSinceListed=14&query=motorbike&exact=false")
#browser.visit("https://www.facebook.com/marketplace/category/vehicles?maxPrice=10000&maxMileage=100000&minYear=2011&make=1274042129420222&exact=false")

browser.fill('email', user_email)
browser.fill('pass', user_pass)

time.sleep(2)
Xbutton = browser.find_by_xpath('//div[@aria-label="Close" and @role="button"]')
Xbutton.click()

time.sleep(3)
logInButton = browser.find_by_xpath('//div[@aria-label="Log in" and @role="button"]')
logInButton.click()


# Define the number of times to scroll the page
scroll_count = 4

# Define the delay (in seconds) between each scroll
scroll_delay = 4

# Loop to perform scrolling
for _ in range(scroll_count):
    # Execute JavaScript to scroll to the bottom of the page
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Pause for a moment to allow the content to load
    time.sleep(scroll_delay)

# Parse the HTML
html = browser.html

# Create a BeautifulSoup object from the scraped HTML
market_soup = soup(html, 'html.parser')

year_model_div = market_soup.find_all('span', class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6")
year_model = [title.text.strip() for title in year_model_div]
prices_div = market_soup.find_all('span', class_="x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x1lkfr7t x1lbecb7 x1s688f xzsf02u")
prices_list = [price.text.strip() for price in prices_div]
mileage_div = market_soup.find_all('span', class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft")
mileage_list = [mileage.text.strip() for mileage in mileage_div]
urls_div = market_soup.find_all('a',class_="x1i10hfl xjbqb8w x1ejq31n x18oe1m7 x1sy0etr xstzfhl x972fbf x10w94by x1qhh985 x14e42zd x9f619 x1ypdohk xt0psk2 x3ct3a4 xdj266r x14z9mp xat24cr x1lziwak xexx8yu xyri2b x18d9i69 x1c1uobl x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xkrqix3 x1sur9pj x1s688f x1lku1pv")
urls_list = [url.get('href') for url in urls_div]

km_list = []
foundAssociatedCity = False

for i in range(len(mileage_list)):

    if "VIC" in mileage_list[i]:
        foundAssociatedCity = True
        currentCity = mileage_list[i]

    if i+1 < len(mileage_list):
        if i+1 < len(mileage_list) and "km" in mileage_list[i+1]:
            currentKM = mileage_list[i+1]
        else:
            currentKM = -1
    
    if foundAssociatedCity:
        print(currentKM)
        km_list.append([currentCity, currentKM])
        foundAssociatedCity = False

year = []
model = []
badApple = []
foundValid = False
k = 0
for item in year_model:
    found_year = re.search(r'(^\d*)\s(.*)',item)
    
    if found_year:
        year.append(found_year.group(1))
        model.append(found_year.group(2))
        foundValid = True

    elif not found_year and foundValid:
        badApple.append(k)
    
    k+=1

for i in range(len(urls_list)):
    urls_list[i] = "https://www.facebook.com" + urls_list[i]


prices_list.pop(0)

for i in reversed(badApple):
    print("removing: ", i)
    # if len(prices_list) > i:
    prices_list.pop(i)
    # if len(km_list) > i:
    km_list.pop(i)
    # if len(urls_list) > i:
    urls_list.pop(i)

length = min(len(model), len(year), len(prices_list), len(km_list), len(urls_list))
print(length)
# Add all values to a list of dictionaries
vehicles_list = []

for i in range(length):
    bikes_dict = {
        "Year": year[i],
        "Make": model[i],
        "Price": prices_list[i],
        "Mileage": km_list[i],
        "URL": urls_list[i]
    }
    vehicles_list.append(bikes_dict)

vehicles_df = pd.DataFrame(vehicles_list)

# Set the display option to ensure that all characters in a column are shown
pd.set_option('display.max_colwidth', None)

print(vehicles_df.head())


csv_file_path = r''

vehicles_df = vehicles_df.sort_values(by="Price", ascending=True)
vehicles_df.to_csv(csv_file_path, index=False)