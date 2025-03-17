import os
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS  # 🔥 Import CORS

app = Flask(__name__)
CORS(app)  # 🔥 Enable CORS for all routes

# Load the Unsplash API key from environment variables
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

@app.route("/fetch_unsplash_images", methods=["GET"])
def fetch_unsplash_images():
    query = request.args.get("query", "")
    url = f"https://api.unsplash.com/search/photos?query={query}&per_page=5&orientation=landscape&client_id={UNSPLASH_ACCESS_KEY}"

    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Filter for images that are truly landscape (width > height)
        landscape_images = [
            img["urls"]["full"] for img in data.get("results", [])
            if img["width"] > img["height"]  # Check aspect ratio
        ]

        # Return only the first 2 properly formatted landscape images
        return jsonify({"images": landscape_images[:6]})
    else:
        return jsonify({"error": "Failed to fetch images"}), response.status_code

# 🚀 NEW: Health Check Route
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "alive"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
