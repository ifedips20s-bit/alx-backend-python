# Use official Python image
FROM python:3.10

# Set work directory in container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code into container
COPY . .

# Expose Django default port
EXPOSE 8000

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
