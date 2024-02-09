# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY . /app/

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir .

# Copy entrypoint scripts
COPY knockem_apply_knockout.sh /usr/local/bin/knockem_apply_knockout
COPY knockem_count_sites.sh /usr/local/bin/knockem_count_sites
COPY knockem_compete_two.sh /usr/local/bin/knockem_compete_two

# Make entrypoint scripts executable
RUN chmod +x /usr/local/bin/knockem_apply_knockout
RUN chmod +x /usr/local/bin/knockem_count_sites
RUN chmod +x /usr/local/bin/knockem_compete_two
