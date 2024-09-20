# Use the official Python base image
FROM python:3.11

# Set the working directory in the Docker image
WORKDIR /app

# Copy requirements.txt and install the Python dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the application code to the Docker image
COPY . .

CMD ["uvicorn", "app.main:api", "--host", "0.0.0.0", "--port", "8000"]