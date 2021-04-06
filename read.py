#!/usr/bin/python3

from gpiozero import Button
from signal import pause

water = Button(4, pull_up=False)
pump = Button(5)
fun = Button(6)
heat = Button(13)
auto = Button(17)
alarm = Button(19)
swim = Button(22)
stop = Button(26)
start = Button(27)

def water_tick():
    print("Water tick")

def pump_on():
    print("Pump ON")

def pump_off():
    print("Pump OFF")

def fun_on():
    print("Fun ON")

def fun_off():
    print("Fun OFF")

def heat_on():
    print("Heat ON")

def heat_off():
    print("Heat OFF")

def auto_on():
    print("Auto ON")

def auto_off():
    print("Auto OFF")

def alarm_on():
    print("Alarm ON")

def alarm_off():
    print("Alarm OFF")

def swim_on():
    print("Swim ON")

def swim_off():
    print("Swim OFF")

def stop_on():
    print("Stop ON")

def stop_off():
    print("Stop OFF")

def start_on():
    print("Start ON")

def start_off():
    print("Start OFF")

water.when_pressed = water_tick

if pump.is_pressed:
    pump_on()
else:
    pump_off()

pump.when_pressed = pump_on 
pump.when_released = pump_off

if fun.is_pressed:
    fun_on()
else:
    fun_off()

fun.when_pressed = fun_on 
fun.when_released = fun_off

if heat.is_pressed:
    heat_on()
else:
    heat_off()

heat.when_pressed = heat_on 
heat.when_released = heat_off

if auto.is_pressed:
    auto_on()
else:
    auto_off()

auto.when_pressed = auto_on 
auto.when_released = auto_off

if alarm.is_pressed:
    alarm_on()
else:
    alarm_off()

alarm.when_pressed = alarm_on 
alarm.when_released = alarm_off

if swim.is_pressed:
    swim_on()
else:
    swim_off()

swim.when_pressed = swim_on 
swim.when_released = swim_off

if stop.is_pressed:
    stop_on()
else:
    stop_off()

stop.when_pressed = stop_on 
stop.when_released = stop_off

if start.is_pressed:
    start_on()
else:
    start_off()

start.when_pressed = start_on 
start.when_released = start_off

pause()
