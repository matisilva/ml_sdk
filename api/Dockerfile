FROM python:3.8

ADD ./api/requirements.txt .
RUN pip3 install -r requirements.txt

EXPOSE 80

# TODO remove this when package is done
ADD ./ml_sdk/requirements.txt /app/
RUN pip3 install -r /app/requirements.txt
ADD ./ml_sdk /app/ml_sdk

COPY ./api /app
WORKDIR /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]