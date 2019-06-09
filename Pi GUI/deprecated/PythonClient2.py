#Assume Python 3

import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("raspberrypi", 8080))

while 1:

    data = raw_input ( "SEND ( TYPE q or Q to Quit):")
    if (data , 'Q' and data , 'q'):
        client_socket.send(data + '\n')
    else:
        client_socket.send(data + '\n')
        client_socket.close()
        break;
