import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Load the API key from environment variables
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

@app.route("/fetch_unsplash_images", methods=["GET"])
def fetch_unsplash_images():
    query = request.args.get("query", "")
    url = f"https://api.unsplash.com/search/photos?query={query}&per_page=5&client_id={UNSPLASH_ACCESS_KEY}"
    
    response = requests.get(url)
    if response.status_code == 200:
        return jsonify(response.json())  # Return image data
    else:
        return jsonify({"error": "Failed to fetch images"}), response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
