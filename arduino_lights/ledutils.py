import serial

def serial_port():
  ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200
  )

  # So! Apparently when you connect to the arduino serial port, the bootloader
  # kicks in, resets the arduino and waits a second for a new program to be loaded
  # before running the actual already stored code 
  time.sleep(2)

  return ser

def set_pixel(ser, x, y, red, green, blue):
  red   = min(red, 253)
  green = min(green, 253)
  blue  = min(blue, 253)
  pixel = xy_to_pixel(x, y)
  control_string = bytearray([pixel,red,green,blue, 255])
  ser.write(control_string)

def end_frame(ser):
  control_string = bytearray([254])
  ser.write(control_string)

def xy_to_pixel(x,y):
  row_offset = y * 12
  if y % 2 == 0:
    column_offset = (11 - x)
  else:
    column_offset = x
  return row_offset + column_offset

