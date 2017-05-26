import serial
import time
import os
from collections import namedtuple
from stat import S_ISCHR, S_ISFIFO, S_ISREG

Size = namedtuple('Size', 'w h')
LED_SIZE = Size(12, 12)
LED_COUNT = LED_SIZE.w * LED_SIZE.h
BAUD_RATE = 115200


#The WS2801 has a nonlinear brightness curve, so we need to compensate
# to get a proper colour mapping.
# @todo - this gamma correction should really be run on the Arduino.
gammaCorrection = [
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
    1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
    2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
    5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
   10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
   17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
   25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
   37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
   51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
   69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
   90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
  115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
  144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
  177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
  215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255 ]


def connect(file="/dev/ttyUSB0"):
    file = os.getenv("BLEMU_DEVICE", file)
    if not os.path.exists(file):
        raise ValueError("Device `%s` does not exist. Cannot connect" % file)

    mode = os.stat(file).st_mode
    ser = None
    if S_ISCHR(mode):
        ser = serial.Serial(port=file, baudrate=BAUD_RATE)
    elif S_ISFIFO(mode) or S_ISREG(mode):
        ser = open(file, "w")

    # So! Apparently when you connect to the arduino serial port, the
    # bootloader kicks in, resets the arduino and waits a second for a new
    # program to be loaded before running the actual already stored code
    time.sleep(2)
    return ser


def set_pixel(ser, coord, red, green, blue):
    '''Set the pixel addressed by coord to the given color triplet.
    If coord is a tuple, it will be interpreted as x, y coordinates.
    If it is an integer it's interpreted as a linear pixel address.
    '''
    red = min(red, 254)
    green = min(green, 254)
    blue = min(blue, 254)
    pixel = xy_to_pixel(*coord) if isinstance(coord, tuple) else coord
    if pixel > 254:
        raise ValueError('Pixel number out of range')
    control_string = bytearray([pixel, gammaCorrection[red], gammaCorrection[green], gammaCorrection[blue], 255])
    #control_string = bytearray([pixel, red, green, blue, 255])
    ser.write(control_string)
    ser.flush()


def end_frame(ser):
    control_string = bytearray([254])
    ser.write(control_string)


def draw_pixel_map(ser, pixels, autoend=True):
    '''Utility to draw a dict of (x,y) tuples to (r,g,b) tuples.
    If autoend is true, calls end_frame before returning.'''
    for i in xrange(LED_SIZE.w):
        for j in xrange(LED_SIZE.h):
            set_pixel(ser, (i, j), *pixels[i, j])
    if autoend:
        end_frame(ser)


def clear(ser, red=0, green=0, blue=0, autoend=True):
    '''Utility to clear the screen/fill it with one color'''
    for i in xrange(LED_SIZE.w):
        for j in xrange(LED_SIZE.h):
            set_pixel(ser, (i, j), red, green, blue)
    if autoend:
        end_frame(ser)


def xy_to_pixel(x, y):
    row_offset = y * LED_SIZE.w
    if y % 2 == 0:
        column_offset = LED_SIZE.w - 1 - x
    else:
        column_offset = x
    return row_offset + column_offset


def pixel_to_xy(pixel):
    x = pixel % LED_SIZE.w
    y = pixel / LED_SIZE.w
    if y % 2 == 0:
        # flip every second row, because hardware!
        x = LED_SIZE.w - 1 - x
    return x, y
