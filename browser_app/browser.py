# Created by Carlos Alvarez on 2025-06-26

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import json

class Browser:
    """A simple class to manage a Selenium browser instance to open Mercadona website and add products to the cart."""
    
    # Configure the path to the geckodriver executable
    # In my case, it is in the same directory as this script
    def __init__(self, driver_path: str='./geckodriver'):
        """Initializes the browser with the specified driver path."""
        self.service = Service(executable_path=driver_path)
        self.products = []

    def open_mercadona(self, products_id: list[int] = []):
        """Opens the Mercadona website in the browser.
        
        Args:
            products_id (list[int]): A list of product IDs to add to the cart.
        """
        self.driver = webdriver.Firefox(service=self.service)
        self.driver.get("http://tienda.mercadona.es/")
        # Add the postal code cookie
        self.driver.add_cookie({
            "name": "__mo_da",
            "value": '{"warehouse":"svq1","postalCode":"41020"}',
            "domain": ".mercadona.es",
            "path": "/",
            "secure": True,
            "httpOnly": False,
        })
        # Extend the products list with the provided product IDs
        self.products.extend(products_id)
        # Remove duplicates from the products list
        self.products = list(set(self.products))
        # Create the cart object with the products
        products_lines = [
            {"quantity": 1,"product_id":str(pid), "sources":["+CT"]}
            for pid in self.products
        ]
        cart_object = {
            "id": "716e7efb-4858-4ab6-a6cf-14eaecf2600f",
            "lines": products_lines 
        }
        # Store the cart object in localStorage
        # This is necessary to simulate the cart in the browser
        self.driver.execute_script(
            "window.localStorage.setItem('MO-cart', arguments[0]);",
            json.dumps(cart_object)
        ) 
        # Refresh the page to apply the cart changes
        self.driver.refresh()

    def add_products_to_cart(self, products_id: list[int]):
        """Adds products to the existing cart by their IDs.
        
        Args:
            products_id (list[int]): A list of product IDs to add to the cart.
        """
        # Extend the products list with the new product IDs
        self.products.extend(products_id)
        # Remove duplicates from the products list
        self.products = list(set(self.products))
        # Create the cart object with the updated products
        # This will overwrite the existing cart in localStorage
        products_lines = [
            {"quantity": 1, "product_id": str(pid), "sources": ["+CT"]}
            for pid in self.products
        ]
        cart_object = {
            "id": "716e7efb-4858-4ab6-a6cf-14eaecf2600f",
            "lines": products_lines
        }
        self.driver.execute_script(
            "window.localStorage.setItem('MO-cart', arguments[0]);",
            json.dumps(cart_object)
        )
        # Refresh the page to apply the cart changes
        self.driver.refresh()


    def close(self):
        """Closes the browser."""
        self.driver.quit()

