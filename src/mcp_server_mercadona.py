from mcp.server.fastmcp import FastMCP
from api_mercadona import get_categories as api_get_categories
from api_mercadona import get_subcategories as api_get_subcategories
import sys

mcp = FastMCP("mercadona")

@mcp.tool()
def get_categories():
    """Fetches categories from the Mercadona API."""
    categories_dict = api_get_categories()
    categories = "Here are the categories:\n"
    for category_values in categories_dict.values():
        categories += f"- {category_values['name']}\n"
    return categories

# @mcp.tool()
# def get_subcategories(category_id):
#     """Gets subcategories for a given category from the Mercadona API."""
#     return api_get_subcategories(category_id)

if __name__ == "__main__":
    print('Hola', file=sys.stderr)
    mcp.run(transport='stdio')
