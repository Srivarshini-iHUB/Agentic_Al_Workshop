import os

# API Configuration
GOOGLE_API_KEY = "AIzaSyBHEVrruMH7quV5ChBk5cmnzTsN-KlBhvE"

# Task Types
TASKS = [
    "Leetcode", "Linkedin Article", "Linkedin Connect",
    "Business Card", "DT bootcamp", "Hackathon", "Gen AI Bootcamp"
]

# File Paths
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
TASKS_FILE = os.path.join(DATA_DIR, "okr_tasks.json")

# Create data directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True) 