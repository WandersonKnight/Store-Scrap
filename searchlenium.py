from typing import Type
from selenium import webdriver #pip install selenium
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.keys import Keys
import sys

class ProductSearch:

    def __init__(self, store):
        self.store = store.lower()

        self.custom_options = webdriver.EdgeOptions()
        self.custom_options.add_experimental_option("detach", True)

        self.driver_path = Service("C:\Program Files (x86)\msedgedriver.exe") 
        self.driver = webdriver.Edge(options=self.custom_options, service=self.driver_path) #open browser and keep open

        self.name_price = {}

    def store_list(self):
        print("Kabum\nAmericanas\nAmazon")

    def start_selenium(self):
        if self.store == "kabum":
            self.driver.get("https://www.kabum.com.br/")
        elif self.store == "americanas":
            self.driver.get("https://www.americanas.com.br/")
        elif self.store == "amazon":
            self.driver.get("https://www.amazon.com.br/")
        else:
            sys.exit("Erro: Store scrapping unavailable. Check your input")

    def search_input(self, product):
        if self.store == "kabum":
            search = self.driver.find_element_by_id("input-busca")
        elif self.store == "americanas":
            search = self.driver.find_element_by_class_name("search__InputUI-sc-1wvs0c1-2 dRQgOV")
        elif self.store == "amazon":
            search = self.driver.find_element_by_id("twotabsearchtextbox")

        search.send_keys(product)
        search.send_keys(Keys.RETURN)

    def get_products(self):
        if self.store == "kabum":
            name_list = self.driver.find_elements_by_xpath("//span[contains(@class,'sc-csvncw gASsfm')]")
            price_list = self.driver.find_elements_by_xpath("//span[contains(@class,'sc-dwLEzm')]")
            address_list = [link.get_attribute('href') for link in self.driver.find_elements_by_xpath("//div[contains(@class,'sc-WCkqM')]/a")]
        elif self.store == "americanas":
            name_list = self.driver.find_elements_by_xpath("//h3[contains(@class,'product-name__Name-sc-1shovj0-0')]")
            price_list = self.driver.find_elements_by_xpath("//span[contains(@class,'src__Text-sc-154pg0p-0')]")
            address_list = [link.get_attribute('href') for link in self.driver.find_elements_by_xpath("//div[@class='inStockCard__Wrapper-sc-1ngt5zo-0']/a")]
        elif self.store == "amazon":
            name_list = self.driver.find_elements_by_xpath("//span[contains(@class,'a-size-base-plus')]")
            price_list = self.driver.find_elements_by_xpath("//span[contains(@class,'a-price-whole')]")
            address_list = [link.get_attribute('href') for link in self.driver.find_elements_by_xpath("//h2[contains(@class,'a-size-mini')]/a")]

        for i in range(len(name_list)):
            self.name_price.setdefault(name_list[i].text, [price_list[i].text, address_list[i]])

        return self.name_price

    def best_products(self, product_dict):
        if type(product_dict != dict):
            pass
        

        cheapest = [val[0] for val in product_dict.values()]
        cheapest.sort()
        cheapest = cheapest[:3]

        cheapest_dict = {}

        for key, value in product_dict.items():
            if value[0] in cheapest:
                cheapest_dict.setdefault(key, value)
                self.driver.execute_script(f"window.open('{value[1]}')")