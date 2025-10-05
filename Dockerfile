# Use lightweight Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy everything
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports for Flask (8080) and Streamlit (8501)
EXPOSE 8080 8501

# Start both Flask and Streamlit
# '&' runs Flask in background, Streamlit in foreground
CMD ["sh", "-c", "python run_backend.py & streamlit run frontend/streamlit_app.py --server.port 8501 --server.address 0.0.0.0"]
