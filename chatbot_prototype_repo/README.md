# 🏡 AI Property Chatbot

This is a simple AI-powered chatbot for a property management system. It helps users find property listings by chatting naturally — like asking for houses under a certain budget or in a specific location.

Built using:
- 🐍 Python Flask (backend)
- 🤖 HuggingFace DialoGPT (for natural AI conversation)
- 💾 SQLite3 (for property listings)
- 🌐 HTML/CSS/JavaScript (frontend)

---

## 🚀 Features

✅ Natural language chat with AI  
✅ Smart filtering by price and location  
✅ Dynamic responses from SQLite database  
✅ Fallback to general AI replies if input isn’t a property query

---

## 🧠 Example Prompts

- _"Show me houses under 80,000"_  
- _"Any listings in Westlands?"_  
- _"I’m looking for a 2-bedroom in Kilimani"_  
- _"Tell me a joke!"_ (fallback to AI)

---

## 📁 Project Structure

project/
├── app.py # Main Flask app and chatbot logic
├── setup_db.py # Script to create and seed SQLite database
├── properties.db # SQLite database with listings
├── templates/
│ └── index.html # Frontend chat UI
├── static/
│ └── style.css # (Optional) custom styling
└── README.md # Project documentation


---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/paulMuema/advanced_python_repo.git
cd chatbot_prototype_repo

### 2. Install Requirements

- Make sure you have Python 3.7+ installed

- pip install flask transformers torch

### 3. Set Up the Database

- Created a sample property listings table

- python setup_db.py

### 4. Run the Flask App

- python app.py

- Visit the chatbot at: http://127.0.0.1:5000

💬 How It Works
If a message mentions property-related keywords (e.g. "house", "apartment", "under 100k"), the bot:

Extracts price and location from the message

Queries a local SQLite database for matching listings

Returns relevant results

If no keywords are found, it uses DialoGPT to respond like a friendly assistant.

🔮 Future Enhancements
Extract number of bedrooms from message

Display listings as cards with images

Add admin panel to manage listings

Deploy to Render, Railway, or Heroku

🧪 Sample Listings (in setup_db.py)
2 Bedroom Apartment in Kilimani - KES 85,000

1 Bedroom Apartment in Rongai - KES 45,000

3 Bedroom House in Westlands - KES 150,000

Bedsitter in Rongai - KES 15,000