import os
from flask import Flask, request, jsonify
import requests
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Load the API key from environment variables
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

# Desired image dimensions
TARGET_WIDTH = 1280
TARGET_HEIGHT = 720

def resize_image(image_url):
    """Fetches an image from a URL and resizes it to the target dimensions."""
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            image = image.resize((TARGET_WIDTH, TARGET_HEIGHT))
            
            # Save resized image to a buffer
            img_buffer = BytesIO()
            image.save(img_buffer, format="JPEG")
            img_buffer.seek(0)

            return img_buffer
        else:
            return None
    except Exception as e:
        print("Error resizing image:", str(e))
        return None

@app.route("/fetch_unsplash_images", methods=["GET"])
def fetch_unsplash_images():
    query = request.args.get("query", "")
    url = f"https://api.unsplash.com/search/photos?query={query}&per_page=2&orientation=landscape&client_id={UNSPLASH_ACCESS_KEY}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        resized_images = []

        for image in data.get("results", []):
            resized_image = resize_image(image["urls"]["regular"])
            if resized_image:
                resized_images.append({"image_url": image["urls"]["regular"]})  # Using original URL for now

        return jsonify({"images": resized_images})
    else:
        return jsonify({"error": "Failed to fetch images"}), response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
