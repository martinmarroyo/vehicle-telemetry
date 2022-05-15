"""
A script that consumes vehicle telemetry data 
from a subscribed Kafka Topic, processes it, 
and stores it in a datalake on AWS S3. 
"""
import logging
import json
from datetime import datetime
import boto3
from dotenv import dotenv_values
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from botocore.exceptions import ClientError

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        filename="log_telematic_producer.log",
        encoding="utf-8",
        format="%(asctime)s:%(levelname)s:%(message)s",
    )
    conf = dotenv_values(".env")
    consumer = KafkaConsumer("VehicleTelemetry", bootstrap_servers=[conf['KAFKA_BROKER']])
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=conf["ACCESS_KEY"],
        aws_secret_access_key=conf["SECRET_ACCESS_KEY"],
    )

    logging.info("Starting process")
    try:
        for message in consumer:
            # Process data
            vehicle_id = message.key.decode("utf-8")
            payload = json.loads(message.value.decode("utf-8"))
            payload["value"] = payload["value"].replace('"', "")
            payload["alarmClass"] = payload["alarmClass"].replace('"', "")
            dt = datetime.strptime(payload["timestamp"], "%Y-%m-%d %H:%M:%S.%f")
            # Set up object name and push to s3
            obj_name = (
                "us/vehicle-telemetry-data"
                f"/vehicle-id={vehicle_id}"
                f"/year={dt.year}"
                f"/month={dt.month}"
                f"/day={dt.day}"
                f"/hour={dt.hour}"
                f"/minute={dt.minute}"
                f"/{vehicle_id}-{dt.second}.json"
            )
            try:
                s3_client.put_object(
                    Body=json.dumps(payload), Bucket=conf["RAW_BUCKET"], Key=obj_name
                )
            except ClientError:
                logging.exception("Error uploading to s3")
    except KafkaError:
        logging.exception("Error with Kafka")
