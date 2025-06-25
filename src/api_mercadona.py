# Created by Carlos Alvarez on 2025-06-23

import requests

URL_Categories = "https://tienda.mercadona.es/api/categories/"
URL_Products = "https://tienda.mercadona.es/api/categories/SUBCATEGORY_ID/"

# Read the key from the temp file
URL_Search = "https://7uzjkl1dj0-dsn.algolia.net/1/indexes/products_prod_svq1_es/query?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser&x-algolia-application-id=7UZJKL1DJ0&x-algolia-api-key=API_KEY"

def search_products(query:str, api_key:str):
    """Searches for products in the Mercadona API using a query string. Returns the ID, name and price of the products found.
    Args:
        query (str): The search query string.
    Returns:
        dict: A dictionary containing the products found in the search. 
    """

    query = query.replace(" ", "+")
    global URL_Search
    URL_Search = URL_Search.replace("API_KEY", api_key)

    payload = {"params":f"query={query}&clickAnalytics=true&analyticsTags=%5B%22web%22%5D&getRankingInfo=true&analytics=true"}
    headers = {"Accept-Encoding":"gzip, deflate, br, zstd",
               "Accept-Language":"es-ES,es;q=0.9",
               "Connection":"keep-alive",
               "Content-Length":"108",
               "Host":"7uzjkl1dj0-dsn.algolia.net",
               "Origin":"https://tienda.mercadona.es",
               "Referer":"https://tienda.mercadona.es/",
               "Sec-Fetch-Dest":"empty",
               "Sec-Fetch-Mode":"cors",
               "Sec-Fetch-Site":"cross-site",
               "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
               "accept":"application/json",
               "content-type":"application/x-www-form-urlencoded",
               "sec-ch-ua": 'Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
               "sec-ch-ua-mobile":"?0",
               "sec-ch-ua-platform":'"macOS"',
               "sec-gpc":"1"}
    response = requests.post(URL_Search, json=payload, headers=headers, timeout=30)
    if response.status_code == 200:
        return process_search_json(response.json())
    else:
        raise Exception(f"Error fetching search results: {response.status_code} - {response.text}")

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

def get_types(subcategory_id):
    """Extracts types of products from a subcategory id.
    
    Args:
        subcategory_id (int): The id of a subcategory.
        
    Returns:
        dict: A dictionary containing the types of products for the specified subcategory.
        
    """
    products = get_products_by_subcategory(subcategory_id)
    types = []
    
    for product in products.values():
        category = product['type']
        if category not in types:
            types.append(category)
    
    return types
     
def get_products_by_subcategory(subcategory_id, type:str=None):
    """Fetches products for a given subcategory from the Mercadona API.
    
    Args:
        subcategory_id (int): The ID of the subcategory to fetch products for.
    Returns:
        dict: A dictionary containing the products for the specified subcategory.
        
    """
    url = URL_Products.replace("SUBCATEGORY_ID", str(subcategory_id))
    response = requests.get(url, headers=None, timeout=30)
    if response.status_code == 200:
        products = process_products_json(response.json(), return_type=True)
        if type:
            products = {k: v for k, v in products.items() if v['type'] == type}
        return products
    else:
        raise Exception(f"Error fetching products: {response.status_code} - {response.text}")


def process_products_json(json_data, return_type=True):
    """Processes the JSON data from the Mercadona API to extract products.
    
    Args:
        json_data (dict): The JSON data from the API response.
        return_type (bool): If True, returns the product type inside the dict.
                            If False, does not include the type.
        
    Returns:
        dict: A dictionary containing the processed products. Format:
            {
                product_id: {
                    'name': product_name,
                    'price': product_price
                    'type': product_type (if return_type is True)
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
                'type': category['name']
            }

    return products

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

def process_search_json(json_data, max_products=3):
    """Processes the JSON data from the Mercadona search API to extract products.
    
    Args:
        json_data (dict): The JSON data from the API response.
        max_products (int): The maximum number of products to return. Default is 3.
        
    Returns:
        dict: A dictionary containing the processed products. Format:
            {
                product_id: {
                    'name': product_name,
                    'price': product_price,
                    'type': product_type
                }
            }
        
    """
    products = {}
    for hit in json_data.get('hits', [])[:max_products]:
        # Get the relevant fields from the hit : ID, name and price.
        products[hit['id']] = {
            'name': hit['slug'],
            'price': hit['price_instructions']['bulk_price']
        }
    return products