#echo Eliminando instancias anteriores
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
#sudo docker exec influxdb influx -execute "SHOW USERS"
echo Puede visualizar los datos en http://localhost:3000/d/c6088c92-c3c7-43ba-86da-f36260cf5d6a/altitud?orgId=1&from=now-6h&to=now&timezone=browser&refresh=5s