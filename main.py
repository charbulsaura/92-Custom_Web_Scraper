# Assignment: Custom Web Scraper
# Build a custom web scraper to collect data on things that you are interested in.
"""
Using what you have learnt about web scraping, scrape a website for data that you are interested in.
Try to build a CSV with the scraped data.
What you scrape is up to you.
"""
"""
Here are some suggestions:

NBA Player Stats
Audible Books and Ratings
Miami House Foreclosure Listing
Steam Games Data
Alibaba Products
Registered Doctors in Idaho
Recipes
Real Estate
Songs
Rollercoasters
Food Nutrition
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

chrome_driver_path = Service("chromedriver_win32\chromedriver.exe")
driver = webdriver.Chrome(service=chrome_driver_path)

#Audible Book & Ratings
driver.get("https://www.audible.com/search?keywords=book&node=18573211011")

#How to specify multiple classes in CSS selector???
# https://selenium-python.readthedocs.io/locating-elements.html
# how to access selenium web element attributes

# sign_in = driver.find_elements(By.XPATH,"/html/body/div[1]/div[4]/div/div/div/header/div[1]/span/nav/span/ul/li/a")
sign_in = driver.find_elements(By.CSS_SELECTOR,"li.bc-list-item a.ui-it-sign-in-link")
# print(sign_in[0].text)

#OBTAINING ALL BOOK DESCRIPTIONS  (Missing data/ too many entries for 1 data?)
# --- Fix: Loop through fixed # of times (eg 20 books- 20 times; and apply None value if no element found)
# book_name = driver.find_elements(By.XPATH,"/html/body/div[1]/div[5]/div[5]/div/div[2]/div[4]/div/div/span/ul/div/li[1]/div/div[1]/div/div[2]/div/div/span/ul/li[1]/h3/a")
book_name = driver.find_elements(By.CSS_SELECTOR,"li.bc-list-item h3.bc-heading a.bc-color-link")
print("-----BOOK TITLE-----")
print(f"x {len(book_name)}")
for item in book_name:
    print(item.text)

book_release = driver.find_elements(By.CSS_SELECTOR,"li.releaseDateLabel span.bc-text")
print("\n-----BOOK RELEASE DATE-----")
print(f"x {len(book_release)}")
for item in book_release:
    print(item.text)

book_rating = driver.find_elements(By.CSS_SELECTOR,"li.ratingsLabel span.bc-pub-offscreen")
print("\n-----BOOK RATINGS-----")
print(f"x {len(book_rating)}")
for item in book_rating:
    print(item.text)

book_prices = []
for j in range(len(book_name)):
    book_price = driver.find_elements(By.ID,f"buybox-regular-price-{j}")
    for item in book_price:
        book_prices.append(item.text[16:])

print("\n-----BOOK PRICE-----")
print(f"x {len(book_prices)}")
print(book_prices)

#How to deal with books with no subtitles?
# --- TAP INTO aria-label = "BookTitle" OBJECT; then retrieve relevant subtitles for each object using normal web scraping
# selenium find element by aria-label using css selector
# https://stackoverflow.com/questions/46669850/using-aria-label-to-locate-and-click-an-element-with-python3-and-selenium
# https://stackoverflow.com/questions/65394553/how-to-do-find-aria-label-using-selenium-and-python

# book_subtitle = driver.find_elements(By.CSS_SELECTOR,"li.subtitle span.bc-size-base")
# book_subtitle = driver.find_elements(By.CSS_SELECTOR,"li.subtitle")
print("\n-----BOOK SUBTITLES-----")
book_subtitle = driver.find_elements(By.CSS_SELECTOR,"li[aria-label]")
print(f"x {len(book_subtitle)}")
individual_sub =[]
for i in range(len(book_subtitle)):
    individual_sub.append(book_subtitle[i].find_element(By.CSS_SELECTOR,"span.bc-size-base"))

#How to deal with books with multiple authors?
# --- just find each li.authorLabel object first instead of parsing all author names; which might contain multiple authors;
# --- only add 1 author to each book title

# book_author = driver.find_elements(By.CSS_SELECTOR,"li.authorLabel span a.bc-color-link")
#How to tap into author object? --->book_author[i].text
book_author = driver.find_elements(By.CSS_SELECTOR,"li.authorLabel")
print("\n-----BOOK AUTHOR-----")
print(f"x {len(book_author)}")
# for item in book_author:
#     print(item.text)
    # print(item.get_dom_attribute("bc-list-item-authorLabel"))

#Contains a list of dictionary (with seperate details- title/subtitle/rating/release date...) of each book
#eg: all_book_individual_info= [
#                               {"title": "xxx", "subtitle": "yyy", "rating": "5.0"...},
#                               {"title": "xxX", "subtitle": "yyY", "rating": "4.0"...},

all_book_individual_info = []
print("\n-----BOOK INDIVIDUAL INFO-----")
for i in range(len(book_name)):
    all_book_individual_info.append(
       {"Title":book_name[i].text ,
        "Release Date": book_release[i].text,
        "Rating": book_rating[i].text,
        "Price": book_prices[i],
        "Subtitle": individual_sub[i].text,
        "Author": book_author[i].text,
        })
print(all_book_individual_info)
print(f"x {len(all_book_individual_info)}")

import json
json_all_book = json.dumps(all_book_individual_info, indent= 5)
with open("Audible_Book_List.txt",mode="w") as file:
    file.write(json_all_book)

driver.quit()