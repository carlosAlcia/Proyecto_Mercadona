from api_mercadona import *

if __name__ == "__main__":
    try:
        categories = get_categories()
        # Example usage of get_products
        subcategory_id = next(iter(next(iter(categories.values()))['subcategory'].keys()))
        print(subcategory_id)
        products = get_products(subcategory_id)
        print(products)
        category = next(iter(categories.keys()))
        print(categories)
        print(category)
        print(get_subcategories(category))

    except Exception as e:
        print(f"An error occurred: {e}")