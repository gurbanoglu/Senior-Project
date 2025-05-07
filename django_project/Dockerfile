FROM python:3.10

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    g++ \
    libboost-all-dev \
    python3-dev \
    pkg-config \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements.txt (now in the root of the repo)
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Django will run on
EXPOSE 8000

# Run the development server
CMD ["python", "django_project/manage.py", "runserver", "0.0.0.0:8000"]