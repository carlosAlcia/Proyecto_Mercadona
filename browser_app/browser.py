from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import time

# Configure the path to the geckodriver executable
# In my case, it is in the same directory as this script
service = Service(executable_path='./geckodriver')

# Initialize the Firefox driver with the service
driver = webdriver.Firefox(service=service)

# Open the Mercadona website
driver.get("http://tienda.mercadona.es/")

# Add the postal code cookie
driver.add_cookie({
    "name": "__mo_da",
    "value": '{"warehouse":"svq1","postalCode":"41020"}',
    "domain": ".mercadona.es",
    "path": "/",
    "secure": True,
    "httpOnly": False,
})

# Add the cart data
driver.execute_script("""window.localStorage.setItem( \
                      'MO-cart',\
                      '{"id":"716e7efb-4858-4ab6-a6cf-14eaecf2600f",\
                      "lines":[{\
                        "quantity":1, \
                        "product_id":"20612", \
                        "sources":["+PD"]}]}')""")

# Refresh the page to apply the changes
driver.refresh()



