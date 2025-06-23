import requests

URL_Categories = "https://tienda.mercadona.es/api/categories/"

def get_categories():
    """Fetches categories from the Mercadona API.
    
    Returns:
        dict: A dictionary containing the categories.
        
    """
    response = requests.get(URL_Categories, headers=None, timeout = 30)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching categories: {response.status_code} - {response.text}")
    



