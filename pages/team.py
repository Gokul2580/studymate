"""
Team page for StudyMate application
"""
import streamlit as st
from config.settings import TEAM_MEMBERS

def team_page():
    st.title("👥 Meet Our Team")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; margin-bottom: 2rem;">
        <h2 style="color: white; text-align: center; margin-bottom: 1rem;">🌟 The Minds Behind StudyMate</h2>
        <p style="color: white; text-align: center; font-size: 1.2rem; margin-bottom: 0;">
            A passionate team of AI researchers, developers, and designers committed to revolutionizing education.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Team stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Team Members", "3", help="Core team size")
    
    with col2:
        st.metric("Combined Experience", "19+", help="Years of combined experience")
    
    with col3:
        st.metric("AI Projects", "50+", help="AI projects completed")
    
    with col4:
        st.metric("Users Helped", "10K+", help="Students assisted")
    
    st.divider()
    
    # Team members
    st.markdown("## 👨‍💻👩‍💻 Our Core Team")
    
    for i, member in enumerate(TEAM_MEMBERS):
        # Alternate layout for visual interest
        if i % 2 == 0:
            col1, col2 = st.columns([1, 2])
        else:
            col1, col2 = st.columns([2, 1])
        
        if (i % 2 == 0):
            with col1:
                st.markdown(f"""
                <div style="text-align: center; padding: 2rem; background-color: #f8f9fa; border-radius: 15px; margin: 1rem 0;">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">{member['avatar']}</div>
                    <h3 style="color: #2c3e50; margin-bottom: 0.5rem;">{member['name']}</h3>
                    <h4 style="color: #3498db; margin-bottom: 1rem;">{member['role']}</h4>
                    <a href="{member['linkedin']}" target="_blank" style="text-decoration: none;">
                        <button style="background-color: #0077b5; color: white; padding: 0.5rem 1rem; border: none; border-radius: 5px; cursor: pointer;">
                            💼 LinkedIn
                        </button>
                    </a>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="padding: 2rem 1rem;">
                    <h3 style="color: #2c3e50; margin-bottom: 1rem;">About {member['name'].split()[1]}</h3>
                    <p style="color: #5d6d7e; line-height: 1.8; font-size: 1.1rem;">
                        {member['bio']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        else:
            with col1:
                st.markdown(f"""
                <div style="padding: 2rem 1rem;">
                    <h3 style="color: #2c3e50; margin-bottom: 1rem;">About {member['name'].split()[1]}</h3>
                    <p style="color: #5d6d7e; line-height: 1.8; font-size: 1.1rem;">
                        {member['bio']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="text-align: center; padding: 2rem; background-color: #f8f9fa; border-radius: 15px; margin: 1rem 0;">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">{member['avatar']}</div>
                    <h3 style="color: #2c3e50; margin-bottom: 0.5rem;">{member['name']}</h3>
                    <h4 style="color: #3498db; margin-bottom: 1rem;">{member['role']}</h4>
                    <a href="{member['linkedin']}" target="_blank" style="text-decoration: none;">
                        <button style="background-color: #0077b5; color: white; padding: 0.5rem 1rem; border: none; border-radius: 5px; cursor: pointer;">
                            💼 LinkedIn
                        </button>
                    </a>
                </div>
                """, unsafe_allow_html=True)
        
        if i < len(TEAM_MEMBERS) - 1:
            st.divider()
    
    # Team values
    st.markdown("## 💡 Our Values")
    
    values = [
        {
            "icon": "🎓",
            "title": "Education First",
            "description": "We believe in the transformative power of education and are committed to making learning more accessible and effective for everyone."
        },
        {
            "icon": "🤝",
            "title": "Collaboration",
            "description": "Great products come from great teamwork. We foster an environment of open communication, mutual respect, and shared goals."
        },
        {
            "icon": "🚀",
            "title": "Innovation",
            "description": "We constantly push the boundaries of what's possible with AI and educational technology to create breakthrough experiences."
        },
        {
            "icon": "🌟",
            "title": "Excellence",
            "description": "We strive for excellence in everything we do, from code quality to user experience, ensuring StudyMate exceeds expectations."
        }
    ]
    
    cols = st.columns(2)
    for i, value in enumerate(values):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="background-color: #ffffff; border: 2px solid #e1e8ed; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; height: 220px;">
                <div style="text-align: center; font-size: 3rem; margin-bottom: 1rem;">{value['icon']}</div>
                <h4 style="color: #2c3e50; text-align: center; margin-bottom: 1rem;">{value['title']}</h4>
                <p style="color: #5d6d7e; text-align: center; line-height: 1.6;">{value['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Contact section
    st.divider()
    
    st.markdown("## 📬 Get in Touch")
    
    contact_cols = st.columns(3)
    
    contact_info = [
        {"icon": "📧", "title": "Email", "info": "team@studymate.ai", "link": "mailto:team@studymate.ai"},
        {"icon": "🐦", "title": "Twitter", "info": "@StudyMateAI", "link": "https://twitter.com/StudyMateAI"},
        {"icon": "💬", "title": "Discord", "info": "StudyMate Community", "link": "https://discord.gg/studymate"}
    ]
    
    for i, contact in enumerate(contact_info):
        with contact_cols[i]:
            st.markdown(f"""
            <div style="text-align: center; padding: 2rem; background-color: #f8f9fa; border-radius: 15px;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">{contact['icon']}</div>
                <h4 style="color: #2c3e50; margin-bottom: 0.5rem;">{contact['title']}</h4>
                <a href="{contact['link']}" style="color: #3498db; text-decoration: none; font-weight: 500;">
                    {contact['info']}
                </a>
            </div>
            """, unsafe_allow_html=True)
    
    # Join us section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%); padding: 2rem; border-radius: 15px; text-align: center; margin-top: 3rem;">
        <h3 style="color: white; margin-bottom: 1rem;">🚀 Want to Join Our Mission?</h3>
        <p style="color: white; font-size: 1.1rem; margin-bottom: 1.5rem;">
            We're always looking for talented individuals who share our passion for education and AI.
        </p>
        <p style="color: white; font-size: 1rem;">
            📧 Send your resume to <strong>careers@studymate.ai</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    team_page()
