# Ingesting Vehicle Telemetry Data at Scale
A practice project for ingesting, storing, and processing of streaming vehicle telemetry data.

## Motivation for this project
Normally, I work with batch data processing. However, I wanted to gain more experience processing streaming data and architecting systems that could scale. My main goals are:
- To practice working with streaming datasets (Apache Kafka)
- To practice working with distributed systems (Apache Spark, BigQuery, etc)
- To learn best practices in the design and implementation of distributed data systems

## Data Source
I was able to grab some vehicle telemetry data from [here](https://www.kaggle.com/datasets/ankitp013/automobile-telematics-dataset?resource=download) to work with. The dataset tracks multiple sensors on multiple vehicles over the course of several days. Metrics that are collected monitor car behavior like speeding, accelerating, turning, breaking etc. Since the original source is static, I wrote a Kafka Producer that simulates streaming the data as text/JSON. The script is available [here.](https://github.com/martinmarroyo/vehicle-telemetry/blob/main/data/telematic_producer.py)

### Schema
- **deviceId**: The unique identifier of the sensor *(String)*
- **timeMili**: The timestamp of the emitted event in milliseconds *(Long)*
- **timestamp**: The timestamp of the Parameter ID (PID) captured *(Timestamp)*
- **value**: The diagnostic values observed for the PID *(Numeric)*
- **variable**: The captured parameter ID (PID) *(String)*
- **alarmClass**: A threshold value for each PID observed per sampling time *(Integer: 0-5)*


