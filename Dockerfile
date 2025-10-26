# Use official Python image
FROM python:3.10-slim


# Set working directory
WORKDIR /FastAPI-MongoDB


# Copy requirements file
COPY app/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .


# Add /app to PYTHONPATH to ensure the app module is found
ENV PYTHONPATH=/app

# Expose port for FastAPI
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

