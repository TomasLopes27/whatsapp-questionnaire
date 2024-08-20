from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(dotenv_path='example.env')
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")
WEBHOOKVERIFYTOKEN = os.getenv("VERIFY_TOKEN") 
