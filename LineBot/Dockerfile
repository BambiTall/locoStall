# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8.17-bullseye

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Install uWSGI and Nginx
RUN apt-get update && apt-get install -y uwsgi uwsgi-plugin-python3 nginx

# Create a directory for the Nginx configuration
RUN mkdir -p /etc/nginx/sites-available

# Copy the Nginx configuration to the container
COPY nginx.conf /etc/nginx/sites-available/default

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD uwsgi --socket 127.0.0.1:8000 --plugin python3 --wsgi-file app.py --callable app --master --processes 4 --threads 2 --daemonize /var/log/uwsgi.log