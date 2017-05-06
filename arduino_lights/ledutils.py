import serial, time, os, sys
from stat import *

def serial_port(file="/dev/ttyUSB0"):
  if not os.path.exists(file):
    print "File " + file + " does not exist. Cannot open serial port"
    sys.exit(1)

  mode = os.stat(file).st_mode
  ser = None
  if S_ISCHR(mode):
    ser = serial.Serial(
      port=file,
      baudrate=115200
    )
  elif S_ISFIFO(mode):
    ser = open(file, "w")

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
  ser.flush()

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

