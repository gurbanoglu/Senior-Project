# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app/django_project

# Install OS-level dependencies needed for dlib
RUN apt-get update && apt-get install -y \
    build-essential cmake libopenblas-dev liblapack-dev \
    libx11-dev libgtk-3-dev libboost-all-dev curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy Django project files (everything from root into /app)
COPY . .

# Set environment variable if needed
ENV DJANGO_SETTINGS_MODULE=django_project.django_project.settings

# Expose the port
EXPOSE 8000

# Run the app using gunicorn
CMD ["gunicorn", "django_project.wsgi:application", "--bind", "0.0.0.0:8000"]