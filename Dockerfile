# Use a Python 3.10 slim base image for a smaller footprint
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
# This is a best practice to leverage Docker's layer caching
COPY requirements.txt .

# Install the Python dependencies
# `--no-cache-dir` reduces the image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code, including the 'data' directory
COPY . .

# Expose the port the Flask API will run on
EXPOSE 5000

# Set the default command to run the application
# This command starts the Flask API server
CMD ["python", "api.py", "--host=0.0.0.0"]
