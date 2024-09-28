# streamlit_app.py

import streamlit as st
import pandas as pd
from generator import generate_synthetic_data

# Set up the Streamlit app
st.title("Synthetic Data Generator")

# Input API Key
api_key = st.text_input("Enter your OpenAI API key:", type="password")

# File upload widget
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

# Input: number of rows to generate
num_rows = st.number_input("Number of rows to generate", min_value=1, step=1, value=10)

# Button to generate the synthetic data
if st.button("Generate Data"):
    if uploaded_file is not None and api_key:
        # Save the uploaded file locally to use in the function
        with open("temp.xlsx", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Call the function from util.py
        generated_df = generate_synthetic_data(api_key, "temp.xlsx", num_rows=num_rows)

        # Load the original data for combination
        original_df = pd.read_excel("temp.xlsx")

        # Show the generated data in the Streamlit app
        st.write("Generated Synthetic Data:")
        st.dataframe(generated_df)

        # Combine original and generated data for download
        combined_df = pd.concat([original_df, generated_df], ignore_index=True)

        # Allow users to download the combined data
        combined_csv = combined_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Combined Data as CSV",
            data=combined_csv,
            file_name="combined_data.csv",
            mime="text/csv",
        )
    else:
        st.error("Please upload an Excel file and enter your API key.")
