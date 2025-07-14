# Start from the official Ollama image (includes Ollama and Ubuntu)
FROM ollama/ollama:latest

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean

# Set workdir
WORKDIR /app

# Copy your app code
COPY . /app

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Install supervisor to run multiple processes
RUN apt-get update && apt-get install -y supervisor

# Create supervisor config
RUN echo "[supervisord]\nnodaemon=true\n" \
         "[program:ollama]\ncommand=ollama serve\n" \
         "[program:streamlit]\ncommand=streamlit run app.py --server.port=7860 --server.address=0.0.0.0\n" \
         > /etc/supervisor/conf.d/supervisord.conf

# Expose both ports (Ollama default: 11434, Streamlit default: 7860)
EXPOSE 11434 7860

RUN ollama pull llama3.2:3b

# Start both services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"] 