#!/usr/bin/python3

import time
from gpiozero import Button
from pymemcache.client import base
from pymemcache import serde
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

debug = True

temperature_keys = ['Swim_temperature', 'Freeze_temperature']

cache = base.Client(('127.0.0.1', 11211), serde=serde.pickle_serde)

current_milli_time = lambda: int(round(time.time() * 1000))

past_time = current_milli_time()-1

l = 0

countable = cache.get('water')

#initialisation on boot
if type(countable) != type(dict()):
    countable = {}

    f = open("/home/cgaspoz/therminator/meter/totJin", 'r')
    totJin = int(f.readline())
    countable['totJin'] = totJin
    f.close()

    f = open("/home/cgaspoz/therminator/meter/totJout", 'r')
    totJout = int(f.readline())
    countable['totJout'] = totJout
    f.close()

    f = open("/home/cgaspoz/therminator/meter/totLitres", 'r')
    totLitres = int(f.readline())
    countable['totLitres'] = totLitres
    f.close()

    print("Read", totJin, totJout, totLitres)
    cache.set('water', countable)

io_states = cache.get('io_states')

#initialisation on boot
if type(io_states) != type(dict()):
    io_states = {}


def water_tick():
    global past_time
    global l
    global countable
    print("Water tick")
    current_time = current_milli_time()
    temperatures = cache.get_many(temperature_keys)
    if temperatures:
        jtemp = float(temperatures['Swim_temperature'])
        rtemp = float(temperatures['Freeze_temperature'])
        dtemp = rtemp - jtemp
    else:
        jtemp = None
        rtemp = None
        dtemp = None

    tick_duration = current_time - past_time
    
    if debug:
        print("Rising edge, duration=", tick_duration, "temp aller=", jtemp, "temp retour=", rtemp, "dif=", dtemp)
    if l > 0 and tick_duration > 0:
        lth = 36000000/tick_duration
        ltm =   600000/tick_duration 

        joules = int(dtemp * 4190 )
        power = int(dtemp * lth * 4.19 / 3.6)

        if joules > 0 :
            countable['totJin'] += joules
            if l % 100 == 0: # preserve la flash ;)
                f = open("/home/cgaspoz/therminator/meter/totJin", 'w')
                f.write(str(countable['totJin']) + "\n")
                f.close()
        else:
            countable['totJout'] -= joules
            if l % 100 == 0: # preserve la flash ;)
                f = open("/home/cgaspoz/therminator/meter/totJout", 'w')
                f.write(str(countable['totJout']) + "\n")
                f.close()

        if debug:
            print("lth=", lth, "ltm=", ltm, "power=", power, "joules=", joules, "inJ=", countable['totJin'], "outJ=", countable['totJout'], "totLitres=", countable['totLitres'])

    countable['totLitres'] += 10
    if l % 100 == 0: # preserve la flash ;)
        f = open("/home/cgaspoz/therminator/meter/totLitres", 'w')
        f.write(str(countable['totLitres']) + "\n")
        f.close()

    cache.set('water', countable)
    past_time = current_time
    l += 10

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
