from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

STORAGE_DIR = "/samruddhi_PV_dir"  

def store_file():
    data = request.get_json()
    if not data or 'file' not in data or 'data' not in data:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    filename = data['file']
    content = data['data']

    app.logger.info("B00990999_Samruddhi")

    if not filename:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    try:
        filepath = os.path.join(STORAGE_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        return jsonify({"file": filename, "message": "Success."}), 200
    except Exception as e:
        return jsonify({"file": filename, "error": "Error while storing the file to the storage."}), 500

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    if not data or 'file' not in data or 'product' not in data:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    filename = data['file']
    product = data['product']

    try:
        response = requests.post(
            "http://container-2-service:6001/process",
            json={"file": filename, "product": product}
        )
        response.raise_for_status()
        return jsonify(response.json()), 200
    except requests.exceptions.RequestException as e:
        if response.status_code == 400:
            error = response.json().get('error', 'Unknown error')
            return jsonify({"file": filename, "error": error}), 400
        else:
            return jsonify({"file": filename, "error": "Error processing request."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)