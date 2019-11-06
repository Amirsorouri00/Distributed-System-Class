import socket
import threading
import hashlib


def client_socket():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000 # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    print("Connection Created.")
    return client_socket
    

def handshake(conn):
    print("Handshake starting ...")
    intent  = "handshake"
    
    conn.send(intent.encode())  # send message
    data = conn.recv(1024).decode()  # receive response

    print("Size of the file@server is = " + str(data))
    return int(data)


def download_chunk(conn, conn_num, chunk_size, chunks, index):

    buffer = 1024
    received = 0
    chunk = []
    try:
        while received < chunk_size:
            data = conn.recv(min(chunk_size - received, buffer))
            received += len(data)
            print(data)
            print(received)
            chunk.append(data)
        file_chunk = b''.join(chunk)
        chunks[index] = file_chunk
        print(file_chunk)
        print('Received file')
        print('Expected size:', chunk_size)
        print('Received size:', len(file_chunk))
    
    except Exception as e:
        print("3-An exception occurred. " + str(e))


def download_file(conn_num, file_size):
    chunk_size = int(file_size)/int(conn_num)
    last_chunk_size = file_size - ((conn_num - 1) * int(chunk_size))
    print("last chunk size: " + str(last_chunk_size))
    threads = []
    chunks = []
    connections = []
    for i in range(0, conn_num): 
        chunks.append(0) 

    for i in range(0, conn_num):  
        conn = client_socket()
        connections.append(conn)
        x = 0
        data = str(i) + ":" + str(0 + i*int(chunk_size))
        conn.send(data.encode())

        if i == conn_num - 1:
            x = threading.Thread(target=download_chunk, args=(conn, conn_num, last_chunk_size, chunks, i))            
        else:
            x = threading.Thread(target=download_chunk, args=(conn, conn_num, int(chunk_size), chunks, i))
        
        threads.append(x)
        x.start()
    
    for i in range(0, conn_num):  
        threads[i].join()
        connections[i].close()


    conn = client_socket()    
    conn.send("hash".encode())
    print(chunks)

    received = 0
    otherchunks = []
    while received < 64:
        data = conn.recv(64 - received)
        received += len(data)
        otherchunks.append(data)
    sha512 = b''.join(otherchunks)
    print('Received Hash', len(sha512), sha512)
    conn.close()
    
    file = b''.join(chunks)
    hash_ok = hashlib.sha512(file).digest() == sha512
    print('Hash is ok') if hash_ok else print('Hash is not ok')

    return file


if __name__ == '__main__':

    path = input(' Input path of the file i have to save the downloaded file: ')
    try:
        conn = client_socket()

        filesize = handshake(conn)
        conn_num = input( " Input the Number of concurrent connection: ")
        conn.close()

        file = download_file(int(conn_num), int(filesize))
        print(file)
        with open(path, 'wb') as fd:
            fd.write(file)
            fd.close()

    except Exception as e:
        print("1-An exception occurred. " + str(e)) 



















# def client_program():

    

#     string_size = input(" please input the segment number of the input string: ")  # take input
#     segment_size = int(string_size)/4
#     counter = 0
#     arr = []
#     wholedata = []
#     for i in range(0, int(segment_size)):
#         arr.append(0)
#         wholedata.append(0)

#     while check(arr, segment_size) == -1:
#         segment_num = input(" input segment number you want me to get ")  # take input

#         client_socket.send(segment_num.encode())  # send message
#         data = client_socket.recv(1024).decode()  # receive response
        
#         print('Received from server: ' + data)  # show in terminal
#         wholedata[int(segment_num)] = data
#         arr[int(segment_num)] = 1
#         # message = input(" -> ")  # again take input

#     client_socket.close()  # close the connection

#     h = ""
#     for i in range(0, int(segment_size)):
#         h = h + wholedata[i]
#         h = h + " "
#     print(h)
