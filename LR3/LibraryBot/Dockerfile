#Tells Docker to use the official python 3 image from dockerhub as a base image
FROM python:3

# Sets an environmental variable that ensures output from python is sent 
# straight to the terminal without buffering it first
ENV PYTHONUNBUFFERED=1

# Sets the container's working directory to /LibraryBot
WORKDIR /LibraryBot

# runs the pip install command
RUN pip install Django

# Copies all files from our local project into the container
COPY . /LibraryBot/