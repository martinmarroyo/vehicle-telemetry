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

## Architecture & Data Flow

![Telemetry Reading Architecture Overview](https://github.com/martinmarroyo/vehicle-telemetry/blob/ca880d13b67eed263934e6772390514668d71598/VehicleTelemetryArchitecture-Overview.PNG)

## Implementation Plan
The high-level plan for building an analytics solution to monitor and report this data involves ingesting the data as it streams in, processing it (either in real-time, for later analysis, or both), and storing it somewhere for use in reporting tools down the line. I chose Apache Kafka to handle the data streams. This is because Kafka is an efficient Log store system, which is perfect for handling the streaming telemetry log data. On top of that, it's distributed and highly available making which would allow for wide scaling in the future. 

Now that I knew how I would be ingesting the data, I needed a way to process it as it streams in. While this could be done using regular Python, it won't scale too well. This is where Apache Spark (PySpark) comes in. Using Spark, I can ingest and do some calculations on the data as it streams in real-time. Then I can send the data off to a file store continuously. Spark allows me to do this at scale due to the distributed processing that it makes available.

Next, I needed a place to keep the data as it was ingested and processed. For this, I chose S3 since storage there is inexpensive and flexible. From here, I could choose to push the data down to a relational or document database. S3 also allows direct querying of the data using Athena, so there are plenty of options for setting up a reporting system after collection and storage. If I were to store the data in a relational database, I would likely choose BigQuery as a distributed warehouse solution since it scales and integrates with many different reporting systems.

## Implementation Details

### Ingestion, Processing, and Storage (Still in progress)
To start, I needed to simulate the data stream coming from the vehicle sensors, so I created a Kafka Producer that would feed a line of data every second from my [data source.](https://github.com/martinmarroyo/vehicle-telemetry/blob/978822a1ef771758c6a548284e3e4186baa2326f/data/Telematicsdata.csv) The producer reads a line from the data source, converts the values to JSON, and then publishes it to a Kafka Topic called `VehicleTelemetry`. [Here is the code](https://github.com/martinmarroyo/vehicle-telemetry/blob/978822a1ef771758c6a548284e3e4186baa2326f/data/telematic_producer.py) for the producer.

Next, I created a Kafka Consumer that subscribes to the `VehicleTelemetry` topic and ingests the incoming data. From there, we do some light transformations on the data (converting to appropriate data types and stripping uneccessary characters from strings). Then the results are pushed to a data lake in S3 where it will be stored for future analysis. The code for the consumer can be found [here.](https://github.com/martinmarroyo/vehicle-telemetry/blob/978822a1ef771758c6a548284e3e4186baa2326f/ingest/telematic_consumer.py)

### Notes going forward
The current implementation uses plain Python to process the data. However, I plan on implementing the consumer in PySpark soon to better represent what a scalable solution might look like. Then I have to decide how I would want to store the data for processing after it arrives in our data lake. I'm leaning towards the data warehouse route, but this will also depend on what my downstream reporting solution would look like. If it were a web app, I'd likely lean more towards a document store database than a relational one, but I feel as if I'm more likely to use Tableau or Data Studio. These are easier to integrate with relational databases. 
