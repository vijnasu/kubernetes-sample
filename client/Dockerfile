# Use an official Python runtime as a parent image
FROM python:3.7-slim

ENV http_proxy=http://proxy-iind.intel.com:911
ENV https_proxy=http://proxy-iind.intel.com:911

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org grpcio-tools

ENV http_proxy=''
ENV https_proxy=''

# Run client.py when the container launches
CMD ["python", "client.py"]

