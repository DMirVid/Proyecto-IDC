# Proyecto-IDC
Proyecto de clase de la asignarura de IDC. Una estación metereológica en una RaspberryPico W. Los sensores utilizados son: un anenómetro, un DHT22 para temperatura y humedad, un ldr y un sensor de presión y altitud. 
Los datos recogidos se envían a un servidor mqtt, test.mosquitto.org, son recogidos con Telegraf, almacenados en InfluxDB y se muestran con Grafana.
Como característica adicional se intentará implementar una predicción de lluvia con TinyML 


Pasos para desplegar el sistema:
- Abrir terminal en la carpeta del proyecto
- Ejecutar "chmod +x INIT.sh"
- Ejecutar "./INIT.sh"

El sistema ya estará disponible y podrá visualizar los datos en la página web de Grafana que se mostrará despues de ejecutar INIT.sh
Es posible que necesite usuario y contraseña.
- Usuario: admin
- Contraseña: admin
