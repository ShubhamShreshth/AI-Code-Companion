import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate
)
from config import SYSTEM_PROMPT, ERROR_MESSAGES

class LLMService:
    def __init__(self, ollama_service):
        self.ollama_service = ollama_service
    
    def generate_response(self, user_query, chat_sessions, active_chat, selected_model, temperature):
        """Generate AI response for user query."""
        # Add user query to chat
        chat_sessions[active_chat].append({"role": "user", "content": user_query})
        
        # Get LLM engine
        llm_engine = self.ollama_service.get_llm_engine(selected_model, temperature)
        
        if llm_engine is None:
            st.error(ERROR_MESSAGES["no_valid_model"])
            return False
        
        with st.spinner("🧠 Processing..."):
            try:
                # Build prompt chain
                prompt_sequence = []
                prompt_sequence.append(SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT))
                
                for msg in chat_sessions[active_chat]:
                    if msg["role"] == "user":
                        prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
                    elif msg["role"] == "ai":   
                        prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))
                
                prompt_chain = ChatPromptTemplate.from_messages(prompt_sequence)
                
                # Generate AI response
                processing_pipeline = prompt_chain | llm_engine | StrOutputParser()
                ai_response = processing_pipeline.invoke({})
                
                # Add AI response to chat
                chat_sessions[active_chat].append({"role": "ai", "content": ai_response})
                return True
                
            except Exception as e:
                error_msg = ERROR_MESSAGES["response_generation_failed"].format(error=str(e))
                chat_sessions[active_chat].append({"role": "ai", "content": error_msg})
                return False 