# Use the official Python 3.11 image from Docker Hub
FROM python:3.11

# Set the working directory in the Docker container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt ./

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Command to run the application
CMD ["python3", "main.py"]