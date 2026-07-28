import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://dummyjson.com")
BREW_BASE_URL = os.getenv("BREW_BASE_URL", "https://api.openbrewerydb.org/v1")
TIMEOUT = int(os.getenv("TIMEOUT", "10"))
