import time
import sys
import csv 
import pandas
import requests
from  bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def browser():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome('chromedriver', chrome_options=options)
    return driver

def urls1(soup):
    links = []
    divs = soup.find_all("div", attrs={"data-testid": "property-card"})
    for div in divs:
        raitingis = div.find("div", attrs={"data-testid": "rating-stars"})
        raitin = raitingis.find_all("span") if raitingis else ""
        if len(raitin) >= 4:
            link = div.find("a")["href"]
            links.append(link)
        else:
            continue
    return links
def urls():
    final_data = []
    driver = webdriver.Chrome()
    driver.maximize_window()
    url = "https://www.booking.com/searchresults.en-gb.html?ss=Dubai%2C+Dubai+Emirate%2C+United+Arab+Emirates&efdco=1&label=gen173nr-1BCAEoggI46AdIM1gEaO4BiAEBmAEJuAEXyAEM2AEB6AEBiAIBqAIDuAKsmeWhBsACAdICJDM4YjEzMzAxLWE2MTMtNGJiNi05OWZhLTViYzZkODBiMTMzYtgCBeACAQ&sid=ed2a5713498518492dcc3228c24e2c68&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=index&dest_id=-782831&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=4ef75a96aac604d5&ac_meta=GhA0ZWY3NWE5NmFhYzYwNGQ1IAAoATICZW46BGR1YmFAAEoAUAA%3D&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure"
    driver.get(url)
    time.sleep(3)
    driver.execute_script("window.scrollBy(0,15000)", "")
    time.sleep(1)
    driver.execute_script("window.scrollBy(0,-700)", "")
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    data = urls1(soup)
    final_data.extend(data)
    button = driver.find_element(By.XPATH, '//div/button[@aria-label="Next page"]')
    for s in range(39):
        button.click()
        time.sleep(3)
        driver.execute_script("window.scrollBy(0,15000)", "")
        time.sleep(1)
        driver.execute_script("window.scrollBy(0,-700)", "")
        time.sleep(1)
        soup1 = BeautifulSoup(driver.page_source, 'html.parser')
        data1 = urls1(soup1)
        final_data.extend(data1)
    return final_data

def datas():
    data5 = []
    all_url = urls()
    n = 0
    for url in all_url:
        try:
            driver = browser()
            driver.get(url)
            time.sleep(1)
            soup5 = BeautifulSoup(driver.page_source, 'html.parser')
            raitingis1 = soup5.find("span", attrs={"data-testid": "rating-stars"})
            raitin1 = raitingis1.find_all("span") if raitingis1 else ""
            location = soup5.find("span", attrs={"data-node_tt_id": "location_score_tooltip"}).text.strip()
            hotel_name = soup5.find("div", id="hp_hotel_name").find("h2").text.strip()
            data5.append(
                {
                "hotel_name": hotel_name,
                "hotel_adress": location,
                "raiting_stars": len(raitin1),
                "url": url
                }
            )
            n+=1
            k = len(all_url)
            print(f"{k}/{n}")
            driver.quit()
        except:
            driver.quit()
            continue
    return data5

data = datas()
df = pandas.DataFrame(data=data)
df.to_csv("sample.csv", index=False)