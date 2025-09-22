FROM python:3.12.3-slim

# Install system dependencies
RUN apt-get update -qq \
    && apt-get install -y build-essential libcairo2 libpango-1.0-0 libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 libffi-dev shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Install Python dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

# Copy project files
COPY . .

# Optional: run Django migrations automatically (if desired)
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
