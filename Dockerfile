FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt 

COPY . .

# Copy the generate_auth_key.py script from app/deps directory
# COPY app/deps/generate_auth_key.py .

# Run the script to generate the authentication key
# RUN python generate_auth_key.py

# Install NLTK and download the resources
# RUN pip install nltk
# RUN python -c "import nltk; nltk.download('stopwords')"

ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

# For railway
# COPY entrypoint.sh /app/entrypoint.sh
# RUN chmod +x /app/entrypoint.sh
# ENTRYPOINT ["/app/entrypoint.sh"]