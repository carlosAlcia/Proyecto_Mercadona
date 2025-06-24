from api_mercadona import *

if __name__ == "__main__":
    try:
        

        categories = get_categories()
        # Example usage of get_products
        subcategory_id = next(iter(next(iter(categories.values()))['subcategory'].keys()))
        products = get_products(subcategory_id)
        category = next(iter(categories.keys()))
        product_id, price = get_more_cheap_product(products, 'Aceite de oliva')
        subcategories = get_subsubcategory(subcategory_id)
        print(f"Category:{subcategory_id}, subcategory: {subcategories}" )
        print(f"The cheapest product is {product_id} with a price of {price}")

    except Exception as e:
        print(f"An error occurred: {e}")