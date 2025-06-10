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

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "firewall.py", "azurealerts.py"]

