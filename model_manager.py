#!/usr/bin/env python3
"""
Model Manager for AI Code Companion
Helps manage Ollama models for deployment
"""

import subprocess
import sys
import time
from typing import List, Optional

class ModelManager:
    def __init__(self):
        self.available_models = [
            "incept5/llama3.1-claude:latest",
            "chevalblanc/gpt-4o-mini:latest", 
            "llama3.1:8b",
            "llama3:8b",
            "llama3.2:3b"
        ]
    
    def check_ollama_installed(self) -> bool:
        """Check if Ollama is installed and running."""
        try:
            result = subprocess.run(['ollama', '--version'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def start_ollama_server(self):
        """Start Ollama server if not running."""
        try:
            # Check if server is already running
            result = subprocess.run(['ollama', 'list'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print("🔄 Starting Ollama server...")
                subprocess.Popen(['ollama', 'serve'])
                time.sleep(5)  # Wait for server to start
        except Exception as e:
            print(f"❌ Error starting Ollama server: {e}")
            return False
        return True
    
    def list_installed_models(self) -> List[str]:
        """Get list of currently installed models."""
        try:
            result = subprocess.run(['ollama', 'list'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                models = []
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        model_name = line.split()[0]
                        models.append(model_name)
                return models
            return []
        except Exception as e:
            print(f"❌ Error listing models: {e}")
            return []
    
    def download_model(self, model_name: str) -> bool:
        """Download a specific model."""
        if not self.check_ollama_installed():
            print("❌ Ollama is not installed. Please install Ollama first.")
            return False
        
        if not self.start_ollama_server():
            return False
        
        print(f"📥 Downloading model: {model_name}")
        try:
            result = subprocess.run(['ollama', 'pull', model_name], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Successfully downloaded {model_name}")
                return True
            else:
                print(f"❌ Failed to download {model_name}: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error downloading {model_name}: {e}")
            return False
    
    def download_recommended_models(self):
        """Download recommended models for the AI Code Companion."""
        recommended = ["llama3.2:3b"]
        
        print("🚀 Downloading recommended models for AI Code Companion...")
        print("This may take several minutes depending on your internet speed.")
        
        for model in recommended:
            if self.download_model(model):
                print(f"✅ {model} ready!")
            else:
                print(f"❌ Failed to download {model}")
        
        print("\n📋 Installed models:")
        installed = self.list_installed_models()
        for model in installed:
            print(f"  - {model}")
    
    def show_available_models(self):
        """Show all available models."""
        print("📋 Available models:")
        for i, model in enumerate(self.available_models, 1):
            print(f"  {i}. {model}")
    
    def interactive_download(self):
        """Interactive model download."""
        self.show_available_models()
        
        while True:
            try:
                choice = input("\nEnter model number to download (or 'q' to quit): ").strip()
                if choice.lower() == 'q':
                    break
                
                model_index = int(choice) - 1
                if 0 <= model_index < len(self.available_models):
                    model_name = self.available_models[model_index]
                    self.download_model(model_name)
                else:
                    print("❌ Invalid choice. Please try again.")
            except ValueError:
                print("❌ Please enter a valid number.")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break

def main():
    """Main function."""
    manager = ModelManager()
    
    print("🤖 AI Code Companion - Model Manager")
    print("=" * 40)
    
    if not manager.check_ollama_installed():
        print("❌ Ollama is not installed!")
        print("Please install Ollama first: https://ollama.ai")
        sys.exit(1)
    
    print("✅ Ollama is installed")
    
    # Show current models
    installed = manager.list_installed_models()
    if installed:
        print(f"📋 Currently installed models: {', '.join(installed)}")
    else:
        print("📋 No models installed yet.")
    
    print("\nOptions:")
    print("1. Download recommended models (llama2:7b, codellama:7b)")
    print("2. Interactive model download")
    print("3. List installed models")
    print("4. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                manager.download_recommended_models()
            elif choice == "2":
                manager.interactive_download()
            elif choice == "3":
                installed = manager.list_installed_models()
                if installed:
                    print("📋 Installed models:")
                    for model in installed:
                        print(f"  - {model}")
                else:
                    print("📋 No models installed.")
            elif choice == "4":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main() 