#!/usr/bin/python3

import minimalmodbus
import time
from pymemcache.client import base
from pymemcache import serde

PORT = '/dev/ttyUSB0'

thermostats = {10:'Jacuzzi', 11:'Pump', 12:'Swim', 13:'Boiler', 14:'Freeze'}

cache = base.Client(('127.0.0.1', 11211), serde=serde.pickle_serde)

def get_device(slave_address, timeout=0.5, baudrate=9600, mode=minimalmodbus.MODE_RTU):
    device = minimalmodbus.Instrument(PORT, slave_address)
    #device.close_port_after_each_call = True
    device.serial.timeout = timeout
    device.serial.baudrate = baudrate
    device.mode = mode
    return device

def get_temperature(slave_address):
    # Temperature register 0
    device = get_device(slave_address)
    data = device.read_register(0, 1)
    return data

def get_relay(slave_address):
    # Relay coils 20
    device = get_device(slave_address)
    data = device.read_bit(20, functioncode=1)
    return data

while True:
    for i in thermostats:
        try:
            temperature = get_temperature(i)
            relay = get_relay(i)
            if relay == 0:
                relay = False
            else:
                relay = True
            cache.set(thermostats[i] + "_temperature", temperature)
            cache.set(thermostats[i] + "_relay", relay)
            print(thermostats[i], temperature, relay)
            time.sleep(3)
        except IOError:
            print("Error reading {}".format(thermostats[i]))
        