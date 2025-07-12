import streamlit as st
from datetime import datetime
import hashlib
from firebase_service import FirebaseService
from config import CHAT_CONFIG, WELCOME_MESSAGES, SUCCESS_MESSAGES

class ChatManager:
    def __init__(self):
        self.firebase_service = FirebaseService()
    
    def initialize_chat_sessions(self, user_name):
        """Initialize chat sessions for the user."""
        if "chat_sessions" not in st.session_state:
            # Try to load existing chat sessions for this user
            loaded_sessions, loaded_active_chat = self.firebase_service.load_chat_sessions(
                st.session_state.get('user_email')
            )
            
            if loaded_sessions:
                st.session_state.chat_sessions = loaded_sessions
                st.session_state.active_chat = loaded_active_chat
                st.success(SUCCESS_MESSAGES["chat_loaded"].format(user_name=user_name))
            else:
                # Create default chat session with welcome message
                st.session_state.chat_sessions = {
                    "default": [{"role": "ai", "content": WELCOME_MESSAGES["default"].format(user_name=user_name)}]
                }
                st.session_state.active_chat = "default"
        
        # Ensure active_chat is always set
        if "active_chat" not in st.session_state:
            st.session_state.active_chat = "default"
    
    def create_new_chat(self, chat_name, user_name):
        """Create a new chat session."""
        if chat_name and chat_name not in st.session_state.chat_sessions:
            welcome_message = WELCOME_MESSAGES["new_chat"].format(
                user_name=user_name, 
                chat_name=chat_name
            )
            st.session_state.chat_sessions[chat_name] = [{"role": "ai", "content": welcome_message}]
            st.session_state.active_chat = chat_name
            self.save_chat_sessions()
            return True
        return False
    
    def clear_current_chat(self, user_name):
        """Clear the current chat session."""
        welcome_message = WELCOME_MESSAGES["default"].format(user_name=user_name)
        st.session_state.chat_sessions[st.session_state.active_chat] = [{"role": "ai", "content": welcome_message}]
        self.save_chat_sessions()
    
    def delete_current_chat(self, user_name):
        """Delete the current chat session."""
        if len(st.session_state.chat_sessions) > 1:
            if st.session_state.active_chat in st.session_state.chat_sessions:
                # Remove the current chat session
                del st.session_state.chat_sessions[st.session_state.active_chat]
                
                # Switch to first available chat if current chat is deleted
                remaining_chats = list(st.session_state.chat_sessions.keys())
                if remaining_chats:
                    st.session_state.active_chat = remaining_chats[0]
                else:
                    # Fallback: create default chat if none exist
                    welcome_message = WELCOME_MESSAGES["default"].format(user_name=user_name)
                    st.session_state.chat_sessions["default"] = [{"role": "ai", "content": welcome_message}]
                    st.session_state.active_chat = "default"
                self.save_chat_sessions()
                return True
        return False
    
    def save_chat_sessions(self):
        """Save chat sessions to Firebase."""
        return self.firebase_service.save_chat_sessions(
            st.session_state.chat_sessions,
            st.session_state.active_chat,
            st.session_state.get('user_email'),
            st.session_state.get('user_name', 'Unknown')
        )
    
    def get_file_hash(self):
        """Get hash of the current file for auto-refresh functionality."""
        try:
            with open(__file__, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return ""
    
    def check_for_code_changes(self):
        """Check if the code has changed and preserve chat sessions."""
        current_hash = self.get_file_hash()
        
        if "file_hash" not in st.session_state:
            st.session_state.file_hash = current_hash
            st.session_state.last_refresh = datetime.now().strftime("%H:%M:%S")
            return False
        
        if st.session_state.file_hash != current_hash:
            if "chat_sessions" in st.session_state:
                preserved_sessions = st.session_state.chat_sessions.copy()
                preserved_active_chat = st.session_state.active_chat
                st.session_state.file_hash = current_hash
                st.session_state.chat_sessions = preserved_sessions
                st.session_state.active_chat = preserved_active_chat
                st.session_state.last_refresh = datetime.now().strftime("%H:%M:%S")
                st.info("🔄 Code updated! Chat sessions preserved.")
                return True
        return False 