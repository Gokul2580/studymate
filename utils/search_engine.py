"""
Semantic search engine using FAISS and sentence transformers
"""
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import streamlit as st
from typing import List, Tuple
import pickle
import os

class SearchEngine:
    def __init__(self):
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.dimension = self.embedder.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatL2(self.dimension)
        self.documents = []
        self.document_metadata = []
    
    def add_documents(self, chunks: List[str], document_name: str = ""):
        """Add document chunks to the search index"""
        if not chunks:
            return
        
        with st.spinner("🔍 Creating embeddings..."):
            embeddings = self.embedder.encode(chunks, convert_to_numpy=True)
            self.index.add(embeddings)
            self.documents.extend(chunks)
            
            # Store metadata for each chunk
            for i, chunk in enumerate(chunks):
                self.document_metadata.append({
                    "document_name": document_name,
                    "chunk_index": i,
                    "text_preview": chunk[:100] + "..." if len(chunk) > 100 else chunk
                })
    
    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, float, dict]]:
        """Search for relevant documents"""
        if not self.documents:
            return []
        
        query_vec = self.embedder.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_vec, top_k)
        
        results = []
        for distance, idx in zip(distances[0], indices[0]):
            if idx < len(self.documents):
                results.append((
                    self.documents[idx],
                    float(distance),
                    self.document_metadata[idx]
                ))
        
        return results
    
    def get_similar_questions(self, current_question: str, chat_history: List[dict], top_k: int = 3) -> List[str]:
        """Find similar previously asked questions"""
        if not chat_history:
            return []
        
        previous_questions = [item['question'] for item in chat_history if item['question'] != current_question]
        
        if not previous_questions:
            return []
        
        # Encode current question and previous questions
        current_vec = self.embedder.encode([current_question], convert_to_numpy=True)
        prev_vecs = self.embedder.encode(previous_questions, convert_to_numpy=True)
        
        # Calculate similarities
        similarities = np.dot(prev_vecs, current_vec.T).flatten()
        
        # Get top similar questions
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        similar_questions = [previous_questions[i] for i in top_indices if similarities[i] > 0.5]
        
        return similar_questions
    
    def save_index(self, filepath: str):
        """Save the search index to disk"""
        try:
            # Save FAISS index
            faiss.write_index(self.index, f"{filepath}.index")
            
            # Save documents and metadata
            with open(f"{filepath}.pkl", "wb") as f:
                pickle.dump({
                    "documents": self.documents,
                    "metadata": self.document_metadata
                }, f)
            
            return True
        except Exception as e:
            st.error(f"Error saving index: {str(e)}")
            return False
    
    def load_index(self, filepath: str):
        """Load the search index from disk"""
        try:
            if os.path.exists(f"{filepath}.index") and os.path.exists(f"{filepath}.pkl"):
                # Load FAISS index
                self.index = faiss.read_index(f"{filepath}.index")
                
                # Load documents and metadata
                with open(f"{filepath}.pkl", "rb") as f:
                    data = pickle.load(f)
                    self.documents = data["documents"]
                    self.document_metadata = data["metadata"]
                
                return True
        except Exception as e:
            st.error(f"Error loading index: {str(e)}")
        
        return False
    
    def clear_index(self):
        """Clear the search index"""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.documents = []
        self.document_metadata = []
