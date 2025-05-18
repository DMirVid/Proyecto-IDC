# Proyecto-IDC
Proyecto de clase de la asignarura de IDC. Una estación metereológica en una RaspberryPico W. Los sensores utilizados son: un anenómetro, un DHT22 para temperatura y humedad, un ldr y un sensor de presión y altitud. 
Los datos recogidos se envían a un servidor mqtt, test.mosquitto.org, son recogidos con Telegraf, almacenados en InfluxDB y se muestran con Grafana.
Como característica adicional se intentará implementar una predicción de lluvia con TinyML 
