#!/bin/bash

# Load environment variables from .env file
source .env

# Start your application
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
