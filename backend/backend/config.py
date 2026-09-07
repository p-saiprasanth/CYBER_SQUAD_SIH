import os
from pathlib import Path
from dotenv import dotenv_values

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

config = dotenv_values(ENV_FILE)

SECRET_KEY = config.get("SECRET_KEY")
DATABASE_URL = config.get("DATABASE_URL")
NEO4J_URI = config.get("NEO4J_URI")
NEO4J_USERNAME = config.get("NEO4J_USERNAME")
NEO4J_PASSWORD = config.get("NEO4J_PASSWORD")
AI_API_KEY = config.get("AI_API_KEY")