import time
import sys
import csv 
import pandas
import requests
from  bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def finally_data(soup):
    scrape_data = []
    divs = soup.find_all("div", attrs={"data-testid": "property-card"})
    for div in divs:
        link = div.find("a")["href"]
        raitingis = div.find("div", attrs={"data-testid": "rating-stars"})
        raitin = raitingis.find_all("span") if raitingis else ""
        if len(raitin) >= 3:
            title = div.find("div", attrs={"data-testid": "title"}).text.strip()
            info = div.find("div", class_="d8eab2cf7f").text.strip()
            raiting_stars = len(raitin)
        else:
            continue
        scrape_data.append(
            {
            "title": title,
            "info": info,
            "raiting": raiting_stars,
            "url": link
            }
        )
    return scrape_data

final_data = []
driver = webdriver.Chrome()
driver.maximize_window()
url = "https://www.booking.com/searchresults.en-gb.html?ss=Prague%2C+Czech+Republic&efdco=1&label=gen173nr-1BCAEoggI46AdIM1gEaO4BiAEBmAEJuAEXyAEM2AEB6AEBiAIBqAIDuAL0z-OhBsACAdICJGYwY2Q3NjZjLTE4MjUtNDkxNy04MWRmLTNhZmViNmQ1OWIxZNgCBeACAQ&sid=b1a0e06c703b7aaffab908289e57c3a0&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=index&dest_id=-553173&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=74932855a1c90070&ac_meta=GhA3NDkzMjg1NWExYzkwMDcwIAAoATICZW46BlByYWd1ZUAASgBQAA%3D%3D&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure"
driver.get(url)
time.sleep(3)
driver.execute_script("window.scrollBy(0,15000)", "")
time.sleep(1)
driver.execute_script("window.scrollBy(0,-600)", "")
time.sleep(1)
soup = BeautifulSoup(driver.page_source, 'html.parser')
data = finally_data(soup)
final_data.extend(data)
button = driver.find_element(By.XPATH, '//div/button[@aria-label="Next page"]')
for s in range(39):
    button.click()
    time.sleep(3)
    driver.execute_script("window.scrollBy(0,15000)", "")
    time.sleep(1)
    driver.execute_script("window.scrollBy(0,-600)", "")
    time.sleep(1)
    soup1 = BeautifulSoup(driver.page_source, 'html.parser')
    data1 = finally_data(soup1)
    final_data.extend(data1)

df = pandas.DataFrame(data=final_data)
df.to_csv("sample.csv", index=False)
