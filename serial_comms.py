"""
serial_comms.py 

Basic serial comms for the EMF LEDs project.
Adapted for working with RI HueGrid

author : Benjamin Blundell
email : oni@section9.co.uk

"""

import serial,sys,math

def connect():

  ser = serial.Serial('/dev/ttyACM0', 9600)
  print(ser.name)
  if not ser.isOpen():
    print("Failed to open serial port")
    sys.exit()
  
  return ser

def response(ser):
  response = ser.read()
  #print(response)

  if response == b'\x99':
    #print("Command Success")
    return
  elif response == b'\x98':
    print("Command Failed")
    ser.write(b'\x42')
  elif response == b'\x97':
    print("Incorrect Command")
    ser.write(b'\x42')
  elif response == b'\x96':
    print("Malformed command")
    ser.write(b'\x42')
  elif response == b'\x95':
    print("Incorrect pre-amble")
    ser.write(b'\x42')
  else:
    print("Failed response") 


def set_image(rgb_buffer,ser):
  
  bpos = 0;
  for i in range(45): 
 
    image_buffer=[]
    image_buffer.append(0x99)
    image_buffer.append(0x69)

    for i in range(60):
      image_buffer.append(rgb_buffer[bpos])
      bpos+=1
  
    image_buffer.append(0x96)

    ser.write(bytes(image_buffer))
    response(ser)
 

def clear_screen(ser):

  ser.write(b'\x99'b'\x70'b'\x96')
  response(ser)

def test_func(ser):
  ser.write(b'\x99'b'\x71'b'\x96')
  response(ser)


# we batch the image calls in buffer sizes of 60 as the serial
# buffer is quite small! :D

def image_test():

  tval = 0
  for i in range(45): 

    image_buffer=[]
    image_buffer.append(0x99)
    image_buffer.append(0x69)
  
    for i in range(60):
      image_buffer.append(int(tval))

    tval+=4
  
    image_buffer.append(0x96)

    ser.write(bytes(image_buffer))
    response(ser)

if __name__ == "__main__":

  ser = connect()
  image_test()
  test_func(ser)
  ser.close() 
