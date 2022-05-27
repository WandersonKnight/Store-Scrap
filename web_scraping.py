#! python3

from searchlenium import ProductSearch

kabum = ProductSearch("aaaa")

kabum.start_selenium()
kabum.search_input("notebook")
temp = kabum.get_products()
kabum.best_products(temp)