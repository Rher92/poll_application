FROM alpine:3.10

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

WORKDIR /poll-application
COPY . /poll-application

RUN  pip3 --no-cache-dir install -r requirements.txt

ENV APP_SETTINGS=poll_application.config.DevelopmentConfig
ENV DATABASE_URL=sqlite:////tmp/poll-application.db
ENV FLASK_APP=main.py
ENV PYTHONPATH=/poll-application/poll_application/

EXPOSE 8000
WORKDIR poll_application
CMD flask run --host=0.0.0.0 -p 8000