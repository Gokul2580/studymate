"""
Main StudyMate application with multi-page navigation
"""
import streamlit as st
from streamlit_option_menu import option_menu
from pages.main_app import main_app
from pages.about import about_page
from pages.team import team_page
from config.settings import UI_CONFIG

# Page configuration
st.set_page_config(
    page_title=UI_CONFIG["page_title"],
    page_icon=UI_CONFIG["page_icon"],
    layout=UI_CONFIG["layout"],
    initial_sidebar_state=UI_CONFIG["initial_sidebar_state"]
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    /* Hide Streamlit style */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
    }
    
    /* Enhanced buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        background: linear-gradient(135deg, #2980b9 0%, #3498db 100%);
    }
    
    /* Enhanced metrics */
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem 0;
    }
    
    /* Enhanced text areas and inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid #e1e8ed;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #3498db;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
    }
    
    /* Loading animations */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .loading {
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    /* Enhanced navigation */
    .nav-menu {
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        padding: 0.5rem;
        margin-bottom: 2rem;
    }
    
    /* Success/error messages */
    .stAlert {
        border-radius: 10px;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        background: #f8f9fa;
        border-radius: 10px;
        margin-top: 3rem;
        color: #6c757d;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📚 StudyMate</h1>
        <p>Your AI-Powered Academic Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation menu
    with st.container():
        selected = option_menu(
            menu_title=None,
            options=["🏠 Home", "📖 About", "👥 Team"],
            icons=["house", "info-circle", "people"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "white",
                    "border-radius": "15px",
                    "box-shadow": "0 4px 8px rgba(0,0,0,0.1)",
                    "margin-bottom": "2rem"
                },
                "icon": {"color": "#3498db", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "center",
                    "margin": "0px",
                    "padding": "12px 16px",
                    "border-radius": "10px",
                    "color": "#2c3e50",
                    "font-weight": "500"
                },
                "nav-link-selected": {
                    "background": "linear-gradient(135deg, #3498db 0%, #2980b9 100%)",
                    "color": "white",
                    "font-weight": "600"
                },
            }
        )
    
    # Page routing
    if selected == "🏠 Home":
        main_app()
    elif selected == "📖 About":
        about_page()
    elif selected == "👥 Team":
        team_page()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p><strong>StudyMate</strong> © 2024 | Built with ❤️ using Streamlit and IBM Watsonx AI</p>
        <p>Empowering students worldwide with intelligent document analysis</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()