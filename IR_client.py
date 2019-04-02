import socket
import sys
import RPi.GPIO as GPIO
import time

sensor = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor,GPIO.IN)
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
                    inp_sensor=GPIO.input(sensor)
                    if inp_sensor==0 and already_sent==0:
                        send_data()
                        print(inp_sensor)
                        already_sent=1
                    elif inp_sensor==1:
                        if already_sent==1:
                            already_sent=0
            except KeyboardInterrupt:
                GPIO.cleanup()
                soc.sendall("q".encode("utf8"))
                break
        except:
            pass
def send_data():
    message="IR:door opened"
    soc.sendall(message.encode("utf8"))

if __name__ == "__main__":
    main()

