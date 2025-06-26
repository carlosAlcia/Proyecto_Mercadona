# Created by Carlos Alvarez on 2025-06-24

def get_more_cheap_product(products, type:str=""):
    """Finds the cheapest product from a dictionary of products.
    
    Args:
        products (dict): A dictionary of products.
        
    Returns:
        tuple: A tuple containing the product ID and its price of the cheapest product.
    """

    if not products:
        return None, None

    # If a category is specified, filter products by that category
    if type:
        products = {k: v for k, v in products.items() if v['type'] == type}
    
    cheapest_product = min(products.items(), key=lambda item: float(item[1]['price']))
    
    return cheapest_product[0], products[cheapest_product[0]]['price']