import time
from gpiozero import LED
import RPi.GPIO as GPIO

p = GPIO.PWM(servoPIN, 50) 
servoPIN = 15
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)



def turn_on_outside_lights(outside_lights,outside_lights_obj,*argv):
    for key in outside_lights.keys():
        outside_lights[key]=1
        outside_lights_obj[key].on()
    return outside_lights
def turn_off_outside_lights(outside_lights,outside_lights_obj):
    for key in outside_lights.keys():
        outside_lights[key]=0
        outside_lights_obj[key].off()
        time.sleep(2)
    return outside_lights
def turn_on_inside_lights(inside_lights,inside_lights_obj):
    for key in inside_lights.keys():
        inside_lights[key]=1
        inside_lights_obj[key].on()
    return inside_lights
def turn_off_inside_lights(inside_lights,inside_lights_obj):
    for key in inside_lights.keys():
        inside_lights[key]=0
        inside_lights_obj[key].off()
        time.sleep(2)
    return inside_lights

def turn_on_all_lights(inside_lights,outside_lights,inside_lights_obj,outside_lights_obj):
    inside_lights=turn_on_inside_lights(inside_lights,inside_lights_obj)
    outside_lights=turn_on_outside_lights(outside_lights,outside_lights_obj)
    return (inside_lights,outside_lights)

def turn_off_all_lights(inside_lights,outside_lights,inside_lights_obj,outside_lights_obj):
    inside_lights=turn_off_inside_lights(inside_lights,inside_lights_obj)
    outside_lights=turn_off_outside_lights(outside_lights,outside_lights_obj)
    return (inside_lights,outside_lights)

def open_door(door,p):
    if door="closed":
        door="open"
        p.start(1) 
        p.ChangeDutyCycle(10)
    return door

def close_door(door,p):
    if door="open":
        door="closed"
        p.ChangeDutyCycle(1)
        p.stop()
    return door

def message_decode(command ,inside_lights,outside_lights,inside_lights_obj,outside_lights_obj,door,p):

    tokens=command.split()
    tokens=[token.lower() for token in tokens]
    reply=""
    if  set(['on','inside','lights']).issubset(set(tokens)):
        inside_lights=turn_on_inside_lights(inside_lights,inside_lights_obj)
        reply="Inside Lights Are On"
    elif set(['on','outside','lights']).issubset(set(tokens)): 
        outside_lights=turn_on_outside_lights(outside_lights,outside_lights_obj)
        reply="Outside Lights Are on"
    elif set(['on','lights']).issubset(set(tokens)): 
        (inside_lights,outside_lights)=turn_on_all_lights(inside_lights,outside_lights,inside_lights_obj,outside_lights_obj)
        reply= "Lights are on"
    elif set(['off','inside','lights']).issubset(set(tokens)): 
        inside_lights=turn_off_inside_lights(inside_lights,inside_lights_obj)
        reply= "Inside lights are off"
    elif set(['off','outside','lights']).issubset(set(tokens)): 
        outside_lights=turn_off_outside_lights(outside_lights,outside_lights_obj)
        reply= "Outside Lights are off"
    elif set(['off','lights']).issubset(set(tokens)): 
        (inside_lights,outside_lights)=turn_off_all_lights(inside_lights,outside_lights,inside_lights_obj,outside_lights_obj)
        reply="Lights are off"
    elif set(['open','door']).issubset(set(tokens)): 
        door=open_door(door,p)
        reply= "The door is open"
    elif set(['close','door']).issubset(set(tokens)):
        door=close_door(door,p)
        reply= "The door is closed"
    return (inside_lights,outside_lights,door,reply)
