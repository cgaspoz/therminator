#!/usr/bin/python3

import json
import minimalmodbus
import pika
import struct
import time
from pymemcache.client import base
from pymemcache import serde

PORT = '/dev/ttyUSB0'
EXCHANGE = 'therminator'
QUEUE = 'modbus_relays'

cache = base.Client(('127.0.0.1', 11211), serde=serde.pickle_serde)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange=EXCHANGE, exchange_type='topic')

result = channel.queue_declare(QUEUE)
channel.queue_bind(exchange=EXCHANGE, queue=QUEUE, routing_key='jacuzzi.relays.*')

def get_device(slave_address, timeout=0.5, baudrate=9600, mode=minimalmodbus.MODE_RTU):
    device = minimalmodbus.Instrument(PORT, slave_address)
    #device.close_port_after_each_call = True
    device.serial.timeout = timeout
    device.serial.baudrate = baudrate
    device.mode = mode
    return device

def momentary(relay, slave_address=2):
    device = get_device(slave_address)
    data = device.write_register(relay, 1280, functioncode=6)
    return data

def read_all(slave_address=2):
    retry = True
    print("Reading all relays state...")
    while retry:
        try:
            device = get_device(slave_address)
            data = device.read_string(1, 8).encode()
            retry = False
        except IOError:
            print("Failed to read modbus")
            time.sleep(1)
    return list(struct.unpack('16B', data))[1::2]

def close_all(slave_address=2):
    retry = True
    print("Closing all relays...")
    while retry:
        try:
            device = get_device(slave_address)
            data = device.write_register(0, 2048, functioncode=6)
            retry = False
        except IOError:
            print("Failed to write modbus")
            time.sleep(1)
    print("All relays closed")
    return data

def send_momentary(relay):
    retry = True

    while retry:
        try:
            momentary(relay)
            retry = False
            print("Succeed to write modbus")
        except IOError:
            print("Failed to write modbus")
            time.sleep(1)

def set_status(status):
    if status == 0:
        return False
    elif status == 1:
        return True
    else:
        return status

def callback(ch, method, properties, body):
    print(ch, method, properties, body)
    action = method.routing_key.split('.')[-1]
    command = body.decode()

    relay = None

    if action == 'heat':
        if command == 'ON':
            relay = 1
            print("Starting heat")
        elif command == 'OFF':
            relay = 4
            print("Stopping heat")
    elif action == 'swim':
        if command == 'ON':
            relay = 2
            print("Starting swim")
        elif command == 'OFF':
            relay = 3
            print("Stopping swim")
    elif action == 'pump':
        if command == 'ON':
            relay = 5
            print("Starting pump")
        elif command == 'OFF':
            relay = 6
            print("Stopping pump")
    elif action == 'fun':
        if command == 'ON':
            relay = 7
            print("Starting fun")
        elif command == 'OFF':
            relay = 8
            print("Stopping fun")
    elif action == 'status':
        status = read_all()
        body = {'heat_ON': set_status(status[0]), 'heat_OFF': set_status(status[3]), 'swim_ON': set_status(status[1]), 'swim_OFF': set_status(status[2]), 'pump_ON': set_status(status[4]), 'pump_OFF': set_status(status[5]), 'fun_ON': set_status(status[6]), 'fun_OFF': set_status(status[7])}
        channel.basic_publish(exchange=EXCHANGE, routing_key='jacuzzi.state.relays', body=json.dumps(body))
        print("All relays states: {}".format(body))

    if relay:
        send_momentary(relay)

print("Starting relays")

close_all()

print("Start listening queue %s..." % QUEUE)

channel.basic_consume(
    queue=QUEUE, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
