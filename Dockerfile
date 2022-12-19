FROM python:3.9-slim-buster

WORKDIR /app

RUN pip install -U pip && \
    mkdir data

COPY ["data/model.tflite", "./data/"]

COPY [ "*.py", "start.sh", "./" ]

RUN pip install https://github.com/alexeygrigorev/tflite-aws-lambda/raw/main/tflite/tflite_runtime-2.7.0-cp39-cp39-linux_x86_64.whl && \
    pip install flask gunicorn streamlit numpy pillow

CMD ["./start.sh"]
