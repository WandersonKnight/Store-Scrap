#! python3

from searchlenium import ProductSearch

kabum = ProductSearch("amazon")

kabum.start_selenium()
kabum.search_input("notebook")
kabum.get_products()
