from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# GKE Persistent Volume Mount Directory
STORAGE_DIR = "/root/samruddhi_PV_dir"
SERVICE2_URL = "http://service2:6001/process"  # Container 2 URL

# Ensure the persistent storage directory exists
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
    """ Calls Container 2 to compute the sum of a given product """
    data = request.get_json()

    if not data or "file" not in data or "product" not in data:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_path = os.path.join(STORAGE_DIR, data["file"])
    if not os.path.exists(file_path):
        return jsonify({"file": data["file"], "error": "File not found."}), 404

    response = requests.post(SERVICE2_URL, json=data)
    return response.json(), response.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
