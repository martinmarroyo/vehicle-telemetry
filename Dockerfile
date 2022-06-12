FROM python:3.8

WORKDIR /vehicle-telemetry

COPY . .

COPY ./data/.env .

RUN pip install -r requirements.txt

CMD ["tail",  "-f", "/dev/null"]