#! python3

from searchlenium import ProductSearch

kabum = ProductSearch("kabum")

kabum.start_selenium()
kabum.search_input("notebook")
temp = kabum.get_products()
kabum.best_products(temp)
kabum.print_products(temp)