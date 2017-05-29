#!/usr/bin/env python
'''Utility to test the raw performance of the arduino-lights system'''
import argparse
import time
from itertools import product

import arduino_lights as al
from arduino_lights import LED_SIZE

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--per-pixel', action='store_true')
    parser.add_argument('--delay', type=float, default=0.0)
    args = parser.parse_args()

    blinken = al.connect()
    frames = 0
    last = time.time()

    def print_fps():
        global last
        if frames % 60 == 0:
            now = time.time()
            print "Frames %d, FPS: %.2f" % (frames, 60 / (now - last))
            last = now

    while True:
        for xy in product(xrange(LED_SIZE.w), xrange(LED_SIZE.h)):
            color = (frames % 256,
                     frames % 256,
                     frames % 256)
            al.set_pixel(blinken, xy, *color)
            if args.per_pixel:
                al.end_frame(blinken)
                frames += 1
                if args.delay:
                    time.sleep(args.delay)
                print_fps()

        if not args.per_pixel:
            al.end_frame(blinken)
            frames += 1
            if args.delay:
                time.sleep(args.delay)
            print_fps()
