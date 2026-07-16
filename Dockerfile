FROM python:3.12-slim
WORKDIR /app

RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

ENV DOCKER_ENVIRONMENT=yes
ENV TZ=Australia/Melbourne

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p /app/challenges

COPY ./src/generators/challenge-generation-crontab /etc/cron.d/my-crontab
RUN chmod 0644 /etc/cron.d/my-crontab && touch /var/log/cron.log

CMD ["sh", "-c", "DOCKER_ENVIRONMENT=yes /usr/local/bin/python /app/src/generators/challenge_file_generator.py >> /var/log/cron.log 2>&1 && cron && fastapi run src/main.py --host 0.0.0.0 --port 8000"]
