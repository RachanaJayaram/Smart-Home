import socket
import sys
from gpiozero import LightSensor, Buzzer
import time

sensor = 18
ldr = LightSensor(18) 
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 8888
def main():
    already_sent=0
    #twice=0
    while True:
        try:
            soc.connect((host, port))
            try: 
                while True:
                    inp_sensor=ldr.value
                    if inp_sensor<0.05 and already_sent==0:
                        send_data()
                        print(inp_sensor)
                        already_sent=1
                    elif inp_sensor==1:
                        if already_sent==1:
                            already_sent=0
            except KeyboardInterrupt:
                sys.exit()
                break
        except:
            pass
def send_data():
    message="LDR:lighting_changed"
    soc.sendall(message.encode("utf8"))

if __name__ == "__main__":
    main()
