FROM python:3.10

LABEL Author="Mikael"

RUN mkdir /app
WORKDIR /app

COPY . ./

RUN pip install -r requirements.txt


ENTRYPOINT ["python", "main.py"]