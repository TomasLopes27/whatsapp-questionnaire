from dotenv import load_dotenv
import os, logging

# Configure logging to file
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - %(lineno)d - %(message)s",
    handlers=[
        logging.FileHandler("responses.log"),  # Output file for logs
    ],
)

# Load environment variables
load_dotenv(dotenv_path="example.env")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")
WEBHOOKVERIFYTOKEN = os.getenv("VERIFY_TOKEN")
