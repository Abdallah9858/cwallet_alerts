# Use a base Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install the necessary dependencies directly
RUN pip install --no-cache-dir \
    acme==2.9.0 \
    appdirs==1.4.4 \
    argcomplete==3.1.4 \
    argon2-cffi==21.1.0 \
    asgiref==3.7.2 \
    asn1crypto==1.5.1 \
    asttokens==2.4.1 \
    async-timeout==4.0.3 \
    attrs==23.2.0 \
    Babel==2.10.3 \
    bleach==6.1.0 \
    blinker==1.7.0\
    Brlapi==0.8.5

# Copy the entire project into the container
COPY . .

# Install any additional system dependencies you may need
RUN apt-get update && apt-get install -y \
    some-system-package

# Set environment variables, if necessary
ENV SOME_ENV_VAR=some_value

# Run the app when the container starts
CMD ["python", "app.py"]
