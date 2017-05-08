'''
An emulator for the blinkenbox, so that developing cool, tasty
effects doesn't need the hardware.

Because Windows is a biatch when it comes to anything terminal related,
this will only work on Unix-y systems.
'''
import os
import pty
import logging
import argparse
import pygame
from pygame import Rect, Color

from controller import Size, LED_SIZE, pixel_to_xy


SCREEN_SIZE = Size(600, 600)
PIXEL_SIZE = Size(SCREEN_SIZE.w / LED_SIZE.w,
                  SCREEN_SIZE.h / LED_SIZE.h)
screen = None


def setup_screen():
    global screen
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Blinkenbox Emulator')


def draw_pixel(pixel, color):
    x, y = pixel_to_xy(pixel)
    rect = Rect((x * PIXEL_SIZE.w, y * PIXEL_SIZE.h), PIXEL_SIZE)
    screen.fill(color, rect)


def show():
    pygame.display.flip()


def process_command(frame):
    if len(frame) != 4:
        logging.error('Broken frame! Wrong length: %d', len(frame))
    pixel, red, green, blue = frame
    logging.debug('Set pixel %d to (%d, %d, %d)', pixel, red, green, blue)
    draw_pixel(pixel, Color(red, green, blue))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A Blinkenbox emulator!')
    parser.add_argument('--debug', action='store_true', help='Debug logging')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    setup_screen()
    master, slave = pty.openpty()
    logging.info('Listening for commands at %s', os.ttyname(slave))
    frame = bytearray()
    while True:
        byte = os.read(master, 1)
        if byte == '\xff':
            process_command(frame)
            frame = bytearray()
        elif byte == '\xfe':
            show()
        else:
            frame.append(byte)
