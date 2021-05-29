# Use the official UBUNTU IMAGE.
FROM ubuntu:20.04 

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./


#timing
ENV TZ=Europe/Rome
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install production dependencies.
RUN apt-get update
RUN apt-get -y install python3.8 python3-pip 
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN apt-get -y install ffmpeg

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
#CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
CMD exec pip3 install --upgrade youtube-dl
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 main:app