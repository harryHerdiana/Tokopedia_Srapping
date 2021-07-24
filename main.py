import math
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
chrome_driver_path = "/home/harryherdiana/Documents/chromedriver_linux64/chromedriver"
tokopedia_url = "https://www.tokopedia.com"
item_search = input("What is the product you searching for?\n")
currency = input("What currency do you want to convert?\nsee below link for reference\n"
                 "https://docs.1010data.com/1010dataReferenceManual/DataTypesAndFormats/currencyUnitCodes.html\n")
search_item_url = ""
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
           "Accept-Language": "en-US,en;q=0.5"}
prices = []
average_price = int


class Scrapper:
    def __init__(self, driver_path):
        self.driver = webdriver.Chrome(executable_path=driver_path, options=options)

    def finding_item(self):
        global search_item_url
        self.driver.get(tokopedia_url)
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[1]/div/div/div[2]/div[2]/form/div/div/div/input"
        ).send_keys(item_search)  # filling search input with item search
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[1]/div/div/div[2]/div[2]/form/div/div/div/button").click()  # click find item
        time.sleep(3)
        self.driver.refresh()
        time.sleep(3)
        self.driver.refresh()
        time.sleep(2)
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/div/button").click()  # click sorting
        time.sleep(1)
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/div/div/ul/li[3]/button").click()  # sorting from
        # newest
        time.sleep(1)
        # self.driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div[1]/div[1]/div/div/div[
        # 2]/div/div/div/div[2]/div/div/input").click() # Selecting items from power merchant
        search_item_url = self.driver.current_url

    def scrapping(self):
        global search_item_url
        self.response = requests.get(
            url=search_item_url, headers=headers)
        self.website = self.response.text
        self.soup = BeautifulSoup(self.website, "lxml")
        self.prices = self.soup.find_all("div", class_="css-rhd610")
        for price in self.prices:
            pre_formatted_price = str(price.getText()).replace(".", "").replace("Rp", "")
            prices.append(int(pre_formatted_price))
        self.driver.quit()

    def average_calc(self):
        global prices, average_price
        self.total = 0
        self.sorted_prices = prices[5:]
        for price in self.sorted_prices:
            self.total += price
        self.average = math.floor(self.total / len(prices))
        average_price = self.average


class Convert_To_Other_Currency:
    def __init__(self, driver_path):
        self.driver2 = webdriver.Chrome(executable_path=driver_path, options=options)

    def converter(self):
        self.driver2.get(f"https://www.xe.com/currencyconverter/convert/?Amount={average_price}&From=IDR&To={currency}")
        time.sleep(2)
        self.converted_price = self.driver2.find_element_by_class_name("result__BigRate-sc-1bsijpp-1").text
        print(
            f"Here is the average price of {item_search} "
            f"in Indonesian market on your currency: {self.converted_price}")
        self.driver2.quit()


bot = Scrapper(chrome_driver_path)
bot.finding_item()
bot.scrapping()
bot.average_calc()
bot2 = Convert_To_Other_Currency(chrome_driver_path)
bot2.converter()
