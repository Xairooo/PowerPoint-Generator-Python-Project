import os
import requests
import json
import io
def fallback_string(val):
    if isinstance(val, list):
        return "\n".join(val)
    return str(val)

def search_unsplash_images(keyword):
    UNSPLASH_API_URL = f'https://api.unsplash.com/search/photos?query={keyword}&per_page=1'
    UNSPLASH_API_KEY = os.getenv('UNPLASH_API_KEY')
    print("URL:", UNSPLASH_API_URL) # Debug
    headers = {
        'Authorization': f'Client-ID {UNSPLASH_API_KEY}',
        'Accept-Version': 'v1'
    }
    response = requests.get(UNSPLASH_API_URL, headers=headers)
    # print("Response Status Code:", response.status_code) # Debug
    # print("Response Content:", response.text) # Debug
    data = json.loads(response.text)
    if 'results' in data:
        if len(data['results']) > 0:
            return data['results'][0]['urls']['regular']
    return None

def create_image_stream(img_path):
    image_data = requests.get(img_path).content
    # load image into BytesIO object
    return io.BytesIO(image_data)