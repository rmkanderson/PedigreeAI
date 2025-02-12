import streamlit as st
import pytesseract
from PIL import Image
import graphviz

st.title("PedigreeAI: Family Health History Scanner")

# Camera input option
uploaded_file = st.camera_input("Take a photo of your handwritten list")  

if uploaded_file:
    # Convert the image for processing
    image = Image.open(uploaded_file)
    st.image(image, caption="Captured Image", use_column_width=True)

    # Extract text using OCR
    extracted_text = pytesseract.image_to_string(image)
    
    st.subheader("Extracted Text")
    st.text_area("Edit the extracted text if needed:", value=extracted_text, height=150)

# Upload image section
uploaded_file = st.file_uploader("Upload a handwritten list (image format)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Extract text using OCR
    extracted_text = pytesseract.image_to_string(image)
    
    st.subheader("Extracted Text")
    st.text_area("Edit the extracted text if needed:", value=extracted_text, height=150)

    def parse_family_text(text):
        """
        Parses the extracted text into structured format.
        Assumes "Name, Relation, Condition" format for now.
        """
        family = []
        lines = text.split("\n")
        for line in lines:
            parts = line.split(",")  # Splitting by commas
            if len(parts) == 3:
                family.append({"name": parts[0].strip(), "relation": parts[1].strip(), "condition": parts[2].strip()})
        return family

    family_data = parse_family_text(extracted_text)

    # Generate proband diagram
    def generate_proband_diagram(family_data):
        """
        Creates a proband diagram using Graphviz.
        """
        dot = graphviz.Digraph(format='png')

        # Add nodes for each family member
        for member in family_data:
            label = f"{member['name']}\n({member['condition']})"
            shape = "circle" if "female" in member["relation"].lower() else "square"
            dot.node(member["name"], label=label, shape=shape)

            # Example: Connect parents to proband (needs refinement)
            if "parent" in member["relation"].lower():
                dot.edge(member["name"], "Proband")

        return dot

    if st.button("Generate Proband Diagram"):
        st.subheader("Proband Diagram")
        proband_diagram = generate_proband_diagram(family_data)
        st.graphviz_chart(proband_diagram)
