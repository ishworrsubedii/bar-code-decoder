"""
Created By: ishwor subedi
Date: 2024-04-13
"""
import os
import requests
from bs4 import BeautifulSoup
import json


def save_image(url, directory):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(os.path.join(directory, os.path.basename(url)), 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Image saved: {url}")
        else:
            print(f"Failed to save image: {url}")
    except Exception as e:
        print(f"Error saving image: {e}")


def scrape_images_from_url(url, directory, num_images):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Google uses JavaScript to load images dynamically, so we extract image URLs from the page source
        scripts = soup.find_all('script')
        for script in scripts:
            if 'AF_initDataCallback' in str(script):
                script_text = str(script)
                start_index = script_text.find('{"key":"ds:1"')
                if start_index != -1:
                    end_index = script_text.find('};', start_index) + 1
                    json_data = json.loads(script_text[start_index:end_index])
                    for item in json_data['data']:
                        img_url = item['ou']
                        save_image(img_url, directory)
                        num_images -= 1
                        if num_images == 0:
                            break
                if num_images == 0:
                    break
    except Exception as e:
        print(f"Error scraping images: {e}")


if __name__ == '__main__':

    # Example usage:
    google_image_url = "https://www.google.com/search?sca_esv=e578d9453acfd45f&sxsrf=ACQVn08NX5Hec2aw8P1CbX45YZKVLMYVJg:1713000123891&q=US+driver%27s+license&uds=AMwkrPuHEX7vBCBXODUSNshYogAEAZp1j0iJzkImN51uktNpDR7NlHcpoeIajT_aI-HSiC_WGz73glFtOywNPLmf5pQHyvtuiQu1zZhry6hjf62LDHEOn64hA9iTv6EsgGHZyQSBcImaujO7hvqbzT3RA2QsqWx6XLxNnBrX3JTmRP-hxVh2EaSuO-MQmFIihU92GCbdQhxrOhu1dKxB4dVMjKKgenZo2E2_ec4xF19pUlyLQr2lZV1pS4YKLr_yPaXy9HSQfh6UUVXRUtePI3Z9xPQiJqzFOFOPMDh7iRF39Dc0grKWRqE&udm=2&prmd=invsmbz&sa=X&ved=2ahUKEwjuuonf7r6FAxUlQ2cHHcBSAd0QtKgLegQIJBAB&biw=1920&bih=972"
    num_images = 10
    directory = "resources/driver_licence"

    if not os.path.exists(directory):
        os.makedirs(directory)

    scrape_images_from_url(google_image_url, directory, num_images)
