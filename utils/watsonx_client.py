"""
Watsonx AI client for handling model interactions
"""
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods
from config.settings import WATSONX_CONFIG, MODEL_PARAMS
import streamlit as st

class WatsonxClient:
    def __init__(self):
        self.credentials = {
            "url": WATSONX_CONFIG["url"],
            "apikey": WATSONX_CONFIG["api_key"]
        }
        
        self.params = {
            "decoding_method": DecodingMethods.GREEDY,
            "max_new_tokens": MODEL_PARAMS["max_new_tokens"],
            "temperature": MODEL_PARAMS["temperature"],
        }
        
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the Watsonx model"""
        try:
            self.model = Model(
                model_id=WATSONX_CONFIG["model_id"],
                credentials=self.credentials,
                params=self.params,
                project_id=WATSONX_CONFIG["project_id"]
            )
        except Exception as e:
            st.error(f"Failed to initialize Watsonx model: {str(e)}")
    
    def generate_answer(self, question, context, chat_history=""):
        """Generate answer using Watsonx model"""
        if not self.model:
            return "Model not initialized. Please check your configuration."
        
        prompt = f"""
You are StudyMate, an intelligent academic assistant designed to help students learn effectively.

Chat History:
{chat_history}

Context from Documents:
{context}

Current Question:
{question}

Instructions:
- Provide clear, accurate, and helpful answers based on the context
- If the context doesn't contain enough information, say so clearly
- Use examples when helpful
- Structure your response in a student-friendly way
- Be encouraging and supportive

Answer:
"""
        
        try:
            response = self.model.generate_text(prompt=prompt)
            
            if isinstance(response, list):
                return getattr(response[0], "text", str(response[0]))
            elif isinstance(response, dict) and "results" in response:
                return response["results"][0].get("generated_text", str(response))
            else:
                return str(response)
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def generate_summary(self, text):
        """Generate a summary of the document"""
        prompt = f"""
Please provide a comprehensive summary of the following academic document.
Include:
- Main topics covered
- Key concepts
- Important points students should focus on

Document:
{text[:3000]}  # Limit to first 3000 characters

Summary:
"""
        
        try:
            response = self.model.generate_text(prompt=prompt)
            if isinstance(response, list):
                return getattr(response[0], "text", str(response[0]))
            elif isinstance(response, dict) and "results" in response:
                return response["results"][0].get("generated_text", str(response))
            else:
                return str(response)
        except Exception as e:
            return f"Error generating summary: {str(e)}"
