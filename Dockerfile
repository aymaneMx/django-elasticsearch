# Dockerfile from https://learndjango.com/tutorials/django-docker-and-postgresql-tutorial

# Pull base image
FROM python:3.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
# not `pip install pipenv` because of https://github.com/pypa/pipenv/issues/4273
RUN pip install 'pipenv==2018.11.26'
COPY Pipfile Pipfile.lock /code/
RUN pipenv install --system

# Copy project
COPY . /code/