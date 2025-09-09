"""
Text-to-Speech engine for StudyMate
"""
import streamlit as st
from gtts import gTTS
import io
import base64
from pydub import AudioSegment
import tempfile
import os
from typing import List, Dict
import time

class TTSEngine:
    def __init__(self):
        self.supported_languages = {
            'en': 'English',
            'es': 'Spanish', 
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese'
        }
        self.current_audio = None
        
    def text_to_speech(self, text: str, language: str = 'en', slow: bool = False) -> bytes:
        """Convert text to speech and return audio bytes"""
        try:
            if not text.strip():
                return None
                
            # Create TTS object
            tts = gTTS(text=text, lang=language, slow=slow)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tts.save(tmp_file.name)
                
                # Read the audio file
                with open(tmp_file.name, 'rb') as audio_file:
                    audio_bytes = audio_file.read()
                
                # Clean up
                os.unlink(tmp_file.name)
                
                return audio_bytes
                
        except Exception as e:
            st.error(f"Error generating speech: {str(e)}")
            return None
    
    def create_audio_book(self, chapters: List[Dict], language: str = 'en') -> bytes:
        """Create an audio book from multiple text chapters"""
        try:
            combined_audio = AudioSegment.empty()
            
            progress_bar = st.progress(0)
            total_chapters = len(chapters)
            
            for i, chapter in enumerate(chapters):
                st.info(f"🎙️ Processing Chapter {i+1}: {chapter.get('title', f'Chapter {i+1}')}")
                
                # Add chapter title
                title_text = f"Chapter {i+1}. {chapter.get('title', '')}"
                title_audio_bytes = self.text_to_speech(title_text, language)
                
                if title_audio_bytes:
                    title_audio = AudioSegment.from_mp3(io.BytesIO(title_audio_bytes))
                    combined_audio += title_audio
                    combined_audio += AudioSegment.silent(duration=1000)  # 1 second pause
                
                # Add chapter content
                content_audio_bytes = self.text_to_speech(chapter['content'], language)
                if content_audio_bytes:
                    content_audio = AudioSegment.from_mp3(io.BytesIO(content_audio_bytes))
                    combined_audio += content_audio
                    combined_audio += AudioSegment.silent(duration=2000)  # 2 second pause
                
                progress_bar.progress((i + 1) / total_chapters)
            
            progress_bar.empty()
            
            # Export combined audio
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                combined_audio.export(tmp_file.name, format="mp3")
                
                with open(tmp_file.name, 'rb') as audio_file:
                    audio_bytes = audio_file.read()
                
                os.unlink(tmp_file.name)
                return audio_bytes
                
        except Exception as e:
            st.error(f"Error creating audio book: {str(e)}")
            return None
    
    def get_audio_player_html(self, audio_bytes: bytes, autoplay: bool = False) -> str:
        """Generate HTML audio player"""
        if not audio_bytes:
            return ""
            
        audio_base64 = base64.b64encode(audio_bytes).decode()
        autoplay_attr = "autoplay" if autoplay else ""
        
        return f"""
        <audio controls {autoplay_attr} style="width: 100%; margin: 10px 0;">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        """
    
    def create_download_link(self, audio_bytes: bytes, filename: str = "studymate_audio.mp3") -> str:
        """Create download link for audio file"""
        if not audio_bytes:
            return ""
            
        audio_base64 = base64.b64encode(audio_bytes).decode()
        
        return f"""
        <a href="data:audio/mp3;base64,{audio_base64}" 
           download="{filename}"
           style="display: inline-block; padding: 10px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                  color: white; text-decoration: none; border-radius: 25px; font-weight: 600; margin: 10px 0;">
            📥 Download Audio Book
        </a>
        """
