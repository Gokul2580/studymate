"""
Main application page for PDF Q&A
"""
import streamlit as st
from utils.document_processor import DocumentProcessor
from utils.search_engine import SearchEngine
from utils.watsonx_client import WatsonxClient
from utils.tts_engine import TTSEngine
from utils.pdf_reader import PDFReader
import time
from datetime import datetime
import json
import base64

def init_session_state():
    """Initialize session state variables"""
    if 'search_engine' not in st.session_state:
        st.session_state.search_engine = SearchEngine()
    
    if 'watsonx_client' not in st.session_state:
        st.session_state.watsonx_client = WatsonxClient()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'current_document' not in st.session_state:
        st.session_state.current_document = None
    
    if 'document_stats' not in st.session_state:
        st.session_state.document_stats = {}
    
    if 'tts_engine' not in st.session_state:
        st.session_state.tts_engine = TTSEngine()
    
    if 'pdf_reader' not in st.session_state:
        st.session_state.pdf_reader = PDFReader()
    
    if 'current_audio' not in st.session_state:
        st.session_state.current_audio = None
    
    if 'reading_mode' not in st.session_state:
        st.session_state.reading_mode = False
    
    if 'current_reading_segment' not in st.session_state:
        st.session_state.current_reading_segment = 0

def display_loading_animation(text="Processing..."):
    """Display loading animation"""
    placeholder = st.empty()
    for i in range(3):
        for dots in range(4):
            placeholder.info(f"{text}{'.' * dots}")
            time.sleep(0.5)
    placeholder.empty()

def main_app():
    # Custom CSS for modern UI
    st.markdown("""
    <style>
        .main-title {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem;
            font-weight: 800;
            text-align: center;
            margin-bottom: 1rem;
        }
        
        .subtitle {
            text-align: center;
            color: #6c757d;
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }
        
        .feature-card {
            background: white;
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border: 1px solid #e1e8ed;
            margin: 1rem 0;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        }
        
        .audio-controls {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        
        .reading-highlight {
            background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid #f39c12;
            margin: 1rem 0;
        }
        
        .pdf-viewer-container {
            border: 2px solid #e1e8ed;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-title">📚 StudyMate AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your intelligent companion for academic document analysis with AI-powered features</p>', unsafe_allow_html=True)
    
    init_session_state()
    processor = DocumentProcessor()
    
    # Sidebar for document management
    with st.sidebar:
        st.header("📄 Document Management")
        
        uploaded_file = st.file_uploader(
            "Upload your PDF document",
            type=["pdf"],
            help="Upload academic papers, textbooks, or study materials"
        )
        
        if uploaded_file is not None:
            if st.session_state.current_document != uploaded_file.name:
                st.session_state.current_document = uploaded_file.name
                
                with st.spinner("🔄 Processing your document..."):
                    # Extract text
                    text = processor.extract_text_from_pdf(uploaded_file)
                    
                    # Load PDF for reader
                    uploaded_file.seek(0)  # Reset file pointer
                    st.session_state.pdf_reader.load_pdf(uploaded_file)
                    
                    if text.strip():
                        # Get document statistics
                        st.session_state.document_stats = processor.get_document_stats(text)
                        
                        # Process and index document
                        chunks = processor.chunk_text(text)
                        st.session_state.search_engine.clear_index()
                        st.session_state.search_engine.add_documents(chunks, uploaded_file.name)
                        
                        st.success("✅ Document processed successfully!")
                    else:
                        st.error("❌ Could not extract text from the PDF")
        
        # PDF Reader Controls
        if st.session_state.current_document:
            st.subheader("📖 PDF Reader Controls")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🎯 Auto Read Mode", help="Enable automatic reading with highlighting"):
                    st.session_state.reading_mode = not st.session_state.reading_mode
            
            with col2:
                reading_speed = st.slider("Reading Speed (WPM)", 100, 400, 200)
                st.session_state.pdf_reader.reading_speed = reading_speed
            
            with col3:
                if st.button("📚 Generate Audio Book"):
                    st.session_state.show_audiobook_generator = True
        
        # Document statistics
        if st.session_state.document_stats:
            st.subheader("📊 Document Statistics")
            stats = st.session_state.document_stats
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Words", f"{stats.get('total_words', 0):,}")
                st.metric("Sentences", f"{stats.get('total_sentences', 0):,}")
            
            with col2:
                st.metric("Paragraphs", f"{stats.get('total_paragraphs', 0):,}")
                st.metric("Characters", f"{stats.get('total_characters', 0):,}")
    
    # Main content area
    if st.session_state.current_document:
        st.markdown(f"""
        <div class="feature-card">
            <h4>📖 Current Document</h4>
            <p><strong>{st.session_state.current_document}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tabs for different features
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "💬 AI Q&A Chat", 
            "🔍 Advanced Search", 
            "📖 PDF Reader", 
            "🎙️ Audio Features",
            "📈 Document Insights"
        ])
        
        with tab1:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.subheader("🤖 Ask Questions About Your Document")
            
            # Question input
            question = st.text_input(
                "What would you like to know?",
                placeholder="e.g., What are the main concepts discussed in chapter 3?",
                key="question_input"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Suggested questions
            if st.session_state.chat_history:
                similar_questions = st.session_state.search_engine.get_similar_questions(
                    question if question else "", st.session_state.chat_history
                )
                
                if similar_questions:
                    st.info("💡 Similar questions you've asked before:")
                    for sq in similar_questions[:2]:
                        if st.button(f"📝 {sq}", key=f"similar_{hash(sq)}"):
                            st.session_state.question_input = sq
                            st.rerun()
            
            col1, col2 = st.columns([1, 4])
            
            with col1:
                ask_button = st.button("🚀 Ask", type="primary", use_container_width=True)
            
            with col2:
                if st.button("🗑️ Clear Chat History", use_container_width=True):
                    st.session_state.chat_history = []
                    st.success("Chat history cleared!")
            
            # TTS Controls for Q&A
            if question:
                st.markdown('<div class="audio-controls">', unsafe_allow_html=True)
                st.subheader("🎙️ Text-to-Speech Controls")
                
                tts_col1, tts_col2, tts_col3 = st.columns(3)
                
                with tts_col1:
                    tts_language = st.selectbox(
                        "Language",
                        options=list(st.session_state.tts_engine.supported_languages.keys()),
                        format_func=lambda x: st.session_state.tts_engine.supported_languages[x],
                        key="tts_language"
                    )
                
                with tts_col2:
                    tts_speed = st.checkbox("Slow Speech", help="Enable slower speech for better comprehension")
                
                with tts_col3:
                    if st.button("🔊 Read Question Aloud"):
                        audio_bytes = st.session_state.tts_engine.text_to_speech(question, tts_language, tts_speed)
                        if audio_bytes:
                            audio_html = st.session_state.tts_engine.get_audio_player_html(audio_bytes, autoplay=True)
                            st.markdown(audio_html, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            if ask_button and question:
                # Search for relevant context
                with st.spinner("🔍 Searching for relevant information..."):
                    search_results = st.session_state.search_engine.search(question, top_k=3)
                
                if search_results:
                    context = "\n\n".join([result[0] for result in search_results])
                    
                    # Generate chat history context
                    chat_context = ""
                    if st.session_state.chat_history:
                        recent_chat = st.session_state.chat_history[-3:]  # Last 3 interactions
                        chat_context = "\n".join([
                            f"Q: {item['question']}\nA: {item['answer']}\n"
                            for item in recent_chat
                        ])
                    
                    # Generate answer
                    with st.spinner("🤖 Generating answer..."):
                        answer = st.session_state.watsonx_client.generate_answer(
                            question, context, chat_context
                        )
                    
                    # Display answer with enhanced formatting
                    st.markdown("### 💬 Answer")
                    st.markdown(f'<div class="feature-card"><p>{answer}</p></div>', unsafe_allow_html=True)
                    
                    # TTS for Answer
                    st.markdown('<div class="audio-controls">', unsafe_allow_html=True)
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("🔊 Read Answer Aloud", key="read_answer"):
                            audio_bytes = st.session_state.tts_engine.text_to_speech(answer, tts_language, tts_speed)
                            if audio_bytes:
                                audio_html = st.session_state.tts_engine.get_audio_player_html(audio_bytes, autoplay=True)
                                st.markdown(audio_html, unsafe_allow_html=True)
                    
                    with col2:
                        if st.button("📥 Download Answer Audio", key="download_answer"):
                            audio_bytes = st.session_state.tts_engine.text_to_speech(answer, tts_language, tts_speed)
                            if audio_bytes:
                                download_link = st.session_state.tts_engine.create_download_link(
                                    audio_bytes, f"answer_{int(time.time())}.mp3"
                                )
                                st.markdown(download_link, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Show sources
                    with st.expander("📚 Source Context"):
                        for i, (text, score, metadata) in enumerate(search_results):
                            st.markdown(f"**Source {i+1}** (Relevance: {1-score:.2f})")
                            st.text_area(
                                f"Context {i+1}",
                                text[:300] + "..." if len(text) > 300 else text,
                                height=100,
                                key=f"context_{i}"
                            )
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "question": question,
                        "answer": answer,
                        "sources": len(search_results)
                    })
                    
                else:
                    st.warning("⚠️ No relevant context found for your question. Try rephrasing it.")
            
            # Display chat history
            if st.session_state.chat_history:
                st.markdown("### 📜 Chat History")
                
                for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):  # Show last 5
                    with st.expander(f"💭 {chat['question'][:60]}... ({chat['timestamp']})"):
                        st.markdown(f"**Q:** {chat['question']}")
                        st.markdown(f"**A:** {chat['answer']}")
                        st.caption(f"Sources used: {chat['sources']}")
        
        with tab2:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.subheader("🔍 Advanced Semantic Search")
            
            search_query = st.text_input(
                "Search through document content",
                placeholder="Enter keywords or phrases to search for..."
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            with col1:
                num_results = st.slider("Number of results", 1, 10, 5)
            
            with col2:
                search_type = st.selectbox("Search mode", ["Semantic", "Keyword"])
            
            if st.button("🔍 Search", type="primary") and search_query:
                with st.spinner("Searching..."):
                    results = st.session_state.search_engine.search(search_query, top_k=num_results)
                
                if results:
                    st.success(f"Found {len(results)} relevant results")
                    
                    for i, (text, score, metadata) in enumerate(results):
                        with st.container():
                            st.markdown(f"### 📄 Result {i+1}")
                            st.markdown(f"**Relevance Score:** {1-score:.3f}")
                            
                            # Highlight search terms (basic implementation)
                            highlighted_text = text
                            for term in search_query.split():
                                highlighted_text = highlighted_text.replace(
                                    term, f"**{term}**"
                                )
                            
                            st.markdown(highlighted_text)
                            st.divider()
                else:
                    st.info("No results found for your search query.")
        
        with tab3:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.subheader("📖 Interactive PDF Reader")
            
            if st.session_state.pdf_reader.current_pdf:
                # PDF Navigation
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("⬅️ Previous Page") and st.session_state.pdf_reader.current_page > 0:
                        st.session_state.pdf_reader.current_page -= 1
                
                with col2:
                    page_num = st.number_input(
                        "Page", 
                        min_value=1, 
                        max_value=st.session_state.pdf_reader.total_pages,
                        value=st.session_state.pdf_reader.current_page + 1
                    ) - 1
                    st.session_state.pdf_reader.current_page = page_num
                
                with col3:
                    if st.button("➡️ Next Page") and st.session_state.pdf_reader.current_page < st.session_state.pdf_reader.total_pages - 1:
                        st.session_state.pdf_reader.current_page += 1
                
                with col4:
                    st.metric("Total Pages", st.session_state.pdf_reader.total_pages)
                
                # Text highlighting
                highlight_text = st.text_input("🎯 Highlight text in PDF", placeholder="Enter text to highlight...")
                
                # Display current page
                current_page = st.session_state.pdf_reader.current_page
                
                if highlight_text:
                    img_data = st.session_state.pdf_reader.highlight_text_in_page(current_page, highlight_text)
                else:
                    img_data = st.session_state.pdf_reader.get_page_image(current_page)
                
                if img_data:
                    st.markdown('<div class="pdf-viewer-container">', unsafe_allow_html=True)
                    st.image(img_data, use_column_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Page text and reading features
                page_text = st.session_state.pdf_reader.get_page_text(current_page)
                
                if page_text:
                    with st.expander("📄 Page Text Content"):
                        st.text_area("Page Content", page_text, height=200)
                    
                    # Reading automation
                    if st.session_state.reading_mode:
                        st.markdown('<div class="reading-highlight">', unsafe_allow_html=True)
                        st.subheader("🎯 Auto Reading Mode Active")
                        
                        segments = st.session_state.pdf_reader.get_reading_segments(page_text)
                        
                        if segments:
                            current_segment = st.session_state.current_reading_segment
                            if current_segment < len(segments):
                                st.markdown(f"**Reading Segment {current_segment + 1}/{len(segments)}:**")
                                st.markdown(f'<div style="background: #fff3cd; padding: 1rem; border-radius: 8px; font-size: 1.1rem;">{segments[curren
