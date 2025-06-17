#!/bin/bash

 
influx -execute 'CREATE DATABASE telegraf'
influx -execute "CREATE USER telegraf WITH PASSWORD 'uforobot' "
influx -execute 'GRANT ALL ON telegraf TO telegraf'
influx -execute 'CREATE RETENTION POLICY thirty_days ON telegraf DURATION 30d REPLICATION 1 DEFAULT'

echo Base de datos creada correctamente

