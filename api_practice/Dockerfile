# Use the official Python 3.12 slim image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port
EXPOSE 8000

# Run the application with Uvicorn
CMD ["uvicorn", "api_backend:app", "--host", "0.0.0.0", "--port", "8000"]