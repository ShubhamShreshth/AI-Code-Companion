import streamlit as st
from config import PAGE_CONFIG
from firebase_service import FirebaseService
from ollama_service import OllamaService
from auth_interface import AuthInterface
from chat_manager import ChatManager
from ui_components import UIComponents
from llm_service import LLMService

# PAGE CONFIGURATION
st.set_page_config(**PAGE_CONFIG)

# Initialize services
firebase_service = FirebaseService()
ollama_service = OllamaService()
auth_interface = AuthInterface()
chat_manager = ChatManager()
ui_components = UIComponents()
llm_service = LLMService(ollama_service)

# Render CSS
ui_components.render_css()

def main():
    # Check if user is authenticated
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        auth_interface.render()
        return
    
    # User is authenticated
    user_name = st.session_state.get('user_name', 'User')
    user_email = st.session_state.get('user_email', 'unknown@example.com')
    
    # APP HEADER
    st.title("Code Companion")
    st.caption(f"Welcome back, {user_name}")
    
    # Initialize chat sessions
    chat_manager.initialize_chat_sessions(user_name)
    
    # Check for code changes
    chat_manager.check_for_code_changes()
    
    # SIDEBAR CONFIGURATION
    with st.sidebar:
        # User info section (includes logout button)
        ui_components.render_sidebar_user_info(user_name, user_email)
        st.divider()
        
        # Model selection
        selected_model = ui_components.render_model_selection(ollama_service)
        
        # Temperature setting
        temperature = ui_components.render_temperature_slider()
        st.divider()
        
        # Model capabilities
        ui_components.render_model_capabilities()
        st.divider()
        
        # Chat session management
        ui_components.render_chat_session_management(chat_manager, user_name)
        
        # Firebase status
        ui_components.render_firebase_status(firebase_service)
        
    
    # CHAT INTERFACE
    chat_container = st.container()
    
    with chat_container:
        # Ensure active chat exists
        if st.session_state.active_chat not in st.session_state.chat_sessions:
            available_chats = list(st.session_state.chat_sessions.keys())
            if available_chats:
                st.session_state.active_chat = available_chats[0]
            else:
                st.session_state.chat_sessions["default"] = [{"role": "ai", "content": f"Hi {user_name}! I'm your personal LLM. How can I help you code today?"}]
                st.session_state.active_chat = "default"
        
        # Chat session header
        ui_components.render_chat_header(st.session_state.active_chat, user_name)
        
        # Render chat messages
        ui_components.render_chat_messages(st.session_state.chat_sessions, st.session_state.active_chat)
    
    # Chat input
    user_query = st.chat_input("Type your code/query here...")
    
    if user_query:
        # Generate AI response
        success = llm_service.generate_response(
            user_query, 
            st.session_state.chat_sessions, 
            st.session_state.active_chat, 
            selected_model, 
            temperature
        )
        
        # Save chat sessions
        if success:
            chat_manager.save_chat_sessions()
        
        st.rerun()

# Run the main application
if __name__ == "__main__":
    main() 