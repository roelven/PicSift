# Use an official Python runtime based on Debian 10 ("buster") as a parent image.
# This image includes Python 3.8, which is suitable for most applications.
FROM python:3.8-slim-buster

# Define the working directory in the container. This is the directory in which
# the commands will run unless full path to executable is specified.
WORKDIR /app

# Copy your project's requirement.txt file into the container and install the
# Python dependencies. The `--no-cache-dir` option ensures the Docker image is
# as small as possible, while the `-r requirements.txt` option installs the 
# required packages as specified in the requirements.txt file.
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Tesseract
RUN apt-get update \
    && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-deu \
    tesseract-ocr-nld \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of the code into the Docker container. Note that this happens
# after the installation of dependencies, which means Docker can use its cache
# during the building process if the dependencies haven't changed.
COPY . /app

# Expose port 5000 in the Docker container. This is the default port on which
# Flask applications run.
EXPOSE 5000

# Set environment variables for Flask
# If you are deploying in a production environment, set FLASK_ENV to "production"
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# Run the application. If you have an entry point defined in your setup.py file,
# Docker will run this by default. Otherwise, it will look for the `app.py` file.
CMD ["flask", "run"]
