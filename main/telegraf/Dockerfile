[agent]
    flush_interval = "15s"
    interval = "15s"

[[inputs.mqtt_consumer]]
    name_override = "estacion_meteorologica"
    servers = ["tcp://test.mosquitto.org:1883"]
    qos = 0
    connection_timeout = "30s"
    topics = [ "idc/estacion_metereologica/datos" ]
    client_id = "telegraf_estacion"
    data_format = "json"
    json_string_fields = ["viento", "humedad", "presion", "temperatura", "altitud", "ldr"]

[[outputs.influxdb]]
    database = "telegraf"
    urls = [ "http://localhost:8086" ]
    username = "telegraf"
    password = "uforobot"
