FROM python:3.9-slim-buster

WORKDIR /app

# Install system dependencies for DeepFace (opencv, dlib sometimes needs this)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    # Add other deps if deepface/opencv-python needs them for your specific build
    # e.g., build-essential, cmake for dlib compilation
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY models/ ./models/ 
# If you pre-download models

# DeepFace's default model download location is ~/.deepface
# We can instruct it to use a specific directory if needed.
ENV DEEPFACE_HOME=/app/models/.deepface
# This tells DeepFace to download models into /app/models/.deepface if they don't exist.

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8002", "--workers", "1"]
# Use --workers 1 if DeepFace models are large or not thread-safe.
# For CPU-bound tasks, increase workers to match CPU cores. For GPU, usually 1 worker.
