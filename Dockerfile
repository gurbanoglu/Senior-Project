# Use official slim Python base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory to the project root
WORKDIR /app

# Install system dependencies needed for dlib and other native packages
RUN apt-get update && apt-get install -y \
    build-essential cmake libopenblas-dev liblapack-dev \
    libx11-dev libgtk-3-dev libboost-all-dev curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy entire project into container
COPY . .

# Set PYTHONPATH so Python can locate your Django apps (like 'blog')
ENV PYTHONPATH=/app/django_project

# Set environment variable for Django settings
ENV DJANGO_SETTINGS_MODULE=django_project.settings

# Expose port 8000
EXPOSE 8000

# Run the app using Gunicorn with the correct module path
CMD ["gunicorn", "django_project.wsgi:application", "--bind", "0.0.0.0:8000"]