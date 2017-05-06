
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

