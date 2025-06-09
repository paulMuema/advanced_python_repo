#render_template is used to render HTML templates
#request is used to handle incoming requests or receives user input from frontend
#jsonify sends back chatbot responses
import sqlite3  # Importing SQLite3 for database operations
import re
from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
#Transformers is a library that provides pre-trained models for natural language processing tasks - Giving access to the Hugging Face model
#Torch runs the model (DialoGPT is built with PyTorch)
import torch

app = Flask(__name__) #app instance

#Load DialoGPT model and tokenizer - converts text to tokens and vice versa
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Chat History (Memory)
chat_history_ids = None #stores the conversation history so chatbot has context

known_locations = ['kilimani', 'westlands', 'parklands', 'cbd', 'kileleshwa']

keywords = ['property', 'apartment', 'house', 'rent', 'buy', 'listings']

def extract_price(text):
    # Regular expression to find price in KES
    match = re.search(r"(under|less than|below)\s?(\d{1,3}(?:[,]\d{3})*|\d+)(k)?", text.lower())
    if match:
        number = match.group(2).replace(',', '')
        if match.group(3):
            return int(number) * 1000  # Convert to KES if 'k' is present
    return 100000 # default cap

def extract_location(text):
    for location in known_locations:
        if location in text.lower():
            return location.capitalize()
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global chat_history_ids
    user_input = request.json.get('message')
    print("User input:", user_input)

    # Simple logic to detect property query

    # Check if the user input contains any property-related keywords
    if any(keyword in user_input.lower() for keyword in keywords):
        # Connect to the SQLite database
        conn = sqlite3.connect('properties.db')
        cursor = conn.cursor()

        # Query the database for property listings
        cursor.execute("SELECT title, location, price, bedrooms, description, image_url FROM listings WHERE price <= 100000")
        properties = cursor.fetchall()

        # Close the database connection
        conn.close()

        if properties:
            # Format the property listings for the response
            listings = "\n".join([f"{r[0]} in {r[1]} - KES {r[2]}" for r in properties])
            return jsonify({"reply": f"Here are some property listings:\n{listings}"})
        else:
            return jsonify({"reply": "Sorry, I couldn't find any property listings."})
    try:
        # Encode the new user input, add the eos_token and return a tensor in Pytorch
        #eos_token or end-of-sequence token is the end of sentence token, used to signify the end of a user's input
        new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

        # Append the new user input tokens to the chat history
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if chat_history_ids is not None else new_user_input_ids

        # Keep only last 1000 tokens
        if bot_input_ids.shape[-1] > 1000:
            bot_input_ids = bot_input_ids[:, -1000:]

        # Generate Model Response
        chat_history_ids = model.generate(
            bot_input_ids,
            max_length=1000,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.75
        )

        #pretty print last output tokens from bot
        print("DialoGPT: {}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))

        # Decode response
        response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        print("Bot response:", response)
        return jsonify({"reply": response})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"reply": "Sorry, I couldn't process that."})

if __name__ == '__main__':
    app.run(debug=True)