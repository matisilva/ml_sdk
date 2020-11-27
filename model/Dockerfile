FROM python:3.8

ADD ./model /src/
RUN pip3 install -r /src/requirements.txt

# TODO remove this when package is done
ADD ./ml_sdk/requirements.txt /src/requirements.txt
RUN pip3 install -r /src/requirements.txt
ADD ./ml_sdk/ /src/ml_sdk

WORKDIR /src
CMD ["python", "service.py"]