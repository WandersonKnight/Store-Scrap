#! python3

from searchlenium import ProductSearch
import sys

print("Argumentos no Terminal: script.py nome_loja nome_produto")

if len(sys.argv) > 3 and sys.argv[1].lower() == "mercado": 
    store = ProductSearch("mercadolivre")
elif len(sys.argv) > 2:
    store =  ProductSearch(sys.argv[1].lower())
else:
    print("Argumentos invalidos")
    exit()

store.store_list()
store.start_selenium()

if sys.argv[1] == "mercado":
    store.search_input(" ".join(sys.argv[3:]))
else:
    store.search_input(" ".join(sys.argv[2:]))

product_dict = store.get_products()
store.best_products(product_dict)
store.print_products(product_dict)