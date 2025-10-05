# Use lightweight Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy backend and frontend folders
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Copy requirements from backend
COPY backend/requirements.txt ./requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports for Flask (8080) and Streamlit (8501)
EXPOSE 8080 8501

# Start both Flask and Streamlit
CMD ["sh", "-c", "python backend/run_backend.py & streamlit run frontend/streamlit_app.py --server.port 8501 --server.address 0.0.0.0"]
