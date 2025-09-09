"""
Advanced PDF reader with highlighting and automation
"""
import streamlit as st
import fitz  # PyMuPDF
import base64
from typing import List, Tuple, Dict
import time
import re

class PDFReader:
    def __init__(self):
        self.current_pdf = None
        self.current_page = 0
        self.total_pages = 0
        self.reading_speed = 200  # words per minute
        
    def load_pdf(self, pdf_file) -> bool:
        """Load PDF file"""
        try:
            self.current_pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")
            self.total_pages = len(self.current_pdf)
            self.current_page = 0
            return True
        except Exception as e:
            st.error(f"Error loading PDF: {str(e)}")
            return False
    
    def get_page_text(self, page_num: int) -> str:
        """Get text from specific page"""
        if not self.current_pdf or page_num >= self.total_pages:
            return ""
        
        try:
            page = self.current_pdf[page_num]
            return page.get_text("text")
        except Exception as e:
            st.error(f"Error extracting text from page {page_num}: {str(e)}")
            return ""
    
    def get_page_image(self, page_num: int, zoom: float = 2.0) -> bytes:
        """Get page as image"""
        if not self.current_pdf or page_num >= self.total_pages:
            return None
        
        try:
            page = self.current_pdf[page_num]
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            return img_data
        except Exception as e:
            st.error(f"Error rendering page {page_num}: {str(e)}")
            return None
    
    def highlight_text_in_page(self, page_num: int, text_to_highlight: str) -> bytes:
        """Highlight specific text in page and return as image"""
        if not self.current_pdf or page_num >= self.total_pages:
            return None
        
        try:
            page = self.current_pdf[page_num]
            
            # Search for text
            text_instances = page.search_for(text_to_highlight)
            
            # Highlight found text
            for inst in text_instances:
                highlight = page.add_highlight_annot(inst)
                highlight.set_colors(stroke=[1, 1, 0])  # Yellow highlight
                highlight.update()
            
            # Render page with highlights
            mat = fitz.Matrix(2.0, 2.0)
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            
            return img_data
        except Exception as e:
            st.error(f"Error highlighting text: {str(e)}")
            return None
    
    def get_reading_segments(self, text: str, words_per_segment: int = 50) -> List[str]:
        """Split text into reading segments"""
        words = text.split()
        segments = []
        
        for i in range(0, len(words), words_per_segment):
            segment = " ".join(words[i:i + words_per_segment])
            segments.append(segment)
        
        return segments
    
    def estimate_reading_time(self, text: str) -> float:
        """Estimate reading time in minutes"""
        word_count = len(text.split())
        return word_count / self.reading_speed
    
    def create_pdf_viewer_html(self, pdf_bytes: bytes) -> str:
        """Create HTML PDF viewer"""
        pdf_base64 = base64.b64encode(pdf_bytes).decode()
        
        return f"""
        <div style="width: 100%; height: 600px; border: 2px solid #e1e8ed; border-radius: 10px; overflow: hidden;">
            <embed src="data:application/pdf;base64,{pdf_base64}" 
                   type="application/pdf" 
                   width="100%" 
                   height="100%"
                   style="border: none;">
        </div>
        """
    
    def get_pdf_metadata(self) -> Dict:
        """Get PDF metadata"""
        if not self.current_pdf:
            return {}
        
        metadata = self.current_pdf.metadata
        return {
            "title": metadata.get("title", "Unknown"),
            "author": metadata.get("author", "Unknown"),
            "subject": metadata.get("subject", ""),
            "creator": metadata.get("creator", ""),
            "producer": metadata.get("producer", ""),
            "creation_date": metadata.get("creationDate", ""),
            "modification_date": metadata.get("modDate", ""),
            "pages": self.total_pages
      }
