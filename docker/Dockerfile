# syntax=docker/dockerfile:1
# FROM python:3.11-slim

# # Set working directory
# WORKDIR /app

# # Copy project
# COPY . .

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Default command (can be overridden)
# CMD ["python", "media_review.py", "--help"]

# Use lightweight Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

ENV PYTHONPATH=/app

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies (no cache to reduce image size)
RUN pip install --no-cache-dir -r requirements.txt


# Install bash (since python:3.11-slim doesn’t include it)
RUN apt-get update && apt-get install -y bash

# Copy the rest of your project
COPY . .

# Set environment variables (adjust as needed) - All print() and logging output shows immediately in the container logs, 
# since by default, Python buffers its output — meaning logs or print() statements might not appear instantly.
# In a Docker container, that can make logs appear late or even out of order in real time.
ENV PYTHONUNBUFFERED=1

# Default to a bash shell (so docker-compose command can override it easily)
# Because now we want to run multiple Python scripts as commands in docker-compose, 
# not lock ourselves to one entrypoint like media_review.py.
# ENTRYPOINT ["/bin/bash"]

#later use python media_review --help for the commands

