# Use a lightweight and fast official Python image
FROM python:3.11-slim

# Prevent Python from creating .pyc files and force real-time log output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the dependencies file first to take advantage of Docker's cache
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application code into the container
COPY . .

# Expose the port on which FastAPI will run
EXPOSE 8000

# Command to start the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]