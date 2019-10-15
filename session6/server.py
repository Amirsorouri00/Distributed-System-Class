
import socket


#!/usr/bin/python           # This is server.py file                                                                                                                                                                           

import socket               # Import socket module
import threading

def server_socket():
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 5069               # Reserve a port for your service.

    print('Server started!')
    print('Waiting for clients...')

    s.bind((host, port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.
    
    while True:
        c, addr = s.accept()     # Establish connection with client.
        print('Got connection from', addr)
        
        x = threading.Thread(target=server_program, args=(c, addr))
        x.start()
        # s.close()




def server_program(conn, address):
    print("here")
    # # get the hostname
    # host = socket.gethostname()
    # port = 5067  # initiate port no above 1024

    # server_socket = socket.socket()  # get instance
    # # look closely. The bind() function takes tuple as argument
    # server_socket.bind((host, port))  # bind host address and port together

    # # configure how many client the server can listen simultaneously
    
    # server_socket.listen(2)
    # conn, address = server_socket.accept()  # accept new connection

    string = input(' input the string: ')
    length = len(string)
    print("Length of the string you just input is = " + str(length))
    if length % 4 != 0 and length < 12:
        print("your input format is wrong.")
    else:
        # split into 4 character data
        segment_size = 4
        print(segment_size)
        segmented_data = [string[i:i+segment_size] for i in range(0, length, segment_size)]

        for i in range(0,segment_size + 1):
            print(segmented_data[i])

        print("Connection from: " + str(address))
        while True:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = conn.recv(1024).decode()
            if not data:
                break
            print("user wants me to send the " + str(data) + " segment.")
            conn.send(segmented_data[int(data)].encode())  # send data to the client

        conn.close()  # close the connection

        


if __name__ == '__main__':
    server_socket()

