#!/usr/bin/env python3

import ast
import datetime
import time
from influxdb import InfluxDBClient
from pymemcache.client import base
from pymemcache import serde

cache = base.Client(('127.0.0.1', 11211), serde=serde.pickle_serde)

temperatures = ['Jacuzzi_temperature', 'Pump_temperature', 'Swim_temperature', 'Boiler_temperature', 'Freeze_temperature']
relays = ['Jacuzzi_relay', 'Pump_relay', 'Swim_relay', 'Boiler_relay', 'Freeze_relay']
covers = ['Cover_state', 'Cover_current']

# influx configuration - edit these
ifuser = "grafana"
ifpass = "jacuzzi4fun!"
ifdb   = "therminator"
ifhost = "127.0.0.1"
ifport = 8086

while True:
    # take a timestamp for this measurement
    current_time = datetime.datetime.utcnow()

    temperatures_keys = cache.get_many(temperatures)
    relays_keys = cache.get_many(relays)
    cover_keys = cache.get_many(covers)
    water = cache.get('water')

    temperature_fields = {}
    for key in temperatures_keys:
        temperature_fields[key.split('_')[0]] = temperatures_keys[key]

    relay_fields = {}
    for key in relays_keys:
        relay_fields[key.split('_')[0]] = relays_keys[key]

    body = [
        {
            "measurement": 'temperatures',
            "time": current_time,
            "fields": temperature_fields
        },
        {
            "measurement": 'relays',
            "time": current_time,
            "fields": relay_fields
        },
        {
            "measurement": 'cover',
            "time": current_time,
            "fields": {'state': cover_keys['Cover_state'], 'current': cover_keys['Cover_current']}
        },
        {
            "measurement": 'water',
            "time": current_time,
            "fields": {'joules_in': water['totJin'], 'joules_out': water['totJout'], 'liters': water['totLitres']}
        },
        
    ]

    # connect to influx
    ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)

    # write the measurement
    ifclient.write_points(body)
    time.sleep(60)
