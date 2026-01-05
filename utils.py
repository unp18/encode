# utils.py
import requests

def get_product_details(barcode):
    """
    Fetches product ingredients from OpenFoodFacts using the barcode.
    """
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 1:  # Product found
            product = data['product']
            return {
                "name": product.get("product_name", "Unknown Product"),
                "ingredients_text": product.get("ingredients_text", "No ingredients listed."),
                "image_url": product.get("image_url", None),
                "nutriments": product.get("nutriments", {})
            }
    return None
