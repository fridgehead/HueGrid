import serial,sys,math
from PIL import Image

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
 


def sample_image(filename,ser):
  im = Image.open(filename)
  #print(im.format, im.size, im.mode)

  rgb_buffer = []

  exact = True
  if im.size[0] != im.size[1] != 30:
    exact = False

  for row in range(0, 30):
    for column in range (0,30):
    
      x = column
      y = row
      
      if not exact:
        x *= (math.floor(im.size[0]/ 31))
        y *= (math.floor(im.size[1] / 31))

      # sample around the centroid
      rgb = [0,0,0]
      if exact:
        rgb = im.getpixel((x,y))

      else:
        ss = 5
    
        total = ss * 2
        total = total * total
        for xs in range(0,ss * 2):
          for ys in range (0, ss* 2):
            xsr = -ss + xs
            ysr = -ss + ys
            trgb = im.getpixel((x + xsr,y + ysr))
            rgb[0] += trgb[0]
            rgb[1] += trgb[1]
            rgb[2] += trgb[2]

        rgb[0] /= total
        rgb[1] /= total
        rgb[2] /= total
    
      brg = (int(rgb[2]),int(rgb[0]),int(rgb[1]))
     
      rgb_buffer.append(int(rgb[2]))
      rgb_buffer.append(int(rgb[0]))
      rgb_buffer.append(int(rgb[1]))

  
  set_image(rgb_buffer,ser)


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

  #clear_screen()
  if sys.argv[1] == "clear":
    clear_screen(ser)
  elif sys.argv[1] == "seq":
    for i in range(2,len(sys.argv)):
      sample_image(sys.argv[i],ser)
  else:
    sample_image(sys.argv[1],ser)
  #image_test()
  #test_func()
  ser.close() 
