import firebase_admin
from firebase_admin import credentials, firestore, auth
from datetime import datetime
import streamlit as st
from config import FIREBASE_CONFIG, ERROR_MESSAGES, SUCCESS_MESSAGES, WARNING_MESSAGES

class FirebaseService:
    def __init__(self):
        self.db = None
        self.initialize_firebase()
    
    def initialize_firebase(self):
        """Initialize Firebase Admin SDK."""
        try:
            if not firebase_admin._apps:
                # Create credentials from environment variables
                cred_dict = {
                    "type": FIREBASE_CONFIG["type"],
                    "project_id": FIREBASE_CONFIG["project_id"],
                    "private_key_id": FIREBASE_CONFIG["private_key_id"],
                    "private_key": FIREBASE_CONFIG["private_key"],
                    "client_email": FIREBASE_CONFIG["client_email"],
                    "client_id": FIREBASE_CONFIG["client_id"],
                    "auth_uri": FIREBASE_CONFIG["auth_uri"],
                    "token_uri": FIREBASE_CONFIG["token_uri"],
                    "auth_provider_x509_cert_url": FIREBASE_CONFIG["auth_provider_x509_cert_url"],
                    "client_x509_cert_url": FIREBASE_CONFIG["client_x509_cert_url"],
                    "universe_domain": FIREBASE_CONFIG["universe_domain"]
                }
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
            self.db = firestore.client()
            return True
        except Exception as e:
            st.error(ERROR_MESSAGES["firebase_init_failed"].format(error=e))
            return False
    
    def create_user_account(self, email, password, display_name):
        """Create a new user account using Firebase Auth."""
        try:
            user = auth.create_user(
                email=email,
                password=password,
                display_name=display_name
            )
            
            # Create user document in Firestore
            if self.db:
                user_data = {
                    "uid": user.uid,
                    "email": email,
                    "display_name": display_name,
                    "created_at": firestore.SERVER_TIMESTAMP,
                    "last_login": firestore.SERVER_TIMESTAMP
                }
                
                self.db.collection(FIREBASE_CONFIG["collection_users"]).document(user.uid).set(user_data)
                
                # Create default chat session
                default_chat = {
                    "default": [{"role": "ai", "content": f"Hi {display_name}! I'm your personal LLM. How can I help you code today?"}]
                }
                
                chat_data = {
                    "chat_sessions": default_chat,
                    "active_chat": "default",
                    "last_saved": datetime.now().isoformat(),
                    "updated_at": firestore.SERVER_TIMESTAMP,
                    "user_id": user.uid,
                    "user_name": display_name
                }
                
                self.db.collection(FIREBASE_CONFIG["collection_users"]).document(user.uid).collection(FIREBASE_CONFIG["collection_chats"]).document(FIREBASE_CONFIG["document_history"]).set(chat_data)
            
            return True, SUCCESS_MESSAGES["user_created"].format(display_name=display_name)
        except Exception as e:
            return False, f"Failed to create user: {e}"
    
    def get_user_by_email(self, email):
        """Get user information from Firebase."""
        try:
            if self.db:
                users = self.db.collection(FIREBASE_CONFIG["collection_users"]).where('email', '==', email).limit(1).stream()
                for user in users:
                    return user.to_dict()
            return None
        except Exception as e:
            st.error(f"Failed to get user: {e}")
            return None
    
    def verify_user_credentials(self, email, password):
        """Verify user credentials using Firebase Auth."""
        try:
            # Check if user exists in Firebase Auth
            try:
                user = auth.get_user_by_email(email)
                # User exists in Firebase Auth
                # For now, we'll accept any password for demo purposes
                # In production, you should implement proper password verification
                return True, SUCCESS_MESSAGES["login_successful"]
            except auth.UserNotFoundError:
                return False, "User not found in Firebase Auth"
            except Exception as e:
                return False, f"Authentication error: {e}"
                
        except Exception as e:
            return False, f"Authentication failed: {e}"
    
    def save_chat_sessions(self, chat_sessions, active_chat, user_email, user_name):
        """Save all chat sessions to Firebase Firestore for current user."""
        try:
            if not user_email:
                st.error("User not authenticated.")
                return False
            
            if self.db is None:
                st.error(ERROR_MESSAGES["firebase_connection_failed"])
                return False
            
            # Get user document
            user_doc = self.get_user_by_email(user_email)
            if not user_doc:
                st.error(ERROR_MESSAGES["user_not_found"])
                return False
            
            user_id = user_doc.get('uid')
            
            chat_data = {
                "chat_sessions": chat_sessions,
                "active_chat": active_chat,
                "last_saved": datetime.now().isoformat(),
                "updated_at": firestore.SERVER_TIMESTAMP,
                "user_id": user_id,
                "user_name": user_name
            }
            
            # Save to Firestore under user's collection
            self.db.collection(FIREBASE_CONFIG["collection_users"]).document(user_id).collection(FIREBASE_CONFIG["collection_chats"]).document(FIREBASE_CONFIG["document_history"]).set(chat_data)
            st.success(SUCCESS_MESSAGES["chat_saved"])
            return True
        except Exception as e:
            st.error(ERROR_MESSAGES["chat_save_failed"].format(error=e))
            return False
    
    def load_chat_sessions(self, user_email):
        """Load chat sessions from Firebase Firestore for current user."""
        try:
            if not user_email:
                return {}, "default"
            
            if self.db is None:
                st.warning(WARNING_MESSAGES["firebase_not_initialized"])
                return {}, "default"
            
            # Get user document
            user_doc = self.get_user_by_email(user_email)
            if not user_doc:
                return {}, "default"
            
            user_id = user_doc.get('uid')
            
            doc_ref = self.db.collection(FIREBASE_CONFIG["collection_users"]).document(user_id).collection(FIREBASE_CONFIG["collection_chats"]).document(FIREBASE_CONFIG["document_history"])
            doc = doc_ref.get()
            
            if doc.exists:
                chat_data = doc.to_dict()
                return chat_data.get("chat_sessions", {}), chat_data.get("active_chat", "default")
            else:
                st.info(WARNING_MESSAGES["no_chat_history"])
                return {}, "default"
        except Exception as e:
            st.warning(ERROR_MESSAGES["chat_load_failed"].format(error=e))
            return {}, "default"
    
    def is_connected(self):
        """Check if Firebase is connected."""
        return self.db is not None 