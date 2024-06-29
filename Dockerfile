# Use a multi-platform base image
FROM python:3.9-slim
FROM debian

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Copy the application code
COPY . .

# Command to run the application
CMD ["python", "app.py"]