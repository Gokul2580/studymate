"""
Document processing utilities for PDF handling and text extraction
"""
import fitz  # PyMuPDF
import streamlit as st
from typing import List, Tuple

class DocumentProcessor:
    def __init__(self):
        self.supported_formats = ["pdf"]
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text from PDF file"""
        try:
            text = ""
            doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
            
            # Create progress bar
            progress_bar = st.progress(0)
            total_pages = len(doc)
            
            for i, page in enumerate(doc):
                text += page.get_text("text") + "\n"
                progress_bar.progress((i + 1) / total_pages)
            
            progress_bar.empty()
            return text
        except Exception as e:
            st.error(f"Error extracting text from PDF: {str(e)}")
            return ""
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Split text into overlapping chunks"""
        if not text.strip():
            return []
        
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        
        return chunks
    
    def get_document_stats(self, text: str) -> dict:
        """Get statistics about the document"""
        if not text:
            return {}
        
        words = text.split()
        sentences = text.split('.')
        paragraphs = [p for p in text.split('\n\n') if p.strip()]
        
        return {
            "total_characters": len(text),
            "total_words": len(words),
            "total_sentences": len([s for s in sentences if s.strip()]),
            "total_paragraphs": len(paragraphs),
            "avg_words_per_sentence": len(words) / max(len(sentences), 1)
        }
    
    def extract_key_terms(self, text: str, top_k: int = 10) -> List[str]:
        """Extract key terms from document (simple frequency-based)"""
        if not text:
            return []
        
        # Simple keyword extraction (you could enhance this with NLP libraries)
        words = text.lower().split()
        
        # Filter out common words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'are', 'was', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'shall', 'can'
        }
        
        # Count word frequency
        word_freq = {}
        for word in words:
            cleaned_word = ''.join(c for c in word if c.isalnum())
            if cleaned_word and len(cleaned_word) > 3 and cleaned_word not in stop_words:
                word_freq[cleaned_word] = word_freq.get(cleaned_word, 0) + 1
        
        # Return top k words
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:top_k]]
