FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y cron
COPY requirements.txt ./

ENV DOCKER_ENVIRONMENT='yes'
ENV TZ=Australia/Melbourne

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

COPY .env .

COPY ./src/generators/challenge-generation-crontab /etc/cron.d/my-crontab
RUN chmod 0644 /etc/cron.d/my-crontab
RUN touch /var/log/cron.log
RUN crontab /etc/cron.d/my-crontab
CMD ["sh", "-c", "cron -f & tail -f /var/log/cron.log"]
