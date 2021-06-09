#Tells Docker to use the official python 3 image from dockerhub as a base image
FROM python:3

# Sets an environmental variable that ensures output from python is sent 
# straight to the terminal without buffering it first
ENV PYTHONUNBUFFERED=1

# Sets the container's working directory to /LibraryBot
WORKDIR /LibraryBot

COPY ./requerements.txt .

RUN apt install python3-pip python3-dev unixodbc-dev
RUN pip3 install --user pyodbc

# runs the pip install command
RUN pip install -r requerements.txt

# Copies all files from our local project into the container
COPY . .

EXPOSE 8000
