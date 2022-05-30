#! python3

from searchlenium import ProductSearch
import sys

print("Argumentos no Terminal: ")

if len(sys.argv) > 2:
    store =  ProductSearch(sys.argv[1])
else: 
    store = ProductSearch("kabum")

store.store_list()
store.start_selenium()

if len(sys.argv) > 2:
    store.search_input(sys.argv[2:])
else:
    store.search_input("s20 fe")

product_dict = store.get_products()
store.best_products(product_dict)
store.print_products(product_dict)