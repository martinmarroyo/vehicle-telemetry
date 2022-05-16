"""
A script that creates a mock data stream of
vehicle telemetry data from the Telematicsdata.csv
and writes it to a Kafka topic called VehicleTelemetry.

For the sake of the simulation, we have the data stream in
at a rate of 1 reading every 3 seconds.
"""
"""
A script that creates a mock data stream of
vehicle telemetry data from the Telematicsdata.csv
and writes it to a Kafka topic called VehicleTelemetry.
For the sake of the simulation, we have the data stream in
at a rate of 1 line per second.
"""
import json
import logging
from time import sleep
import pandas as pd
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
    # Set up our data feed and producer
    telemetry = pd.read_csv(conf["DATAFILE"])
    producer = KafkaProducer(bootstrap_servers=["localhost:9092"])

    logging.info("Starting stream...")
    # Creates a mock stream of telemetry data
    for row in telemetry.iterrows():
        converted = json.dumps(
            {
                "deviceId": row[1]["deviceId"],
                "timeMili": row[1]["timeMili"],
                "timestamp": row[1]["timestamp"],
                "value": row[1]["value"],
                "variable": row[1]["variable"],
                "alarmClass": row[1]["alarmClass"],
            }
        )
        converted = converted.encode("utf-8")
        try:
            producer.send(
                "VehicleTelemetry",
                value=converted,
                key=row[1]["deviceId"].encode("utf-8"),
            )
            sleep(1)
        except KafkaError:
            print("Error occurred...")
            logging.exception("Something went wrong with our Kafka connection")
