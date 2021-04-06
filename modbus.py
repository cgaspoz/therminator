#!/usr/bin/python3

import minimalmodbus
import time
from pymemcache.client import base

PORT = '/dev/ttyUSB0'

thermostats = {10:'Jacuzzi', 11:'Pump', 12:'Swim', 13:'Boiler', 14:'Freeze'}

cache = base.Client(('127.0.0.1', 11211))

def get_device(slave_address, timeout=0.5, baudrate=9600, mode=minimalmodbus.MODE_RTU):
    device = minimalmodbus.Instrument(PORT, slave_address)
    #device.close_port_after_each_call = True
    device.serial.timeout = timeout
    device.serial.baudrate = baudrate
    device.mode = mode
    return device

def open_relay(relay, slave_address=2):
    # Temperature register 0
    device = get_device(slave_address)
    data = device.write_register(relay, 256, functioncode=6)
    return data

def close_relay(relay, slave_address=2):
    device = get_device(slave_address)
    data = device.write_register(relay, 512, functioncode=6)
    return data

def momentary(relay, slave_address=2):
    device = get_device(slave_address)
    data = device.write_register(relay, 1280, functioncode=6)
    return data

def read_all(slave_address=2):
    device = get_device(slave_address)
    data = device.read_register(1, 8, functioncode=3)
    return data

def open_all(slave_address=2):
    device = get_device(slave_address)
    data = device.write_register(0, 1792, functioncode=6)
    return data

def close_all(slave_address=2):
    device = get_device(slave_address)
    data = device.write_register(0, 2048, functioncode=6)
    return data
