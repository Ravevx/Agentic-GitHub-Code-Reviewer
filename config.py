# config.py
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN  = os.getenv("GITHUB_TOKEN", "")
LM_STUDIO_URL = "http://127.0.0.1:1234/v1"
LM_MODEL      = "ministral-3-3b-instruct-2512"

MAX_FILE_SIZE = 4000 #change as per model
MAX_FILES     = 10 
