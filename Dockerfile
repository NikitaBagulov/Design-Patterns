FROM python:3.12-alpine AS base
WORKDIR /app
EXPOSE 8080

RUN pip3 install typing-extensions --upgrade
RUN pip3 install dict2xml
RUN pip3 install -U connexion[flask]
RUN pip3 install -U connexion[swagger-ui]
RUN pip3 install -U connexion[uvicorn]
RUN pip3 install -U flask-restplus
RUN pip3 install -U Flask


COPY ./src /app/src
COPY ./docs /app/docs
COPY ./main.py /app/main.py
COPY ./swagger.yaml /app/swagger.yaml

CMD ["python", "main.py"]