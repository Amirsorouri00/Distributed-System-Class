
#!/usr/bin/python           # This is server.py file                                                                                                                                                                           
import os
import io
import socket               # Import socket module
import threading
import hashlib


def server_socket(path, filesize):
    print('Server started!')

    s = socket.socket()             # Create a socket object
    host = socket.gethostname()     # Get local machine name
    port = 5000                     # Reserve a port for your service.

    print('Waiting for clients...')
    try:
        s.bind((host, port))            # Bind to the port
        s.listen(5)                     # Now wait for client connection.
    except Exception as e:
        print("2-An exception occurred. " + str(e)) 
        return
    
    while True:
        conn, addr = s.accept()        # Establish connection with client.
        print('Got connection from', addr)
        
        x = threading.Thread(target=server_program, args=(conn, addr, path, filesize))
        x.start()


def server_program(conn, address, path, filesize):
    print("Server_Program Starting ...")

    print("Server_Program Waiting for a data from the client ...")

    data = conn.recv(1024).decode()
    data = str(data)

    if "handshake" == data:
        conn_type = "Client wants to handshake and know size of file."
        handshake(conn, address, path, filesize)
        print("handshake Done.")
    elif "download" == data:
        conn_type = "Client wants to download a chunk of file."
    elif "hash" == data:
        conn_type = "Client wants to close the connection."
        buffsize = 1024
        with open(path, 'rb') as fd:
            fd.seek(0)
            hash = hashlib.sha512()
            while True:
                chunk = fd.read(buffsize)
                if not chunk:
                    break
                hash.update(chunk)
            conn.send(hash.digest())
    else:
        conn_type = "data_chunk "
        info = data.split(":")
        if(len(info) > 1):
            sendfile(conn, address, path, filesize, info)

        
def handshake(conn, address, path, filesize):
    conn.send(str(filesize).encode())  # send data to the client
    return

def sendfile(conn, address, path, filesize, info):
    print("------- inside sendfile -----------")
    buffsize = 1024
    file = path
    print("filesize:" + str(filesize))
    print("info: ")
    print(info)
    
    with open(file, 'rb') as fd:
        fd.seek(int(info[1]))
        while True:
            try:
                chunk = fd.read(buffsize)
                if not chunk:
                    break
                conn.send(chunk)
            except Exception as e:
                print("3-" + str(e)) 
                break
            
    conn.close()
    

if __name__ == '__main__':

    path = input(' Input path of the file i have to server: ')
    try:
        filesize = os.path.getsize(path)
        print("size of the file is = " + str(filesize))
        
        server_socket(path, filesize)
    except Exception as e:
        print("1-An exception occurred. " + str(e)) 

