# Created by Carlos Alvarez on 2025-06-26

from flask import Flask, request, jsonify
from browser import Browser

app = Flask(__name__)
PORT = 8080
BROWSER_LAUNCHED = False
BROWSER = None

@app.route('/create_cart', methods=['POST'])
def create_cart():
    data = request.get_json()  
    products_id = data.get('products', [])

    global BROWSER_LAUNCHED
    if not BROWSER_LAUNCHED:
        BROWSER.open_mercadona(products_id)
        BROWSER_LAUNCHED = True
    else:
        BROWSER.add_products_to_cart(products_id)


    return jsonify('{"Response":"Send to the cart."}'), 200

if __name__ == '__main__':
    BROWSER = Browser()
    app.run(debug=True, port=PORT)