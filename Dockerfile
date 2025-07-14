# Start from the official Ollama image (includes Ollama and Ubuntu)
FROM ollama/ollama:latest

# Install Python, pip, and venv
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    apt-get clean

# Set workdir
WORKDIR /app

# Copy your app code
COPY . /app

# Create and activate virtual environment, then install dependencies
RUN python3 -m venv /app/venv
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Install supervisor to run multiple processes
RUN apt-get update && apt-get install -y supervisor

# Create supervisor config
RUN echo "[supervisord]\nnodaemon=true\n" \
         "[program:ollama]\ncommand=ollama serve\n" \
         "[program:streamlit]\ncommand=/app/venv/bin/streamlit run app.py --server.port=7860 --server.address=0.0.0.0\n" \
         > /etc/supervisor/conf.d/supervisord.conf

# Expose both ports (Ollama default: 11434, Streamlit default: 7860)
EXPOSE 11434 7860

# Optionally pull your desired Ollama model(s) at build time
RUN ollama pull llama3.2:3b

# Start both services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"] 