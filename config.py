
# Configuration settings for the project



# Configuration settings for the project

from dotenv import load_dotenv
import os


load_dotenv()

# API key for Deepgram
API_KEY = os.getenv("DG_API_KEY")

# File path for saving the final transcript
TEXT_FILE = "attempts/final_transcript.txt"

TWILIO_AUTH_TOKEN= os.getenv("TWILIO_AUTH_TOKEN")

TWILIO_ACCOUNT_SID= os.getenv("ACCOUNT_SID")