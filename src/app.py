from api_mercadona import get_categories, get_products

if __name__ == "__main__":
    try:
        categories = get_categories()
        # Example usage of get_products
        subcategory_id = next(iter(next(iter(categories.values()))['subcategory'].keys()))
        print(subcategory_id)
        products = get_products(str(subcategory_id))
        print(products)

    except Exception as e:
        print(f"An error occurred: {e}")