import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PAGE CONFIGURATION
PAGE_CONFIG = {
    "page_title": "AI Code Companion",
    "page_icon": "🧠",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# FIREBASE CONFIGURATION
FIREBASE_CONFIG = {
    "type": os.getenv("FIREBASE_TYPE", "service_account"),
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n"),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": os.getenv("FIREBASE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL", "https://www.googleapis.com/oauth2/v1/certs"),
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("FIREBASE_UNIVERSE_DOMAIN", "googleapis.com"),
    "collection_users": "users",
    "collection_chats": "chats",
    "document_history": "history"
}

# OLLAMA CONFIGURATION
OLLAMA_CONFIG = {
    "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    "timeout": int(os.getenv("OLLAMA_TIMEOUT", "10")),
    "default_temperature": float(os.getenv("OLLAMA_DEFAULT_TEMPERATURE", "0.3"))
}

# CHAT CONFIGURATION
CHAT_CONFIG = {
    "default_chat_name": "default",
    "max_chat_history": 100,
    "auto_save_interval": 30  # seconds
}

# UI CONFIGURATION
UI_CONFIG = {
    "theme": "dark",
    "primary_color": "#6366f1",
    "secondary_color": "#8b5cf6",
    "background_color": "#18181b",
    "text_color": "#e5e5e5"
}

# SYSTEM PROMPT
SYSTEM_PROMPT = """You are an expert AI coding assistant. Provide concise, correct solutions 
with strategic print statements for debugging. Always respond in English."""

# WELCOME MESSAGES
WELCOME_MESSAGES = {
    "default": "Hi {user_name}! I'm your personal LLM. How can I help you code today?",
    "new_chat": "Hi {user_name}! I'm your personal LLM. How can I help you with '{chat_name}' today?"
}

# ERROR MESSAGES
ERROR_MESSAGES = {
    "firebase_init_failed": "Failed to initialize Firebase: {error}",
    "firebase_connection_failed": "Firebase not initialized. Please check your configuration.",
    "user_not_found": "User not found in database.",
    "model_connection_failed": "Failed to connect to model {model}: {error}",
    "no_valid_model": "No valid model selected. Please check your Ollama connection.",
    "response_generation_failed": "Error generating response: {error}",
    "chat_save_failed": "Failed to save chat history to Firebase: {error}",
    "chat_load_failed": "Could not load chat history from Firebase: {error}"
}

# SUCCESS MESSAGES
SUCCESS_MESSAGES = {
    "chat_saved": "💾 Chat history saved to Firebase!",
    "chat_loaded": "📚 Chat history loaded for {user_name}!",
    "user_created": "User {display_name} created successfully!",
    "login_successful": "Login successful!",
    "firebase_connected": "🔥 Firebase Connected",
    "model_available": "✅ {model} is available"
}

# WARNING MESSAGES
WARNING_MESSAGES = {
    "firebase_not_initialized": "Firebase not initialized. Starting with empty chat history.",
    "no_chat_history": "No existing chat history found for this user.",
    "model_unavailable": "⚠️ {model} may not be available",
    "ollama_fetch_failed": "Could not fetch models from Ollama: {error}"
} 