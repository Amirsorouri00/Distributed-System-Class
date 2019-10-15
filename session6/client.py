import socket


def check(arr, size):
    print("here")
    for i in range(0, int(size)):
        if arr[i] == 0:
            print("ooo")
            return -1
    print("heyyy")
    return 1


def client_program():

    host = socket.gethostname()  # as both code is running on same pc
    port = 5069 # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    string_size = input(" please input the segment number of the input string: ")  # take input
    segment_size = int(string_size)/4
    counter = 0
    arr = []
    wholedata = []
    for i in range(0, int(segment_size)):
        arr.append(0)
        wholedata.append(0)

    while check(arr, segment_size) == -1:
        segment_num = input(" input segment number you want me to get ")  # take input

        client_socket.send(segment_num.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response
        
        print('Received from server: ' + data)  # show in terminal
        wholedata[int(segment_num)] = data
        arr[int(segment_num)] = 1
        # message = input(" -> ")  # again take input

    client_socket.close()  # close the connection

    h = ""
    for i in range(0, int(segment_size)):
        h = h + wholedata[i]
        h = h + " "
    print(h)

if __name__ == '__main__':
    client_program()

