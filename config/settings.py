"""
Configuration settings for StudyMate Application
"""
import os

# Watsonx Configuration
WATSONX_CONFIG = {
    "api_key": "XeXlJhF1yW0sEy51ZXydRZyLUskTeSgf6-n-tZ4ZBDHg",
    "project_id": "4696d5b0-60ad-4653-988d-82aee1ad01d1",
    "url": "https://jp-tok.ml.cloud.ibm.com",
    "model_id": "ibm/granite-3-8b-instruct"
}

# Model Parameters
MODEL_PARAMS = {
    "max_new_tokens": 400,
    "temperature": 0.2,
    "chunk_size": 500,
    "chunk_overlap": 50,
    "search_results": 3
}

# UI Configuration
UI_CONFIG = {
    "page_title": "StudyMate - AI PDF Q&A Assistant",
    "page_icon": "📚",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Team Members
TEAM_MEMBERS = [
    {
        "name": "Gokul BA",
        "role": "AI Research Lead",
            },
    {
        "name": "C Nithish",
        "role": "Full Stack Developer",
           },
    {
        "name": "Manojkumar s",
        "role": "UX/UI Designer",
         }
]
