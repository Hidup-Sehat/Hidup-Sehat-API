FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt 

COPY . .

# Copy the generate_auth_key.py script from app/deps directory
COPY app/deps/generate_auth_key.py .

# Run the script to generate the authentication key
RUN python generate_auth_key.py

EXPOSE 8080

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

# For railway
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", $PORT]