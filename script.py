import os
from flask import Flask, request, jsonify
import requests
import base64

app = Flask(__name__)

# Load Unsplash API key securely
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

def convert_to_base64(image_url):
    response = requests.get(image_url)
    return base64.b64encode(response.content).decode("utf-8")

@app.route("/fetch_unsplash_images", methods=["GET"])
def fetch_unsplash_images():
    query = request.args.get("query", "")
    per_page = 5  # Fetch more images for filtering
    url = f"https://api.unsplash.com/search/photos?query={query}&client_id={UNSPLASH_ACCESS_KEY}&per_page={per_page}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        landscape_images = []

        # Filter for landscape images (width > height)
        for image in data.get("results", []):
            width = image["width"]
            height = image["height"]
            if width > height:  # Landscape check
                landscape_images.append({
                    "base64": convert_to_base64(image["urls"]["regular"])
                })

            if len(landscape_images) == 2:  # Limit to 2 images
                break

        if landscape_images:
            return jsonify({"images": landscape_images})
        else:
            return jsonify({"error": "No landscape images found"}), 404

    return jsonify({"error": "Failed to fetch images", "response": response.text}), response.status_code

# 🚀 Uptime Robot Route (Prevents Render from Sleeping)
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "alive"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
