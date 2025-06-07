#!/bin/bash
#No se conecta a inlfux
influx
CREATE DATABASE telegraf
CREATE USER telegraf WITH PASSWORD 'uforobot'
GRANT ALL ON telegraf TO telegraf
CREATE RETENTION POLICY thirty_days ON telegraf DURATION 30d REPLICATION 1 DEFAULT
exit
echo Base de datos creada correctamente
exit
