echo Eliminando instancias anteriores
sudo docker rm -f $(sudo docker ps -aq)

echo Iniciando contenedores
sudo docker compose -f ./main/docker-compose.yml up -d
for i in {1..10}
do 
    echo -n .
    sleep 0.2
done
echo .
sudo docker exec influxdb ./run.sh
sudo docker exec influxdb influx -execute "SHOW USERS"
echo Puede visualizar los datos en http://localhost:3000