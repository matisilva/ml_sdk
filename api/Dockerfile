FROM python:3.5

RUN pip3 install \
    flask==1.1.1 \
    gunicorn==19.9.0 \
    redis==3.3.11

ADD ./ /src/

WORKDIR /src
