to create the docker image:
sudo docker build -t gdal_python:latest .

to run the docker volume:
sudo docker run --name gdal_test_volume -v ${PWD}:/app -p 5000:5000 gdal_python

to enter terminal of the volume
sudo docker exec -it gdal_test_volume /bin/sh