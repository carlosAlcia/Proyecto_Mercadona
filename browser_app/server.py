from flask import Flask, request, jsonify

app = Flask(__name__)
PORT = 8080

@app.route('/create_cart', methods=['POST'])
def create_cart():
    data = request.get_json()  
    print("Received data:", data)
    
    response = {
        "Response": "Received your data successfully"
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True, port=PORT)