FROM python:3.9-slim

WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy rest of the application
COPY . .

# Create data directory for SQLite
RUN mkdir -p /app/data

# Expose port 5000
EXPOSE 5000

# Start the application
CMD ["python", "server.py"]
