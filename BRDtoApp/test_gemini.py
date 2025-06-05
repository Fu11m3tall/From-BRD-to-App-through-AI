import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env variables
load_dotenv()

# Read the API key
api_key = os.getenv("GEMINI_API_KEY")

# IMPORTANT: Check if it actually loaded
if not api_key:
    raise ValueError("API key not found. Make sure your .env file is set correctly.")

# Configure Gemini with your API key
genai.configure(api_key=api_key)

# Use Gemini Flash (fast & free)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# Send a prompt
response = model.generate_content("What is 2 + 2?")
print(response.text)
