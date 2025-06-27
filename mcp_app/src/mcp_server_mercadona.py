# Created by Carlos Alvarez on 2025-06-24

from mcp.server.fastmcp import FastMCP
from api_mercadona import get_categories as api_get_categories
from api_mercadona import search_products as api_search_product
from api_mercadona import get_subcategories as api_get_subcategories
from api_mercadona import get_products_by_subcategory as api_get_products_by_subcategory
from api_mercadona import get_types as api_get_types
from utils_products import get_more_cheap_product as utils_get_more_cheap_product
import json
import requests

mcp = FastMCP("mercadona")

# Key for search products
search_api_key = None

@mcp.tool()
def get_categories():
    """Fetches categories from the Mercadona API.
    
    Returns:
        str: A formatted string containing the names of the categories and the ID.
    """

    categories_dict = api_get_categories()
    categories = "Here are the categories:\n"
    for category_id, category_values in categories_dict.items():
        categories += f"- {category_values['name']} - ID: {category_id}\n"
    return categories

@mcp.tool()
def get_subcategories(category_id: str):
    """Gets subcategories for a given category from the Mercadona API.
    
    Args:
        category_id (str): The ID of the category to fetch subcategories for.
        
    Returns:
        str: A formatted string containing the names of the subcategories.
    """

    subcategories_dict = api_get_subcategories(category_id)
    if not subcategories_dict:
        return f"No subcategories found for category ID {category_id}."
    subcategories = "Here are the subcategories:\n"
    for subcategory_id, subcategory in subcategories_dict.items():
        subcategories += f"- {subcategory['name']} (ID: {subcategory_id})\n"
    return subcategories


@mcp.tool()
def search_product(query: str):
    """Searches for products in the Mercadona API.
    
    Args:
        query (str): The search query string.
        
    Returns:
        str: A formatted string containing the products found and their prices.
    """

    results = api_search_product(query, search_api_key)
    if not results:
        return "No products found."
    
    response = "Here are the products found and their price:\n"
    for id, product in results.items():
        response += f"- {product['name']} (ID: {id}, price: {product['price']})\n"
    return response

@mcp.tool()
def get_products_by_subcategory(subcategory_id: str):
    """Gets products by subcategory from the Mercadona API.
    
    Args:
        subcategory_id (str): The ID of the subcategory to fetch products for.
        
    Returns:
        str: A formatted string containing the products found in the subcategory.
    """

    products = api_get_products_by_subcategory(subcategory_id)
    if not products:
        return f"No products found for subcategory ID {subcategory_id}."
    
    response = "Here are the products found:\n"
    for id, product in products.items():
        response += f"- {product['name']} (ID: {id}, price: {product['price']})\n"
    return response

@mcp.tool()
def get_types(subcategory_id: str):
    """Extracts types of products from a subcategory id.
    
    Args:
        subcategory_id (str): The id of a subcategory. 
    Returns:
        str: A formatted string containing the types of products for the specified subcategory.
    """
    
    try:
        subcategory_id = int(subcategory_id)
    except ValueError:
        return f"Invalid subcategory ID: {subcategory_id}. It should be an integer."
    
    types = api_get_types(subcategory_id)
    if not types:
        return f"No types found for subcategory ID {subcategory_id}."
    
    response = "Here are the types of products found:\n"
    for type_name in types:
        response += f"- {type_name}\n"
    return response

@mcp.tool()
def get_more_cheap_product(subcategory_id: str, type: str=""):
    """Gets the cheapest product from a subcategory (and type if specified).
    
    Args:
        subcategory_id (str): The ID of the subcategory to search in.
        type (str): The type of product to filter.
        
    Returns:
        str: A formatted string containing the ID and price of the cheapest product found.
    """
    try:
        subcategory_id = int(subcategory_id)
    except ValueError:
        return f"Invalid subcategory ID: {subcategory_id}. It should be an integer."
    products = api_get_products_by_subcategory(subcategory_id)
    product_id, price = utils_get_more_cheap_product(products, type)
    
    if product_id is None:
        return f"No products found for subcategory ID {subcategory_id} with type '{type}'."
    
    return f"The cheapest product is {product_id} with a price of {price}."


@mcp.tool()
def create_mercadona_cart(products: list[int]):
    """Sends a product list to the server to create a Mercadona cart.
    
    Args:
        products (list[int]): The list of product IDs to be sent in the cart.
        
    Returns:
        str: A confirmation message indicating the cart was sent successfully.
    """
    
    # Sending the request to the server in the host machine
    response = requests.post(
        'http://host.docker.internal:8080/create_cart',
        json={'products': products}
    )
    if response.status_code != 200:
        return f"Failed to send cart: {response.status_code} - {response.text}"
    

    return "Cart sent successfully."



if __name__ == "__main__":
    # Read the API key from the temp file
    with open('../secrets.json', 'r') as file:
        secrets : dict = json.load(file)
        search_api_key = secrets.get('search_key')
        if not search_api_key:
            raise ValueError("API key not found in secrets.json")
    mcp.run(transport='stdio')
