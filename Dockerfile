# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Set environment variables (loaded from .env in docker-compose)
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "app.py"]