up:
	docker-compose up --build -d 

restart:
	docker-compose up -d
	
down:
	docker-compose down

start-stream:
	docker exec -d vehicle-telemetry python data/telematic_producer.py 

sh:
	docker exec -ti vehicle-telemetry bash

view-stream:
	docker exec -it kafka-broker kafka-console-consumer --bootstrap-server kafka-broker:9092 --topic VehicleTelemetry --from-beginning
