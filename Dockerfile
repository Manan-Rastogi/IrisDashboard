# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set environment variables for Python and Flask
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create a virtual environment and activate it
RUN python3 -m venv venv
RUN . venv/bin/activate

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
