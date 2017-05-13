import serial
import time
import os
import sys
from collections import namedtuple
from stat import S_ISCHR, S_ISFIFO

Size = namedtuple('Size', 'w h')
LED_SIZE = Size(12, 12)
LED_COUNT = LED_SIZE.w * LED_SIZE.h
BAUD_RATE = 115200

def connect(file="/dev/ttyUSB0"):
    file = os.getenv("BLEMU_DEVICE", file)
    if not os.path.exists(file):
        raise ValueError("Device `%s` does not exist. Cannot connect" % file)

    mode = os.stat(file).st_mode
    ser = None
    if S_ISCHR(mode):
        ser = serial.Serial(port=file, baudrate=BAUD_RATE)
    elif S_ISFIFO(mode):
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
    red = min(red, 253)
    green = min(green, 253)
    blue = min(blue, 253)
    pixel = xy_to_pixel(*coord) if isinstance(coord, tuple) else coord
    if pixel > 253:
        raise ValueError('Pixel number out of range')
    control_string = bytearray([pixel, red, green, blue, 255])
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
