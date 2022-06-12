up:
	docker-compose up --build -d 

restart:
	docker-compose up
	
down:
	docker-compose down

start-stream:
	docker exec -d vehicle-telemetry python data/telematic_producer.py 

sh:
	docker exec -ti vehicle-telemetry bash

view-stream:
	docker exec -it broker \ 
	kafka-console-consumer \
	--bootstrap-server broker:9092 \
	--topic VehicleTelemetry \
	--from-beginning