# Created by Carlos Alvarez on 2025-06-23


from api_mercadona import *
from utils_products import *
import json

if __name__ == "__main__":
    try:
        

        products = search_products('Aceite de oliva')
        print(f"Found {len(products)} products for 'Aceite de oliva'")
        for product_id, product_data in products.items():
            print(f"Product ID: {product_id}, Name: {product_data['name']}, Price: {product_data['price']}")
        exit()

        categories = get_categories()
        # Example usage of get_products
        subcategory_id = next(iter(next(iter(categories.values()))['subcategory'].keys()))
        products = get_products_by_subcategory(subcategory_id)
        product_id, price = get_more_cheap_product(products, 'Aceite de oliva')
        subcategories = get_types(subcategory_id)
        print(f"Category:{subcategory_id}, subcategory: {subcategories}" )
        print(f"The cheapest product is {product_id} with a price of {price}")

    except Exception as e:
        
        print(f"An error occurred: {e}")
        print(str(e.args))