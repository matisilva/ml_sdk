FROM python:3.8

ADD ./model /src/

# TODO remove this when package is done
ADD ./ml_sdk /src/ml_sdk
RUN pip3 install -r /src/ml_sdk/requirements.txt

RUN pip3 install -r /src/requirements.txt
WORKDIR /src
CMD ["python", "service.py"]