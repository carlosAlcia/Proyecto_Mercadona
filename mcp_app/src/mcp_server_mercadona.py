from mcp.server.fastmcp import FastMCP
from api_mercadona import get_categories as api_get_categories
from api_mercadona import search_products as api_search_product
import sys
import json

mcp = FastMCP("mercadona")

# Key for search products
search_api_key = None

@mcp.tool()
def get_categories():
    """Fetches categories from the Mercadona API.
    
    Returns:
        str: A formatted string containing the names of the categories.
    """

    categories_dict = api_get_categories()
    categories = "Here are the categories:\n"
    for category_values in categories_dict.values():
        categories += f"- {category_values['name']}\n"
    return categories


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
