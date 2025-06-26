# Created by Carlos Alvarez on 2025-06-24

from mcp.server.fastmcp import FastMCP
from api_mercadona import get_categories as api_get_categories
from api_mercadona import search_products as api_search_product
from api_mercadona import get_subcategories as api_get_subcategories
import sys
import json

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



if __name__ == "__main__":
    # Read the API key from the temp file
    with open('../secrets.json', 'r') as file:
        secrets : dict = json.load(file)
        search_api_key = secrets.get('search_key')
        if not search_api_key:
            raise ValueError("API key not found in secrets.json")
    mcp.run(transport='stdio')
