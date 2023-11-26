# Use an official Python runtime as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy all files from the current directory to the container
COPY . .

# Expose the port your Django app is running on (change this if necessary)
EXPOSE 8001

# Start your Django app
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
CMD ["gunicorn", "--bind", "0.0.0.0:8001", "app.wsgi:application"]
