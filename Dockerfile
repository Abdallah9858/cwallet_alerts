# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy only requirements.txt first (to leverage Docker layer caching)
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application files
COPY . .

# Default command to run your scripts
CMD ["python", "firewall.py", "azurealerts.py"]

