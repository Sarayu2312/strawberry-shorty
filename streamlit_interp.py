import streamlit as st
import requests
import pandas as pd

# Define the Ollama API endpoint (modify as needed)
OLLAMA_API_URL = "http://localhost:11434/api/generate"

def query_ollama(model: str, prompt: str):
    """Sends a request to the Ollama API and returns the response."""
    payload = {"model": model, "prompt": prompt}
    response = requests.post(OLLAMA_API_URL, json=payload)
    if response.status_code == 200:
        return response.json().get("response", "No response received.")
    else:
        return f"Error: {response.status_code}, {response.text}"

# Streamlit UI
st.title("Ollama Model Interface")

# Select model
model_name = st.text_input("Enter model name:", "llama2")

# User input
user_input = st.text_area("Enter your prompt:")

# File uploader
uploaded_file = st.file_uploader("Upload a file (CSV, TXT, etc.)", type=["csv", "txt", "json"])

if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1]
    if file_type == "csv":
        df = pd.read_csv(uploaded_file)
        st.write("Preview of uploaded CSV:")
        st.dataframe(df)
    elif file_type == "txt":
        text = uploaded_file.read().decode("utf-8")
        st.write("File Contents:")
        st.text(text)
    elif file_type == "json":
        import json
        json_data = json.load(uploaded_file)
        st.json(json_data)

if st.button("Generate Response"):
    if user_input.strip():
        with st.spinner("Generating response..."):
            output = query_ollama(model_name, user_input)
        st.subheader("Response:")
        st.write(output)
    else:
        st.warning("Please enter a prompt.")

# Run this script with: streamlit run script_name.py
