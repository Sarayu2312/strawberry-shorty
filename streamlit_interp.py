import streamlit as st
import pandas as pd
import ollama

def query_ollama(model: str, prompt: str):
    """Sends a request to Ollama and returns the response using the Python client."""
    try:
        # Call the Ollama generate method
        response = ollama.generate(model=model, prompt=prompt)
        
        # Print for debugging
        print(f"Response received: {response.keys() if hasattr(response, 'keys') else type(response)}")
        
        # Return the response text
        if isinstance(response, dict):
            return response.get('response', 'No response text found')
        else:
            return str(response)
    except Exception as e:
        print(f"Error calling Ollama: {str(e)}")
        return f"Error: {str(e)}"

# Streamlit UI
st.title("Ollama Model Interface")

# Select model
model_name = st.text_input("Enter model name:", "llama2")

# User input
user_input = st.text_area("Enter your prompt:")

# File uploader
uploaded_file = st.file_uploader("Upload a file (CSV, TXT, etc.)", type=["csv", "txt", "json"])

# Process uploaded file
if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1]
    
    # Handle different file types
    if file_type == "csv":
        df = pd.read_csv(uploaded_file)
        st.write("Preview of uploaded CSV:")
        st.dataframe(df)
        
        # Option to include CSV data in prompt
        if st.checkbox("Include CSV data in prompt"):
            csv_string = df.to_string()
            user_input = f"{user_input}\n\nCSV Data:\n{csv_string}"
            
    elif file_type == "txt":
        text = uploaded_file.read().decode("utf-8")
        st.write("File Contents:")
        st.text(text)
        
        # Option to include text file content in prompt
        if st.checkbox("Include text file content in prompt"):
            user_input = f"{user_input}\n\nFile Content:\n{text}"
            
    elif file_type == "json":
        import json
        json_data = json.load(uploaded_file)
        st.json(json_data)
        
        # Option to include JSON data in prompt
        if st.checkbox("Include JSON data in prompt"):
            json_string = json.dumps(json_data, indent=2)
            user_input = f"{user_input}\n\nJSON Data:\n{json_string}"

# Generate button
if st.button("Generate Response"):
    if user_input.strip():
        with st.spinner("Generating response..."):
            print(f"Querying model '{model_name}' with prompt: {user_input[:100]}...")
            output = query_ollama(model_name, user_input)
        
        st.subheader("Response:")
        st.write(output)
    else:
        st.warning("Please enter a prompt.")

# Optional: Add a status indicator for Ollama service
try:
    # Try to list available models to check if Ollama is running
    models = ollama.list()
    st.sidebar.success("✅ Ollama service is running")
    
    # Display available models
    if isinstance(models, dict) and 'models' in models:
        model_list = [model['name'] for model in models['models']]
        st.sidebar.write("Available models:")
        st.sidebar.write(", ".join(model_list))
except Exception as e:
    st.sidebar.error(f"❌ Ollama service not available: {str(e)}")
    st.sidebar.info("Make sure Ollama is running on your system.")