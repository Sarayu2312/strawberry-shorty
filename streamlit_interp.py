import streamlit as st
import pandas as pd
import ollama
import json
import subprocess
import os
import tempfile
import matplotlib.pyplot as plt
import seaborn as sns

def query_ollama(model: str, conversation: list):
    """Sends a request to Ollama and returns the response using the Python client."""
    try:
        # Call the Ollama chat method
        response = ollama.chat(model=model, messages=conversation).model_dump()
        print(response)
        
        # Return the response text
        if isinstance(response, dict):
            return response['message']['content'] if 'message' in response else str(response)
        else:
            return str(response)
    except Exception as e:
        print(f"Error calling Ollama: {str(e)}")
        return f"Error: {str(e)}"

# Initialize session state for conversation history if not already initialized
if 'history' not in st.session_state:
    st.session_state.history = []
    st.session_state.conv_history = []

# Try to list available models to check if Ollama is running
models = ollama.list().model_dump()
st.sidebar.success("✅ Ollama service is running")

# Display available models
if isinstance(models, dict) and 'models' in models:
    model_list = [model['model'] for model in models['models']]

# Streamlit UI
st.title("Ollama Model Interface")

# Select model
model_name = st.selectbox("Select a model:", options=model_list)

# User input
user_input = st.text_area("Enter your prompt:")
user_chat_input = user_input 

# File uploader
uploaded_file = st.file_uploader("Upload a file (CSV, TXT, etc.)", type=["csv", "txt", "json"], )

# Process uploaded file
if uploaded_file is not None:
    # Extract file name and display it without showing the raw file contents
    file_name = uploaded_file.name
    st.write(f"File uploaded: {file_name}")
    
    file_type = file_name.split(".")[-1]
    
    # Handle CSV file type
    if file_type == "csv":
        df = pd.read_csv(uploaded_file)
        
        # Convert DateTime to proper datetime format
        if "DateTime" in df.columns:
            df["DateTime"] = pd.to_datetime(df["DateTime"])
        
        # Summary statistics of numerical columns
        summary_stats = df.describe()
        st.subheader("Summary Statistics:")
        st.dataframe(summary_stats)
        
        # Plot time-series trends for key variables
        fig, axes = plt.subplots(3, 2, figsize=(14, 12))
        
        # Wind Speed at Different Heights
        for height, ax in zip(["1m", "3m", "7m", "13m"], axes[0]):
            if f"WindSpeed_{height}[m/s]" in df.columns:
                df.plot(x="DateTime", y=f"WindSpeed_{height}[m/s]", ax=ax, title=f"Wind Speed at {height}")
        
        # Temperature at Different Heights
        for height, ax in zip(["1m", "3m", "7m", "13m"], axes[1]):
            if f"Temp_{height}[degC]" in df.columns:
                df.plot(x="DateTime", y=f"Temp_{height}[degC]", ax=ax, title=f"Temperature at {height}")
        
        # CO2 Concentration Trends
        if "CO2_MNT[ppm]" in df.columns:
            df.plot(x="DateTime", y="CO2_MNT[ppm]", ax=axes[2][0], title="CO2 Concentration (MNT)")
        if "CO2_desert[ppm]" in df.columns:
            df.plot(x="DateTime", y="CO2_desert[ppm]", ax=axes[2][1], title="CO2 Concentration (Desert)")
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Correlation Heatmap of Key Environmental Factors
        plt.figure(figsize=(12, 8))
        cols = [col for col in df.columns if col in ["WindSpeed_1m[m/s]", "Temp_1m[degC]", "RH_1m[%]", "CO2_MNT[ppm]", "CO2_desert[ppm]", "AirPress_hPa"]]
        if cols:
            corr_matrix = df[cols].corr()
            sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
            plt.title("Correlation Heatmap of Key Environmental Variables")
            st.pyplot(plt)
        
        # Option to include CSV data in the prompt (show a preview if selected)
        if st.checkbox("Include CSV summary in prompt"):
            summary_string = summary_stats.to_string()
            user_chat_input = user_input
            user_input = f"{user_input}\n\nCSV Summary:\n{summary_string}"[:10_000]
            print(len(user_input))

    # Handle TXT file type
    elif file_type == "txt":
        text = uploaded_file.read().decode("utf-8")
        
        # Option to include text file content in prompt
        if st.checkbox("Include text file content in prompt"):
            user_chat_input = user_input
            user_input = f"{user_input}\n\nFile Content:\n{text[:5000]}"
            
    # Handle JSON file type
    elif file_type == "json":
        json_data = json.load(uploaded_file)
        
        # Option to include JSON data in prompt
        if st.checkbox("Include JSON data in prompt"):
            json_string = json.dumps(json_data, indent=2)
            user_chat_input = user_input
            user_input = f"{user_input}\n\nJSON Data:\n{json_string}"

# Handle chat submission
if st.button("Generate Conversation"):
    if user_input.strip():
        # Append the user's message to the conversation history
        st.session_state.history.append({"role": "user", "message": user_input})
        st.session_state.conv_history.append({"role": "user", "message": user_chat_input})
        
        # Prepare the conversation format for the chat method
        messages = [{"role": "user", "content": entry['message']} for entry in st.session_state.history]
        
        with st.spinner("Generating response..."):
            # Get the model's response using the chat-based query
            output = query_ollama(model_name, messages)
            
        # Append the model's response to the conversation history
        st.session_state.history.append({"role": "model", "message": output})
        st.session_state.conv_history.append({"role": "model", "message": output})
        
        # Display the conversation history
        st.subheader("Conversation:")
        for entry in st.session_state.conv_history:
            if entry["role"] == "user":
                st.markdown(f"**You**: {entry['message']}")
            else:
                st.markdown(f"**Model**: {entry['message']}")
        
        # Check if the model's response is a Python script
        if st.checkbox("Execute Generated Script"):
            script_content = output
            
            # Save the script to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
                temp_file.write(script_content.encode('utf-8'))
                temp_file_path = temp_file.name
            
            # Execute the script using subprocess
            try:
                result = subprocess.run(["python", temp_file_path], capture_output=True, text=True, check=True)
                st.success(f"Script executed successfully:\n{result.stdout}")
            except subprocess.CalledProcessError as e:
                st.error(f"Error executing script:\n{e.stderr}")
            finally:
                # Clean up the temporary file
                os.remove(temp_file_path)
    else:
        st.warning("Please enter a message.")