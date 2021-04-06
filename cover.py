#!/usr/bin/python3

import minimalmodbus
import pika
import time
from pymemcache.client import base

EXCHANGE = 'therminator'

cache = base.Client(('127.0.0.1', 11211))

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange=EXCHANGE, exchange_type='topic')

PORT = '/dev/ttyUSB0'

cache = base.Client(('127.0.0.1', 11211))

is_open = False

def get_device(slave_address, timeout=0.5, baudrate=9600, mode=minimalmodbus.MODE_RTU):
    device = minimalmodbus.Instrument(PORT, slave_address)
    #device.close_port_after_each_call = True
    device.serial.timeout = timeout
    device.serial.baudrate = baudrate
    device.mode = mode
    return device

def get_cover(slave_address):
    # Temperature register 0
    device = get_device(slave_address)
    data = device.read_register(2)
    return data

def turn_cover_fun_on():
    channel.basic_publish(exchange=EXCHANGE, routing_key='jacuzzi.relays.fun', body='ON')

def turn_cover_fun_off():
    channel.basic_publish(exchange=EXCHANGE, routing_key='jacuzzi.relays.fun', body='OFF')


while True:
    is_open = cache.get('Cover_state')
    try:
        cover = get_cover(20)
        current = int(cover)
        if current > 50:
            cover_open = True
        else:
            cover_open = False
        if is_open !=  cover_open:
            # state changed
            if cover_open:
                # set cover fun ON
                turn_cover_fun_on()
            elif not cover_open:
                # set cover fun OFF
                turn_cover_fun_off()

        cache.set('Cover_state', cover_open)
        cache.set('Cover_current', current)
        print("Cover open:", cover_open, current)
    except IOError:
        print("Failed to read from cover")
    time.sleep(5)

