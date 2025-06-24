from mcp.server.fastmcp import FastMCP
from api_mercadona import get_categories as api_get_categories
from api_mercadona import get_subcategories as api_get_subcategories

mcp = FastMCP("mercadona")

@mcp()
def get_categories():
    """Fetches categories from the Mercadona API."""
    return api_get_categories()

@mcp()
def get_subcategories(category_id):
    """Gets subcategories for a given category from the Mercadona API."""
    return api_get_subcategories(category_id)

