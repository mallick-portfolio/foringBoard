# Use Python 3.11 as base image
FROM python:3.11


# Set work directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

# Install dependencies
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Run development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]