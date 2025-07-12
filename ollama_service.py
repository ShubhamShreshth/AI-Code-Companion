import subprocess
import streamlit as st
from langchain_ollama import ChatOllama
from config import OLLAMA_CONFIG, ERROR_MESSAGES, SUCCESS_MESSAGES, WARNING_MESSAGES

class OllamaService:
    def __init__(self):
        self.base_url = OLLAMA_CONFIG["base_url"]
        self.timeout = OLLAMA_CONFIG["timeout"]
        self.default_temperature = OLLAMA_CONFIG["default_temperature"]
    
    def get_available_models(self):
        """Get list of available Ollama models."""
        try:
            result = subprocess.run(
                ['ollama', 'list'], 
                capture_output=True, 
                text=True, 
                timeout=self.timeout
            )
            
            if result.returncode == 0 and result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                models = []
                
                for line in lines[1:]:  # Skip header line
                    if line.strip():
                        model_name = line.split()[0]
                        models.append(model_name)
                
                return models if models else None
            else:
                return None
        except Exception as e:
            st.warning(WARNING_MESSAGES["ollama_fetch_failed"].format(error=e))
            return None
    
    def is_model_available(self, model_name):
        """Check if a specific model is available."""
        available_models = self.get_available_models()
        return available_models and model_name in available_models
    
    @st.cache_resource
    def get_llm_engine(_self, model_name, temperature=None):
        """Get LLM engine for the specified model."""
        if temperature is None:
            temperature = _self.default_temperature
            
        try:
            return ChatOllama(
                model=model_name,
                base_url=_self.base_url,
                temperature=temperature
            )
        except Exception as e:
            st.error(ERROR_MESSAGES["model_connection_failed"].format(model=model_name, error=e))
            return None
    
    def get_model_status_message(self, model_name):
        """Get status message for a model."""
        if self.is_model_available(model_name):
            return SUCCESS_MESSAGES["model_available"].format(model=model_name)
        else:
            return WARNING_MESSAGES["model_unavailable"].format(model=model_name) 