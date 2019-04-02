import socket
import sys 
import traceback #For threading error debugging
from threading import Thread
from lights_servo import * 

outside_lights={19:0,26:0} #pin dictionary value is 0 if light is off / value is 1 if light is on
inside_lights={20:0,21:0}
outside_lights_obj={19:LED(19),26:LED(26)} # Dictionary with LED object as value
inside_lights_obj={20:LED(20),21:LED(21)}
door="closed" # stores state of the board
def main():
    start_server()
    
def start_server():
    host = "127.0.0.1" #localhost   
    port = 8888       

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET ->address family IPv4 SOCK_STREAM ->type of connection 
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    # To solve address already in use error when you try to run the program again immediately after closing it
    # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire

    try:
        soc.bind((host, port)) #Bind the socket to address
    except:
        print("Bind failed:" + str(sys.exc_info()))
        sys.exit()
    
    soc.listen(5)       # queue up to 5 connection requests from clients
    print("Socket now listening")

    while True:
        try :
            connection, address = soc.accept()
             #accept connection from client and get connection object(useful for recieving and sending data) address is address of the client
            
            ip, port = str(address[0]), str(address[1])
            print("Connected with " + ip + ":" + port)
            #get ip and port of client


            try:
                Thread(target=client_thread, args=(connection, ip, port)).start()
                #start a new thread to service the client. Multiple threads makes it possible  to service multiple clients simultaneously

            except:
                print("Thread did not start.")
                traceback.print_exc()
                #error handling

        except KeyboardInterrupt:
            soc.close()
            turn_off_inside_lights(inside_lights,inside_lights_obj)
            turn_off_outside_lights(outside_lights,outside_lights_obj)
            #turn off lights before shutting down
            break    



def client_thread(connection, ip, port, max_buffer_size = 5120):
    print("New Thread Started for client- ",ip,':',port)
    is_active = True
    global outside_lights
    global inside_lights
    global door
    #access global variables

    while is_active:
            client_input = receive_input(connection, max_buffer_size) #recieve data from client using recieve_data function
            if(len(str(client_input))>4):
                print("Processed result: {}".format(client_input)) #print processed data 
            else:
                continue
            if client_input=="q":
                is_active=False
                connection.close() #close connection with this client upon clients request
                print("Connection " + ip + ":" + port + " closed")
                break
    
            input_list=client_input.split(':')
            print(input_list)

            #action taken depending on message sent by client
            if input_list[0]=="IR":
                if inside_lights[20]==0:
                    inside_lights=turn_on_inside_lights(inside_lights,inside_lights_obj)
                else:
                    inside_lights=turn_off_inside_lights(inside_lights,inside_lights_obj)
            
            if input_list[0]=="LDR":
                if input_list[1]=="turn_on":
                    outside_lights=turn_on_outside_lights(outside_lights,outside_lights_obj)
                else:
                    outside_lights=turn_off_outside_lights(outside_lights,outside_lights_obj)
            if input_list[0]=="mic":
                inside_lights,outside_lights,door,reply=message_decode(input_list[1],inside_lights,outside_lights,inside_lights_obj,outside_lights_obj,door,p)
                connection.send(reply.encode())
            
            



def receive_input(connection, max_buffer_size):
    client_input = connection.recv(max_buffer_size) #recieve data from client
    client_input_size = sys.getsizeof(client_input)

    if client_input_size > max_buffer_size:
        print("The input size is greater than expected {}".format(client_input_size))

    decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line (from b)

    return decoded_input



if __name__ == "__main__":
    main()
