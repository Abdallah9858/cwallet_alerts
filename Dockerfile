FROM python:3.11-slim

WORKDIR /app

# Install system build dependencies needed for PyGObject and pycairo
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    libcairo2-dev \
    libgirepository1.0-dev \
    python3-dev \
    meson \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install Cython<3.0.0 before PyYAML
RUN pip install "Cython<3.0.0"
RUN pip install --no-build-isolation PyYAML==5.4.1
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y libsystemd-dev pkg-config
RUN apt-get update && apt-get install -y python3-debian

COPY . .

CMD ["python", "firewall.py", "azurealerts.py"]
