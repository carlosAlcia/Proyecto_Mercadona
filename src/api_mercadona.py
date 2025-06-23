import requests

URL_Categories = "https://tienda.mercadona.es/api/categories/"

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
    



