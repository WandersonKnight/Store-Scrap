from selenium import webdriver #pip install selenium
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException 
import sys

class ProductSearch:

    def __init__(self, store):
        self.store = store.lower()

        self.custom_options = webdriver.EdgeOptions()
        self.custom_options.add_experimental_option("detach", True) #Mantém o browser aberto

        self.driver_path = Service("C:\Program Files (x86)\msedgedriver.exe") 
        self.driver = webdriver.Edge(options=self.custom_options, service=self.driver_path) #Abre o browser

        self.name_price = {}

    def store_list(self):
        print("Lojas disponiveis:\nKabum\nMercado Livre")

    def start_selenium(self):
        if self.store == "kabum":
            self.driver.get("https://www.kabum.com.br/")
        elif self.store == "mercadolivre":
            self.driver.get("https://www.mercadolivre.com.br/")
        else:
            sys.exit("Erro: Scraping indisponivel para esta loja. Verifique sua entrada")

    def search_input(self, product):
        try:
            if self.store == "kabum":
                if len(self.driver.find_elements_by_id("input-busca")) > 0:
                    search = self.driver.find_element_by_id("input-busca")
                else:
                    search = self.driver.find_element_by_id("smarthint-search-input")
            elif self.store == "mercadolivre":
                search = self.driver.find_element_by_xpath("/html/body/header/div/form/input")
        except NoSuchElementException:
            sys.exit("Nao foi possivel encontrar o elemento na pagina. Por favor verifique o codigo fonte.")

        search.send_keys(product)
        search.send_keys(Keys.RETURN)

    def get_products(self):
        if self.store == "kabum":
            name_list = self.driver.find_elements_by_xpath("//span[contains(@class,'sc-csvncw gASsfm')]")
            price_list = self.driver.find_elements_by_xpath("//span[contains(@class,'sc-dwLEzm')]")
            address_list = [link.get_attribute('href') for link in self.driver.find_elements_by_xpath("//div[contains(@class,'sc-WCkqM')]/a")]
        elif self.store == "mercadolivre":
            name_list = self.driver.find_elements_by_xpath("//h2[contains(@class,'ui-search-item__title')]")
            price_list = self.driver.find_elements_by_xpath("//div[contains(@class,'ui-search-item__group__element')]/div/div/span/span/span[contains(@class,'price-tag-fraction')]")
            address_list = [link.get_attribute('href') for link in self.driver.find_elements_by_xpath("//div[contains(@class,'ui-search-result__image')]/a")]

        for i in range(len(price_list)):
            self.name_price.setdefault(name_list[i].text, [price_list[i].text, address_list[i]])

        return self.name_price

    def best_products(self, product_dict):
        try:
            if type(product_dict) != dict:
                raise TypeError
        except TypeError:
            sys.exit("Objeto fornecido para o metodo 'best_products' nao e um dicionario")
        
        cheapest = [val[0] for val in product_dict.values()]
        cheapest = ScrapHelper.dict_sort(cheapest, self.store)
        cheapest = cheapest[:4]

        for value in product_dict.values():
            temp_value = value[0]
            if "," in temp_value:
                temp_value = temp_value[:temp_value.find(",")]
            if len(value) > 1 and temp_value in cheapest:
                self.driver.execute_script(f"window.open('{value[1]}')")

    def print_products(self, product_dict):
        try:
            if type(product_dict) != dict:
                raise TypeError
        except TypeError:
            sys.exit("Objeto fornecido para o metodo 'print_products' nao e um dicionario")

        for key, value in product_dict.items():
            print(f"{key}")
            for i in range(len(value)):
                print(f"{value[i]}")
            print()

class ScrapHelper:

    def dict_sort(prices, store):
        aux = []

        for price in prices:
            real_price = price.strip("R$ ")
            real_price = real_price.replace(".", "")
            if real_price.find(",") != -1:
                real_price = real_price[:real_price.find(",")]
            aux.append(int(real_price))

        aux.sort()

        for i in range(len(aux)):
            aux[i] = "{:,}".format(aux[i])
            aux[i] = aux[i].replace(",", ".")
            if store != "mercadolivre":
                aux[i] = f"R$ {aux[i]}"
            
        return aux