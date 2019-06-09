#Converting to Python 3

import serial
port = serial.Serial('/dev/ttyACM0',9600)
#print(ser.name) #check which port was actually used
#polling

input_received = port.read(200) #read 20 bytes

print input_received

port.flush()
port.flushInput()
port.flushOutput()
port.close()
