import streamlit as st
from config import UI_CONFIG, SUCCESS_MESSAGES, ERROR_MESSAGES

class UIComponents:
    @staticmethod
    def render_css():
        """Render the minimal CSS styling."""
        st.markdown("""
        <style>
        /* Hide default elements */
        #MainMenu, header, footer {visibility: hidden;}
        .block-container {padding: 1rem 2rem;}
        
        /* Global styles */
        .stApp {
            background: #000000 !important;
        }
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background: #111111 !important;
            border-right: 1px solid #222222 !important;
        }
        
        /* Main content area */
        .main .block-container {
            background: #000000 !important;
            padding: 2rem !important;
        }
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            font-weight: 600 !important;
            color: #ffffff !important;
        }
        
        /* Chat messages */
        .stChatMessage {
            background: #111111 !important;
            color: #ffffff !important;
            border-radius: 12px !important;
            margin: 8px 0 !important;
            padding: 16px 20px !important;
            border: none !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.3) !important;
            font-size: 0.95rem !important;
            line-height: 1.5 !important;
        }
        
        .stChatMessage[data-testid="chatMessage"] {
            background: #111111 !important;
        }
        
        /* User messages */
        .stChatMessage.user {
            background: #007bff !important;
            color: #ffffff !important;
            margin-left: auto !important;
            max-width: 80% !important;
        }
        
        /* AI messages */
        .stChatMessage.assistant {
            background: #111111 !important;
            color: #ffffff !important;
            max-width: 80% !important;
        }
        
        /* Input styling */
        .stTextInput textarea, .stTextInput input {
            background: #111111 !important;
            color: #ffffff !important;
            border: 1px solid #222222 !important;
            border-radius: 8px !important;
            font-size: 0.95rem !important;
            padding: 12px 16px !important;
            transition: border-color 0.2s ease;
        }
        
        .stTextInput textarea:focus, .stTextInput input:focus {
            border-color: #007bff !important;
            box-shadow: 0 0 0 0.2rem rgba(0,123,255,0.25) !important;
        }
        
        /* Button styling */
        .stButton > button[kind="primary"] {
            background: #007bff !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 8px !important;
            font-size: 0.9rem !important;
            padding: 8px 16px !important;
            font-weight: 500 !important;
            transition: all 0.2s ease;
        }
        
        .stButton > button[kind="primary"]:hover {
            background: #0056b3 !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
        }
        
        /* Logout button styling */
        .stButton > button[kind="secondary"] {
            background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 12px 16px !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            box-shadow: 0 2px 8px rgba(255,68,68,0.3) !important;
            transition: all 0.3s ease !important;
            margin-top: 10px !important;
        }
        
        .stButton > button[kind="secondary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(255,68,68,0.4) !important;
        }
        
        /* Secondary buttons */
        .stButton > button[data-baseweb="button"] {
            background: #6c757d !important;
        }
        
        .stButton > button[data-baseweb="button"]:hover {
            background: #545b62 !important;
        }
        
        /* Selectbox styling */
        .stSelectbox > div > div {
            background: #111111 !important;
            border: 1px solid #222222 !important;
            border-radius: 8px !important;
            color: #ffffff !important;
        }
        
        .stSelectbox > div > div > div {
            background: #111111 !important;
            color: #ffffff !important;
        }
        
        .stSelectbox > div > div > div > div {
            background: #111111 !important;
            color: #ffffff !important;
        }
        
        /* Dropdown options */
        .stSelectbox > div > div > div > div > div {
            background: #111111 !important;
            color: #ffffff !important;
        }
        
        .stSelectbox > div > div > div > div > div:hover {
            background: #222222 !important;
            color: #ffffff !important;
        }
        
        /* Slider styling */
        .stSlider > div > div > div > div {
            background: #007bff !important;
        }
        
        /* Divider styling */
        hr {
            border: none !important;
            height: 1px !important;
            background: #222222 !important;
            margin: 24px 0 !important;
        }
        
        /* Info boxes */
        .stAlert {
            border-radius: 8px !important;
            border: none !important;
            padding: 12px 16px !important;
        }
        
        /* Success styling */
        .stAlert[data-baseweb="notification"] {
            background: #1a2e1a !important;
            color: #4ade80 !important;
            border: 1px solid #22c55e !important;
        }
        
        /* Warning styling */
        .stAlert[data-baseweb="notification"].warning {
            background: #2e2a1a !important;
            color: #fbbf24 !important;
            border: 1px solid #f59e0b !important;
        }
        
        /* Error styling */
        .stAlert[data-baseweb="notification"].error {
            background: #2e1a1a !important;
            color: #f87171 !important;
            border: 1px solid #ef4444 !important;
        }
        
        /* Chat container */
        .chat-container {
            background: #111111 !important;
            border-radius: 12px !important;
            padding: 20px !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3) !important;
        }
        
        /* Minimal spacing */
        .element-container {
            margin-bottom: 16px !important;
        }
        
        /* Code blocks in messages */
        .stChatMessage pre {
            background: #000000 !important;
            border: 1px solid #222222 !important;
            border-radius: 6px !important;
            padding: 12px !important;
            margin: 8px 0 !important;
            overflow-x: auto !important;
        }
        
        
        .stChatMessage code {
            background: #111111 !important;
            padding: 2px 6px !important;
            border-radius: 4px !important;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace !important;
            font-size: 0.9rem !important;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .block-container {padding: 1rem !important;}
            .stChatMessage {max-width: 95% !important;}
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_sidebar_user_info(user_name, user_email):
        """Render user information in sidebar."""
        # Creative user profile card
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
            color: white;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        ">
            <div style="
                width: 60px;
                height: 60px;
                background: rgba(255,255,255,0.2);
                border-radius: 50%;
                margin: 0 auto 15px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
            ">
                👤
            </div>
            <h3 style="margin: 0; font-size: 18px; font-weight: 600;">{}</h3>
            <p style="margin: 5px 0 0; opacity: 0.9; font-size: 14px;">{}</p>
            <div style="
                margin-top: 15px;
                padding: 8px 16px;
                background: rgba(255,255,255,0.1);
                border-radius: 20px;
                font-size: 12px;
                font-weight: 500;
            ">
                🟢 Online
            </div>
        </div>
        """.format(user_name, user_email), unsafe_allow_html=True)
        
        # Logout button positioned right below the online status
        if st.button("🚪 Sign Out", key="logout_btn", type="secondary", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.clear()
            st.rerun()
    

    
    @staticmethod
    def render_model_selection(ollama_service):
        """Render model selection in sidebar."""
        st.markdown("### 🤖 Model")
        
        available_models = ollama_service.get_available_models()
        selected_model = st.selectbox(
            "Select Model",
            available_models,
            index=0,
            help="Choose your AI model"
        )
        
        # Model availability status indicator with better styling
        status_message = ollama_service.get_model_status_message(selected_model)
        if "✅" in status_message:
            st.success(f"✅ {selected_model} is ready to use")
        else:
            st.warning(f"⚠️ {selected_model} is not available")
        
        # Add model info
        # st.caption(f"Model: **{selected_model}**")
        
        return selected_model
    
    @staticmethod
    def render_temperature_slider():
        """Render temperature slider."""
        st.markdown("### ⚙️ Settings")
        
        # Temperature slider with better styling
        temperature = st.slider(
            "Temperature", 
            0.0, 1.0, 0.3, 0.1, 
            help="Response creativity (0.3 recommended for coding)"
        )
        
        # Show temperature value with context
        col1, col2 = st.columns([1, 1])
        with col1:
            st.caption(f"Value: **{temperature}**")
        with col2:
            if temperature <= 0.3:
                st.caption("🎯 Focused")
            elif temperature <= 0.7:
                st.caption("⚖️ Balanced")
            else:
                st.caption("🎨 Creative")
        
        return temperature
    
    @staticmethod
    def render_model_capabilities():
        """Render model capabilities section."""
        st.markdown("### 💡 Capabilities")
        
        # Create a nice capabilities grid
        capabilities = [
            ("🐍", "Python Expert"),
            ("🐞", "Debugging Assistant"),
            ("📝", "Code Documentation"),
            ("💡", "Solution Design"),
            ("🔍", "Code Analysis"),
            ("⚡", "Performance Optimization")
        ]
        
        # Display capabilities in a grid layout
        cols = st.columns(2)
        for i, (icon, capability) in enumerate(capabilities):
            with cols[i % 2]:
                st.markdown(f"{icon} **{capability}**")
    
    @staticmethod
    def render_chat_session_management(chat_manager, user_name):
        """Render chat session management in sidebar."""
        st.markdown("### 💬 Chats")
        
        # Manual refresh button
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh", type="primary", help="Refresh app", use_container_width=True):
                st.rerun()
        with col2:
            if st.button("📊 Status", type="primary", help="Check status", use_container_width=True):
                st.info("✅ Running")
        
        # Create new chat session
        if "new_chat_name" not in st.session_state:
            st.session_state["new_chat_name"] = ""
        
        new_chat_name = st.text_input(
            "New Chat",
            value=st.session_state["new_chat_name"],
            key="new_chat_name_input",
            placeholder="New Chat name..."
        )
        
        if st.button("New Chat", type="primary", use_container_width=True):
            if chat_manager.create_new_chat(new_chat_name, user_name):
                st.session_state["new_chat_name"] = ""
                st.rerun()
        
        # Chat selection
        chat_names = list(st.session_state.chat_sessions.keys())
        selected_chat = st.selectbox("Active Chats", chat_names, index=chat_names.index(st.session_state.active_chat))
        if selected_chat != st.session_state.active_chat:
            st.session_state.active_chat = selected_chat
            st.rerun()
        
        # Clear current chat session
        if st.button("Clear Chat", type="primary", use_container_width=True):
            chat_manager.clear_current_chat(user_name)
            st.rerun()
        
        # Delete current chat session (only if more than one chat exists)
        if len(st.session_state.chat_sessions) > 1:
            if st.button("Delete Chat", type="primary", use_container_width=True):
                if chat_manager.delete_current_chat(user_name):
                    st.rerun()
    
    @staticmethod
    def render_firebase_status(firebase_service):
        """Render Firebase connection status."""
        try:
            if firebase_service.is_connected():
                st.success("✅ Database Connected")
                st.caption("Chat history saved")
            else:
                st.error("❌ Database Connection Failed")
        except Exception as e:
            st.error(f"Error: {e}")
    
    @staticmethod
    def render_chat_header(active_chat, user_name):
        """Render chat session header."""
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 20px;
            text-align: center;
            box-shadow: 0 4px 16px rgba(99, 102, 241, 0.2);
        ">
            <h3 style="color: white; margin: 0; font-weight: 600;">💬 {active_chat}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_chat_messages(chat_sessions, active_chat):
        """Render chat messages."""
        for message in chat_sessions[active_chat]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"]) 