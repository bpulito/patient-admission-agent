# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install elasticsearch==8.15.0
RUN pip install Flask==3.1.2
RUN pip install dotenv

# Copy the current directory contents into the container at /app
COPY . /app

EXPOSE 4000

# Run main.py when the container launches
CMD ["python","-u","src/reservation-tool.py"]