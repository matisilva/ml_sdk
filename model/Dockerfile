FROM python:3.5

RUN pip3 install \
    spanish_sentiment_analysis==1.0.0 \
    ipython==7.8.0 \
    redis==3.3.11

ADD ./ /src/

WORKDIR /src
