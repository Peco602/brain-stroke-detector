FROM python:3.9-slim-buster

WORKDIR /app

RUN pip install -U pip && \
    pip install pipenv && \
    mkdir data

COPY ["data/model.tflite", "./data/"]

COPY [ "Pipfile", "Pipfile.lock", "*.py", "start.sh", "./" ]

RUN pip install https://github.com/alexeygrigorev/tflite-aws-lambda/raw/main/tflite/tflite_runtime-2.7.0-cp39-cp39-linux_x86_64.whl && \
    pipenv install --system --deploy

EXPOSE 8051
EXPOSE 8080

CMD ["./start.sh"]
