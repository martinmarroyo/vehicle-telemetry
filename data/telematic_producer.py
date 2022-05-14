"""
A script that creates a mock data stream of
vehicle telemetry data from the Telematicsdata.csv
and writes it to a Kafka topic called VehicleTelemetry.

For the sake of the simulation, we have the data stream in
at a rate of 1 reading every 3 seconds.
"""
import json
import logging
from time import sleep
from dotenv import dotenv_values
from kafka import KafkaProducer
from kafka.errors import KafkaError

logging.basicConfig(
    level=logging.INFO,
    filename="log_telematic_producer.log",
    encoding="utf-8",
    format="%(asctime)s:%(levelname)s:%(message)s",
)
conf = dotenv_values(".env")

if __name__ == "__main__":

    with open(conf["DATAFILE"],encoding='utf-8') as telemetry:
        # Set up our data feed and producer
        header = [
            "deviceId",
            "timeMili",
            "timestamp",
            "value",
            "variable",
            "alarmClass",
        ]
        next(telemetry)  # Skip header row
        producer = KafkaProducer(bootstrap_servers=["localhost:9092"])
        logging.info("Starting stream...")
        for reading in telemetry:
            # Get record attributes into a dictionary and convert to json
            record = {}
            attributes = reading.split(",")
            for col, val in zip(header, attributes):
                record[col] = val
            try:
                converted = json.dumps(record).encode("utf-8")
                producer.send(
                    "VehicleTelemetry",
                    value=converted,
                    key=record["deviceId"].encode("utf-8"),
                )
                sleep(3) # Simulates delay between readings
            except KafkaError:
                print("Error occurred")
                logging.exception("Error occurred during stream writing")
