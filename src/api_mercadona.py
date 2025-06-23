import requests

URL_Categories = "https://tienda.mercadona.es/api/categories/"
URL_Products = "https://tienda.mercadona.es/api/categories/SUBCATEGORY_ID/"

def process_categories_json(json_data):
    """Processes the JSON data from the Mercadona API to extract categories.
    
    Args:
        json_data (dict): The JSON data from the API response.
        
    Returns:
        dict: A dictionary containing the processed categories. Format:
            {
                category_id: {
                    'name': category_name,
                    'subcategory': {
                        subcategory_id: {
                            'name': subcategory_name
                        }
                    }
                }
            }
        
    """
    categories = {}
    for category in json_data.get('results', []):
        category_id = category['id']
        categories[category_id] = {
            'name': category['name'],
            'subcategory': {}
        }
        for subcategory in category.get('categories', []):
            subcat_id = subcategory['id']
            categories[category_id]['subcategory'][subcat_id] = {
                'name': subcategory['name']
            }

    return categories


def get_categories():
    """Fetches categories from the Mercadona API.
    
    Returns:
        dict: A dictionary containing the categories.
        
    """
    response = requests.get(URL_Categories, headers=None, timeout = 30)
    if response.status_code == 200:
        return process_categories_json(response.json())
    else:
        raise Exception(f"Error fetching categories: {response.status_code} - {response.text}")
    
def get_subcategories(category_id):
    """Gets subcategories for a given category from the Mercadona API.
    
    Args:
        category_id (str): The ID of the category to fetch subcategories for.
    Returns:
        dict: A dictionary containing the subcategories for the specified category.
        """
    response = requests.get(URL_Categories, headers=None, timeout = 30)
    if response.status_code == 200:
        categories = process_categories_json(response.json())
        if category_id in categories:
            return categories[category_id]['subcategory']
        else:
            raise Exception(f"Category ID {category_id} not found in categories.")
    else:
        raise Exception(f"Error fetching categories: {response.status_code} - {response.text}")
    

def process_products_json(json_data):
    """Processes the JSON data from the Mercadona API to extract products.
    
    Args:
        json_data (dict): The JSON data from the API response.
        
    Returns:
        dict: A dictionary containing the processed products. Format:
            {
                product_id: {
                    'name': product_name,
                    'price': product_price
                }
            }
        
    """
    products = {}
    for category in json_data.get('categories', []):
        for product in category.get('products', []):
            product_id = product['id']
            products[product_id] = {
                'name': product['display_name'],
                'price': product['price_instructions']['bulk_price'],
                'category': category['name']
            }

    return products

def get_products(subcategory_id):
    """Fetches products for a given subcategory from the Mercadona API.
    
    Args:
        subcategory_id (int): The ID of the subcategory to fetch products for.
    Returns:
        dict: A dictionary containing the products for the specified subcategory.
        
    """
    url = URL_Products.replace("SUBCATEGORY_ID", str(subcategory_id))
    response = requests.get(url, headers=None, timeout=30)
    if response.status_code == 200:
        return process_products_json(response.json())
    else:
        raise Exception(f"Error fetching products: {response.status_code} - {response.text}")
    

def get_more_cheap_product(products):
    """Finds the cheapest product from a dictionary of products.
    
    Args:
        products (dict): A dictionary of products.
        
    Returns:
        tuple: A tuple containing the product ID and its price of the cheapest product.
        
    """
    if not products:
        return None, None
    
    cheapest_product = min(products.items(), key=lambda item: item[1]['price'])
    return cheapest_product[0], cheapest_product[1]['price']