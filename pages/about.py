"""
About page for StudyMate application
"""
import streamlit as st

def about_page():
    st.title("📖 About StudyMate")
    
    # Hero section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; margin-bottom: 2rem;">
        <h2 style="color: white; text-align: center; margin-bottom: 1rem;">🚀 Revolutionizing Academic Learning</h2>
        <p style="color: white; text-align: center; font-size: 1.2rem; margin-bottom: 0;">
            StudyMate is an AI-powered academic assistant that transforms how students interact with educational content.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mission and Vision
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Our Mission
        
        To democratize access to personalized learning by making academic documents interactive and accessible through cutting-edge AI technology.
        
        **We believe that:**
        - Learning should be interactive and engaging
        - AI can enhance human understanding
        - Complex documents shouldn't be barriers to knowledge
        - Every student deserves personalized academic support
        """)
    
    with col2:
        st.markdown("""
        ### 🔮 Our Vision
        
        To create a world where every student has an intelligent, patient, and knowledgeable study companion available 24/7.
        
        **Our goals:**
        - Reduce study time while improving comprehension
        - Make academic research more accessible
        - Support diverse learning styles and needs
        - Bridge the gap between complex content and understanding
        """)
    
    st.divider()
    
    # Key Features
    st.markdown("## ✨ Key Features")
    
    features = [
        {
            "icon": "🧠",
            "title": "Intelligent Q&A",
            "description": "Ask natural language questions and get contextual answers from your documents using advanced AI."
        },
        {
            "icon": "🔍",
            "title": "Semantic Search",
            "description": "Find relevant information quickly with meaning-based search that understands context and intent."
        },
        {
            "icon": "📊",
            "title": "Document Analytics",
            "description": "Get comprehensive insights, statistics, and summaries to understand document structure and content."
        },
        {
            "icon": "💬",
            "title": "Interactive Chat",
            "description": "Engage in ongoing conversations with your documents, building on previous questions and answers."
        },
        {
            "icon": "🎯",
            "title": "Context-Aware Responses",
            "description": "Receive answers that are specifically tailored to your document content and learning context."
        },
        {
            "icon": "📚",
            "title": "Multi-Format Support",
            "description": "Process various academic document formats with advanced text extraction and understanding."
        }
    ]
    
    for i in range(0, len(features), 2):
        col1, col2 = st.columns(2)
        
        with col1:
            if i < len(features):
                feature = features[i]
                st.markdown(f"""
                <div style="background-color: #f8f9fa; padding: 1.5rem; border-radius: 10px; height: 200px;">
                    <h3 style="color: #2c3e50; margin-bottom: 1rem;">{feature['icon']} {feature['title']}</h3>
                    <p style="color: #5d6d7e; line-height: 1.6;">{feature['description']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            if i + 1 < len(features):
                feature = features[i + 1]
                st.markdown(f"""
                <div style="background-color: #f8f9fa; padding: 1.5rem; border-radius: 10px; height: 200px;">
                    <h3 style="color: #2c3e50; margin-bottom: 1rem;">{feature['icon']} {feature['title']}</h3>
                    <p style="color: #5d6d7e; line-height: 1.6;">{feature['description']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    st.divider()
    
    # Technology Stack
    st.markdown("## 🔧 Technology Stack")
    
    tech_cols = st.columns(4)
    
    technologies = [
        {"name": "IBM Watsonx", "category": "AI/ML", "icon": "🤖"},
        {"name": "Streamlit", "category": "Frontend", "icon": "🎨"},
        {"name": "FAISS", "category": "Search", "icon": "🔍"},
        {"name": "PyMuPDF", "category": "Document Processing", "icon": "📄"},
        {"name": "SentenceTransformers", "category": "NLP", "icon": "🧠"},
        {"name": "Python", "category": "Backend", "icon": "🐍"},
        {"name": "NumPy", "category": "Data Science", "icon": "📊"},
        {"name": "Pandas", "category": "Data Processing", "icon": "🐼"}
    ]
    
    for i, tech in enumerate(technologies):
        with tech_cols[i % 4]:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background-color: #ffffff; border: 2px solid #e1e8ed; border-radius: 10px; margin-bottom: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{tech['icon']}</div>
                <h4 style="margin: 0.5rem 0; color: #2c3e50;">{tech['name']}</h4>
                <p style="color: #7f8c8d; font-size: 0.9rem; margin: 0;">{tech['category']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # How it Works
    st.markdown("## ⚙️ How StudyMate Works")
    
    steps = [
        {
            "step": "1",
            "title": "Document Upload & Processing",
            "description": "Upload your PDF document, and our advanced text extraction engine processes and chunks the content for optimal AI understanding."
        },
        {
            "step": "2", 
            "title": "Semantic Indexing",
            "description": "Create searchable embeddings using state-of-the-art transformer models, enabling meaning-based search and retrieval."
        },
        {
            "step": "3",
            "title": "Intelligent Question Processing", 
            "description": "Your questions are analyzed and matched against relevant document sections using advanced semantic search algorithms."
        },
        {
            "step": "4",
            "title": "AI-Powered Answer Generation",
            "description": "IBM Watsonx AI generates contextual, accurate answers based on relevant document content and conversation history."
        }
    ]
    
    for step in steps:
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin: 1.5rem 0; padding: 1rem; background-color: #f8f9fa; border-radius: 10px;">
            <div style="background-color: #3498db; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 1rem;">
                {step['step']}
            </div>
            <div>
                <h4 style="margin: 0 0 0.5rem 0; color: #2c3e50;">{step['title']}</h4>
                <p style="margin: 0; color: #5d6d7e; line-height: 1.6;">{step['description']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("""
    <div style="background: linear-gradient(135deg, #ff9a56 0%, #ff6b6b 100%); padding: 2rem; border-radius: 15px; text-align: center; margin-top: 3rem;">
        <h3 style="color: white; margin-bottom: 1rem;">Ready to Transform Your Learning Experience?</h3>
        <p style="color: white; font-size: 1.1rem; margin-bottom: 1.5rem;">
            Join thousands of students who are already using StudyMate to enhance their academic journey.
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    about_page()
