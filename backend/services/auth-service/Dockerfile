FROM python:3.9-slim-buster 
#use python 3.9 because its smaller ans more stable than eany other python version
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY .env ./.env

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001"]
