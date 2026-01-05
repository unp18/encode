# ai_logic.py
import google.generativeai as genai

def analyze_ingredients(api_key, product_name, ingredients_text):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash') 

    prompt = f"""
    You are an AI-Native Health Co-Pilot.
    
    Product: "{product_name}"
    Ingredients: "{ingredients_text}"

    Rules:
    1. Infer user intent automatically.
    2. Explain health trade-offs clearly.
    3. Explicitly mention uncertainty if data is unclear.
    4. Keep output short, friendly, and readable.

    Format:
    ## 🧐 The Verdict
    [One-line decision]

    ## ⚖️ The Trade-off
    [Pros vs Cons]

    ## 🧠 Cognitive Load Reduction
    [Explain one complex ingredient in simple terms]
    """

    response = model.generate_content(prompt)
    return response.text


# ai_logic.py
import google.generativeai as genai
from PIL import Image
import io

def extract_ingredients_from_image(api_key, image_file):
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.5-flash")

    # Convert uploaded file → bytes
    image_bytes = image_file.read()

    prompt = """
    You are reading a food package label.

    Task:
    - Extract ONLY the ingredients list
    - Ignore nutrition facts and marketing text
    - Return plain text ingredients
    - If ingredients are unclear or missing, say: "Ingredients unclear"
    """

    response = model.generate_content(
        contents=[
            {
                "role": "user",
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": image_file.type,
                            "data": image_bytes,
                        }
                    },
                ],
            }
        ]
    )

    return response.text
