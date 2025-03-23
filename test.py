import streamlit as st
from ollama import Client
import sqlite3
import os

# Initialize the Ollama client
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
client = Client(host=OLLAMA_HOST)

# Define the model names
MODEL1_NAME = os.getenv("MODEL1_NAME", "mistral")
MODEL2_NAME = os.getenv("MODEL2_NAME", "qwen2.5")

# Function to initialize the database
def init_db():
    conn = sqlite3.connect('conversations.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT,
            model1_response TEXT,
            model2_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert conversation into the database
def insert_conversation(user_input, model1_response, model2_response):
    conn = sqlite3.connect('conversations.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO conversations (user_input, model1_response, model2_response)
        VALUES (?, ?, ?)
    ''', (user_input, model1_response, model2_response))
    conn.commit()
    conn.close()

# Function to get response from a model
def get_model_response(model_name, prompt):
    try:
        response = client.chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}]
        ).model_dump()
        return response['message']['content'] if 'message' in response else str(response)
    except Exception as e:
        return f"Error: {str(e)}"

# Initialize the database
init_db()

# Streamlit app
st.title("Two Models Chat")

st.markdown("Enter a prompt, and the two models will respond in sequence.")

user_input = st.text_input("Enter your prompt:")

if st.button("Submit"):
    with st.spinner("Generating responses..."):
        # Get response from Model 1
        model1_response = get_model_response(MODEL1_NAME, user_input)
        if "Error" in model1_response:
            st.error(model1_response)
        else:
            st.write(f"**Model 1 Response:** {model1_response}")

            # Get response from Model 2
            model2_response = get_model_response(MODEL2_NAME, model1_response)
            if "Error" in model2_response:
                st.error(model2_response)
            else:
                st.write(f"**Model 2 Response:** {model2_response}")

                # Insert conversation into the database
                insert_conversation(user_input, model1_response, model2_response)

# Display conversation history as dropdown and make it collapsible
    
with st.expander("Conversation History", expanded=False):
    conn = sqlite3.connect('conversations.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM conversations ORDER BY timestamp DESC')
    conversations = cursor.fetchall()
    conn.close()
    
    # show all conversations as text
    for conv in conversations:
        st.write(f"**User Input:** {conv[1]}")
        st.write(f"**Model 1 Response:** {conv[2]}")
        st.write(f"**Model 2 Response:** {conv[3]}")
        st.write(f"**Timestamp:** {conv[4]}")
        st.markdown("---")  # Separator between conversations