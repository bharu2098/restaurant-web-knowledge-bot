import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Gemini API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Groq API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")