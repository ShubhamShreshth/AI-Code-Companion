import streamlit as st
from firebase_service import FirebaseService
from config import SUCCESS_MESSAGES

class AuthInterface:
    def __init__(self):
        self.firebase_service = FirebaseService()
    
    def render(self):
        """Render the authentication interface."""
        st.markdown("## 🔐 Authentication")
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            self._render_login_tab()
        
        with tab2:
            self._render_register_tab()
    
    def _render_login_tab(self):
        """Render the login tab."""
        st.markdown("### Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            if email and password:
                success, message = self.firebase_service.verify_user_credentials(email, password)
                if success:
                    # Get user info from Firebase
                    user_doc = self.firebase_service.get_user_by_email(email)
                    if user_doc:
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.session_state.user_name = user_doc.get('display_name', 'User')
                        st.session_state.user_uid = user_doc.get('uid')
                        st.success(SUCCESS_MESSAGES["login_successful"])
                        st.rerun()
                    else:
                        st.error("User not found in database.")
                else:
                    st.error(message)
            else:
                st.warning("Please enter both email and password")
    
    def _render_register_tab(self):
        """Render the register tab."""
        st.markdown("### Register")
        new_email = st.text_input("Email", key="register_email")
        new_password = st.text_input("Password", type="password", key="register_password")
        display_name = st.text_input("Display Name", key="register_name")
        
        if st.button("Register"):
            if new_email and new_password and display_name:
                success, message = self.firebase_service.create_user_account(new_email, new_password, display_name)
                if success:
                    st.success(message)
                    st.info("You can now login with your new account!")
                else:
                    st.error(message)
            else:
                st.warning("Please fill all fields") 