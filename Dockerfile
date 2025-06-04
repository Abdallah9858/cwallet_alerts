FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install flask requests azure-identity azure-mgmt

CMD ["python","firewall.py", "azurealerts.py"]

