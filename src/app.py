from api_mercadona import get_categories

if __name__ == "__main__":
    try:
        categories = get_categories()
        print(categories)
    except Exception as e:
        print(f"An error occurred: {e}")