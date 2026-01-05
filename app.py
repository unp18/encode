# app.py
import streamlit as st
from utils import get_product_details
from ai_logic import analyze_ingredients, extract_ingredients_from_image

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Food Co-Pilot", page_icon="🍏")

API_KEY = "AIzaSyBH5aQV3cOsNRfZ0l6J84qCR8vXFDkgrOc"

# ---------------- UI HEADER ----------------
st.title("🍏 AI-Native Food Co-Pilot")
st.markdown("Understand food with **reasoning**, not raw data.")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Debug Mode")
demo_mode = st.sidebar.checkbox("Use Demo Data")

product_data = None

# ---------------- DEMO MODE ----------------
if demo_mode:
    product_data = {
        "name": "Diet Coke",
        "ingredients_text": (
            "Carbonated Water, Caramel Color, Aspartame, "
            "Phosphoric Acid, Potassium Benzoate, Caffeine."
        ),
        "image_url": "https://images.openfoodfacts.org/images/products/004/900/000/0443/front_en.38.400.jpg"
    }
    st.info("Using Demo Data (Diet Coke)")

# ---------------- USER INPUT ----------------
else:
    input_method = st.radio(
        "Choose Input Method:",
        ["Enter Barcode", "Paste Ingredients", "Upload Image"]
    )

    # ---- Barcode ----
    if input_method == "Enter Barcode":
        barcode = st.text_input("Enter Barcode (Try: 5449000000996)")
        if barcode:
            with st.spinner("Fetching product data..."):
                product_data = get_product_details(barcode)
                if not product_data:
                    st.error("Product not found.")

    # ---- Manual Paste ----
    elif input_method == "Paste Ingredients":
        name = st.text_input("Product Name")
        ingredients = st.text_area("Paste Ingredients List")
        if name and ingredients:
            product_data = {
                "name": name,
                "ingredients_text": ingredients,
                "image_url": None
            }

    # ---- Image Upload ----
    elif input_method == "Upload Image":
        uploaded_image = st.file_uploader(
            "Upload food label image (ingredients side)",
            type=["jpg", "jpeg", "png"]
        )

        if uploaded_image:
            st.image(uploaded_image, caption="Uploaded Image", width=250)

            with st.spinner("🔍 Reading ingredients from image..."):
                extracted_text = extract_ingredients_from_image(
                    API_KEY,
                    uploaded_image
                )

            st.subheader("Extracted Ingredients")
            st.write(extracted_text)

            product_data = {
                "name": "Image-based Product",
                "ingredients_text": extracted_text,
                "image_url": None
            }

# ---------------- DISPLAY PRODUCT ----------------
if product_data:
    st.markdown("---")
    st.subheader(product_data["name"])

    if product_data.get("image_url"):
        st.image(product_data["image_url"], width=150)

    with st.expander("View Raw Ingredients"):
        st.write(product_data["ingredients_text"])

    # ---------------- AI ANALYSIS ----------------
    if st.button("Analyze with AI Context"):
        with st.spinner("🤖 Reasoning about health trade-offs..."):
            analysis = analyze_ingredients(
                API_KEY,
                product_data["name"],
                product_data["ingredients_text"]
            )

        st.markdown("---")
        st.markdown(analysis)

        # ---------------- FUTURE EXTENSION ----------------
        st.markdown("---")
        st.write("🔄 Adjust Context (V2 Feature)")
        if st.button("I'm an athlete"):
            st.info("Would re-run analysis focusing on performance & recovery.")
