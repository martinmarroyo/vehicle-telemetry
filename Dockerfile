FROM python:3.8

WORKDIR /vehicle-telemetry

COPY . .

RUN pip install -r requirements.txt

CMD ["tail",  "-f", "/dev/null"]
