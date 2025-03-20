from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

STORAGE_DIR = "/samruddhi_PV_dir"

os.makedirs(STORAGE_DIR, exist_ok=True)

@app.route('/store-file', methods=['POST'])
def store_file():
    data = request.get_json()

    if not data or "file" not in data or "data" not in data:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_name = data["file"]
    file_content = data["data"]

    try:
        file_path = os.path.join(STORAGE_DIR, file_name)
        with open(file_path, 'w') as f:
            f.write(file_content)
        return jsonify({"file": file_name, "message": "Success."}), 200
    except Exception as e:
        return jsonify({"file": file_name, "error": str(e)}), 500

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    if not data or 'file' not in data or 'product' not in data:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    filename = data['file']
    product = data['product']

    try:
        response = requests.post(
            "http://container-2-service:6000/process",
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