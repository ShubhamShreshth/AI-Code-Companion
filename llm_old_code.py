import streamlit as st
import subprocess
import json
import hashlib
import os
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore, auth
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate
)

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Firebase Auth AI Code Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# FIREBASE CONFIGURATION
def initialize_firebase():
    """Initialize Firebase Admin SDK."""
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate("firebase-service-account.json")
            firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        st.error(f"Failed to initialize Firebase: {e}")
        return None

# FIREBASE AUTHENTICATION
def create_user_account(email, password, display_name):
    """Create a new user account using Firebase Auth."""
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name
        )
        
        # Create user document in Firestore
        db = initialize_firebase()
        if db:
            user_data = {
                "uid": user.uid,
                "email": email,
                "display_name": display_name,
                "created_at": firestore.SERVER_TIMESTAMP,
                "last_login": firestore.SERVER_TIMESTAMP
            }
            
            db.collection('users').document(user.uid).set(user_data)
            
            # Create default chat session
            default_chat = {
                "default": [{"role": "ai", "content": f"Hi {display_name}! I'm your personal LLM. How can I help you code today? 💻"}]
            }
            
            chat_data = {
                "chat_sessions": default_chat,
                "active_chat": "default",
                "last_saved": datetime.now().isoformat(),
                "updated_at": firestore.SERVER_TIMESTAMP,
                "user_id": user.uid,
                "user_name": display_name
            }
            
            db.collection('users').document(user.uid).collection('chats').document('history').set(chat_data)
        
        return True, f"User {display_name} created successfully!"
    except Exception as e:
        return False, f"Failed to create user: {e}"

def get_user_by_email(email):
    """Get user information from Firebase."""
    try:
        db = initialize_firebase()
        if db:
            users = db.collection('users').where('email', '==', email).limit(1).stream()
            for user in users:
                return user.to_dict()
        return None
    except Exception as e:
        st.error(f"Failed to get user: {e}")
        return None

def verify_user_credentials(email, password):
    """Verify user credentials using Firebase Auth."""
    try:
        # Check if user exists in Firebase Auth
        try:
            user = auth.get_user_by_email(email)
            # User exists in Firebase Auth
            # For now, we'll accept any password for demo purposes
            # In production, you should implement proper password verification
            return True, "Login successful"
        except auth.UserNotFoundError:
            return False, "User not found in Firebase Auth"
        except Exception as e:
            return False, f"Authentication error: {e}"
            
    except Exception as e:
        return False, f"Authentication failed: {e}"

# FIREBASE STORAGE FUNCTIONS
def save_chat_sessions():
    """Save all chat sessions to Firebase Firestore for current user."""
    try:
        user_email = st.session_state.get('user_email')
        if not user_email:
            st.error("User not authenticated.")
            return
        
        db = initialize_firebase()
        if db is None:
            st.error("Firebase not initialized. Please check your configuration.")
            return
        
        # Get user document
        user_doc = get_user_by_email(user_email)
        if not user_doc:
            st.error("User not found in database.")
            return
        
        user_id = user_doc.get('uid')
        
        chat_data = {
            "chat_sessions": st.session_state.chat_sessions,
            "active_chat": st.session_state.active_chat,
            "last_saved": datetime.now().isoformat(),
            "updated_at": firestore.SERVER_TIMESTAMP,
            "user_id": user_id,
            "user_name": st.session_state.get('user_name', 'Unknown')
        }
        
        # Save to Firestore under user's collection
        db.collection('users').document(user_id).collection('chats').document('history').set(chat_data)
        st.success("💾 Chat history saved to Firebase!")
    except Exception as e:
        st.error(f"Failed to save chat history to Firebase: {e}")

def load_chat_sessions():
    """Load chat sessions from Firebase Firestore for current user."""
    try:
        user_email = st.session_state.get('user_email')
        if not user_email:
            return {}, "default"
        
        db = initialize_firebase()
        if db is None:
            st.warning("Firebase not initialized. Starting with empty chat history.")
            return {}, "default"
        
        # Get user document
        user_doc = get_user_by_email(user_email)
        if not user_doc:
            return {}, "default"
        
        user_id = user_doc.get('uid')
        
        doc_ref = db.collection('users').document(user_id).collection('chats').document('history')
        doc = doc_ref.get()
        
        if doc.exists:
            chat_data = doc.to_dict()
            return chat_data.get("chat_sessions", {}), chat_data.get("active_chat", "default")
        else:
            st.info("No existing chat history found for this user.")
            return {}, "default"
    except Exception as e:
        st.warning(f"Could not load chat history from Firebase: {e}")
        return {}, "default"

# AUTHENTICATION INTERFACE
def auth_interface():
    """Firebase authentication interface."""
    st.markdown("## 🔐 Firebase Authentication")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.markdown("### Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            if email and password:
                success, message = verify_user_credentials(email, password)
                if success:
                    # Get user info from Firebase
                    user_doc = get_user_by_email(email)
                    if user_doc:
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.session_state.user_name = user_doc.get('display_name', 'User')
                        st.session_state.user_uid = user_doc.get('uid')
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("User not found in database.")
                else:
                    st.error(message)
            else:
                st.warning("Please enter both email and password")
    
    with tab2:
        st.markdown("### Register")
        new_email = st.text_input("Email", key="register_email")
        new_password = st.text_input("Password", type="password", key="register_password")
        display_name = st.text_input("Display Name", key="register_name")
        
        if st.button("Register"):
            if new_email and new_password and display_name:
                success, message = create_user_account(new_email, new_password, display_name)
                if success:
                    st.success(message)
                    st.info("You can now login with your new account!")
                else:
                    st.error(message)
            else:
                st.warning("Please fill all fields")

# CSS STYLING
st.markdown("""
<style>
#MainMenu, header, footer {visibility: hidden;}
.block-container {padding: 0;}

section[data-testid="stSidebar"] {
    background: #18181b !important;
    color: #e5e5e5 !important;
    border-right: 1px solid #23232a !important;
}
.st-emotion-cache-1v0mbdj {background: #18181b !important;}
.st-emotion-cache-z5fcl4 {background: #222 !important;}
.st-emotion-cache-1wrcr25 {background: #222 !important;}

.st-emotion-cache-1kyxreq {
    background: #23232a !important;
    color: #e5e5e5 !important;
    border-radius: 8px;
    margin-bottom: 12px;
    font-size: 1.1rem;
    font-weight: 400;
    padding: 10px 0 10px 0;
    text-align: center;
}

.stChatMessage {
    background: #23232a !important;
    color: #e5e5e5 !important;
    border-radius: 8px !important;
    margin: 8px 0 !important;
    padding: 12px 16px !important;
    border: 1px solid #292929 !important;
    font-size: 1rem;
}
.stChatMessage[data-testid="chatMessage"] {
    background: #23232a !important;
}

.stTextInput textarea, .stTextInput input {
    background: #23232a !important;
    color: #e5e5e5 !important;
    border: 1px solid #292929 !important;
    border-radius: 8px !important;
    font-size: 1rem !important;
    padding: 10px !important;
}
.stTextInput textarea:focus, .stTextInput input:focus {
    border-color: #3b82f6 !important;
    box-shadow: none !important;
}

.stButton > button {
    background: #23232a !important;
    color: #e5e5e5 !important;
    border: 1px solid #292929 !important;
    border-radius: 8px !important;
    font-size: 1rem !important;
    padding: 8px 16px !important;
    font-weight: 400 !important;
    transition: background 0.2s;
}
.stButton > button:hover {
    background: #2d2d2d !important;
    color: #fff !important;
    border-color: #3b82f6 !important;
}

hr {border: none !important; height: 1px !important; background: #292929 !important; margin: 18px 0 !important;}

/* Authentication styling */
.auth-container {
    background: #23232a !important;
    padding: 20px !important;
    border-radius: 12px !important;
    margin: 20px 0 !important;
}
</style>
""", unsafe_allow_html=True)

# MAIN APPLICATION
def main():
    # Check if user is authenticated
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        auth_interface()
        return
    
    # User is authenticated
    user_name = st.session_state.get('user_name', 'User')
    user_email = st.session_state.get('user_email', 'unknown@example.com')
    
    # APP HEADER
    st.title("🧠 Firebase Auth AI Code Companion")
    st.caption(f"🚀 Welcome back, {user_name}! Your AI Pair Programmer with Debugging Superpowers")
    
    # SESSION STATE INITIALIZATION
    if "chat_sessions" not in st.session_state:
        # Try to load existing chat sessions for this user
        loaded_sessions, loaded_active_chat = load_chat_sessions()
        
        if loaded_sessions:
            st.session_state.chat_sessions = loaded_sessions
            st.session_state.active_chat = loaded_active_chat
            st.success(f"📚 Chat history loaded for {user_name}!")
        else:
            # Create default chat session with welcome message
            st.session_state.chat_sessions = {
                "default": [{"role": "ai", "content": f"Hi {user_name}! I'm your personal LLM. How can I help you code today? 💻"}]
            }
            st.session_state.active_chat = "default"
    
    # Ensure active_chat is always set
    if "active_chat" not in st.session_state:
        st.session_state.active_chat = "default"
    
    # AUTO-REFRESH FUNCTIONALITY
    def get_file_hash():
        try:
            with open(__file__, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return ""
    
    def check_for_code_changes():
        current_hash = get_file_hash()
        
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
    
    code_changed = check_for_code_changes()
    
    # MODEL MANAGEMENT
    def get_available_models():
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                models = []
                
                for line in lines[1:]:
                    if line.strip():
                        model_name = line.split()[0]
                        models.append(model_name)
                
                return models if models else None
            else:
                return None
        except Exception as e:
            st.warning(f"Could not fetch models from Ollama: {e}")
            return None
    
    # SIDEBAR CONFIGURATION
    with st.sidebar:
        # User info section
        st.markdown("### 👤 User Information")
        st.info(f"**Logged in as:** {user_name}")
        st.info(f"**Email:** {user_email}")
        
        # Logout button
        if st.button("🚪 Logout", type="secondary"):
            st.session_state.authenticated = False
            st.session_state.clear()
            st.rerun()
        
        st.divider()
        
        st.header("⚙️ Configuration")
        
        # Model selection dropdown
        available_models = get_available_models()
        selected_model = st.selectbox(
            "Choose Model",
            available_models,
            index=0,
            help="Select your preferred AI model for coding assistance"
        )
        
        # Model availability status indicator
        if selected_model in available_models:
            st.success(f"✅ {selected_model} is available")
        else:
            st.warning(f"⚠️ {selected_model} may not be available")
        st.divider()
        
        # AI Model Configuration Settings
        st.markdown("### ⚙️ Settings")
        temperature = st.slider(
            "Temperature", 
            0.0, 1.0, 0.3, 0.1, 
            help="Controls randomness in responses. Lower = more focused, Higher = more creative. Optimal value for coding is 0.3"
        )
        
        st.divider()
        
        # Display model capabilities
        st.markdown("### Model Capabilities")
        st.markdown("""
        - 🐍 Python Expert
        - 🐞 Debugging Assistant
        - 📝 Code Documentation
        - 💡 Solution Design
        """)
        st.divider()
        
        # CHAT SESSION MANAGEMENT
        st.markdown("### 💬 Chat Sessions")
        
        # Create new chat session
        if "new_chat_name" not in st.session_state:
            st.session_state["new_chat_name"] = ""
        
        new_chat_name = st.text_input(
            "New Chat Name",
            value=st.session_state["new_chat_name"],
            key="new_chat_name_input"
        )
        
        if st.button("➕ New Chat", type="secondary"):
            if new_chat_name and new_chat_name not in st.session_state.chat_sessions:
                st.session_state.chat_sessions[new_chat_name] = [{"role": "ai", "content": f"Hi {user_name}! I'm your personal LLM. How can I help you with '{new_chat_name}' today? 💻"}]
                st.session_state.active_chat = new_chat_name
                save_chat_sessions()
            st.session_state["new_chat_name"] = ""
            st.rerun()
        
        # Chat selection
        chat_names = list(st.session_state.chat_sessions.keys())
        selected_chat = st.selectbox("Active Chat", chat_names, index=chat_names.index(st.session_state.active_chat))
        if selected_chat != st.session_state.active_chat:
            st.session_state.active_chat = selected_chat
            st.rerun()
        
        # Clear current chat session
        if st.button("🗑️ Clear Current Chat", type="secondary"):
            st.session_state.chat_sessions[st.session_state.active_chat] = [{"role": "ai", "content": f"Hi {user_name}! I'm your personal LLM. How can I help you code today? 💻"}]
            save_chat_sessions()
            st.rerun()
        
        # Delete current chat session (only if more than one chat exists)
        if len(st.session_state.chat_sessions) > 1:
            if st.button("🗑️ Delete Current Chat", type="secondary"):
                if st.session_state.active_chat in st.session_state.chat_sessions:
                    # Remove the current chat session
                    del st.session_state.chat_sessions[st.session_state.active_chat]
                    
                    # Switch to first available chat if current chat is deleted
                    remaining_chats = list(st.session_state.chat_sessions.keys())
                    if remaining_chats:
                        st.session_state.active_chat = remaining_chats[0]
                    else:
                        # Fallback: create default chat if none exist
                        st.session_state.chat_sessions["default"] = [{"role": "ai", "content": f"Hi {user_name}! I'm your personal LLM. How can I help you code today? 💻"}]
                        st.session_state.active_chat = "default"
                    save_chat_sessions()
                    st.rerun()
        
        st.divider()
        
        # Firebase status
        try:
            db = initialize_firebase()
            if db is not None:
                st.success("🔥 Firebase Connected")
                st.caption("💾 Chat history saved securely")
            else:
                st.error("🔥 Firebase Connection Failed")
        except Exception as e:
            st.error(f"🔥 Firebase Error: {e}")
    
    # LLM ENGINE SETUP
    @st.cache_resource
    def get_llm_engine(model_name, temp=0.3):
        try:
            return ChatOllama(
                model=model_name,
                base_url="http://localhost:11434",
                temperature=temp
            )
        except Exception as e:
            st.error(f"Failed to connect to model {model_name}: {e}")
            return None
    
    llm_engine = get_llm_engine(selected_model, temperature)
    
    # PROMPT CONFIGURATION
    system_prompt = SystemMessagePromptTemplate.from_template(
        "You are an expert AI coding assistant. Provide concise, correct solutions "
        "with strategic print statements for debugging. Always respond in English."
    )
    
    # CHAT INTERFACE
    chat_container = st.container()
    
    with chat_container:
        if st.session_state.active_chat not in st.session_state.chat_sessions:
            available_chats = list(st.session_state.chat_sessions.keys())
            if available_chats:
                st.session_state.active_chat = available_chats[0]
            else:
                st.session_state.chat_sessions["default"] = [{"role": "ai", "content": f"Hi {user_name}! I'm your personal LLM. How can I help you code today? 💻"}]
                st.session_state.active_chat = "default"
        
        # Chat session header
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 20px;
            text-align: center;
            box-shadow: 0 4px 16px rgba(99, 102, 241, 0.2);
        ">
            <h3 style="color: white; margin: 0; font-weight: 600;">💬 {st.session_state.active_chat}</h3>
            <p style="color: rgba(255,255,255,0.8); margin: 5px 0 0 0; font-size: 0.9rem;">User: {user_name}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Render chat messages
        for message in st.session_state.chat_sessions[st.session_state.active_chat]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Chat input
    user_query = st.chat_input("Type your query here...")
    
    if user_query:
        st.session_state.chat_sessions[st.session_state.active_chat].append({"role": "user", "content": user_query})
        
        if llm_engine is None:
            st.error("❌ No valid model selected. Please check your Ollama connection.")
        else:
            with st.spinner("🧠 Processing..."):
                try:
                    # Build prompt chain
                    prompt_sequence = []
                    prompt_sequence.append(system_prompt)
                    
                    for msg in st.session_state.chat_sessions[st.session_state.active_chat]:
                        if msg["role"] == "user":
                            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
                        elif msg["role"] == "ai":   
                            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))
                    
                    prompt_chain = ChatPromptTemplate.from_messages(prompt_sequence)
                    
                    # Generate AI response
                    processing_pipeline = prompt_chain | llm_engine | StrOutputParser()
                    ai_response = processing_pipeline.invoke({})
                    
                    st.session_state.chat_sessions[st.session_state.active_chat].append({"role": "ai", "content": ai_response})
                except Exception as e:
                    error_msg = f"❌ Error generating response: {str(e)}"
                    st.session_state.chat_sessions[st.session_state.active_chat].append({"role": "ai", "content": error_msg})
        
        save_chat_sessions()
        st.rerun()

# Run the main application
if __name__ == "__main__":
    main()
