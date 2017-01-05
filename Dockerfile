FROM python:3.5.2-slim

WORKDIR /app/
RUN groupadd --gid 1001 app && useradd -g app --uid 1001 --shell /usr/sbin/nologin app

RUN apt-get update && \
    apt-get install -y gcc apt-transport-https

COPY ./requirements.txt /app/requirements.txt

RUN pip install -U 'pip>=8' && \
    pip install --no-cache-dir -r requirements.txt

# Install the app
COPY . /app/

# Set Python-related environment variables to reduce annoying-ness
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH=.

USER app

CMD python crashmill/app.py
