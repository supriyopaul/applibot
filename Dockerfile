FROM python:3.9-slim

# Set environment variables
# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

# Set the working directory in the docker container
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt ./

# Install the application dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Declare the directory as a mountable volume
VOLUME /usr/src/app/my-data/

# Specify the command to run on container start
CMD ["python", "-m", "applibot.server", "--config", "/usr/src/app/my-config-file.yaml"]
