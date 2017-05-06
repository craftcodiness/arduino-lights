import argparse
import ledutils
from ledutils import LED_SIZE, LED_COUNT


def colorize(val, max_val):
    return int(1.0 * val / max_val * 255)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test that blinkenbox maan!')
    parser.add_argument('port', help='The port to send commands to')
    args = parser.parse_args()

    with ledutils.serial_port(args.port) as ser:
        for x in range(LED_SIZE.w):
            for y in range(LED_SIZE.h):
                ledutils.set_pixel(ser, x, y,
                                   colorize(x, LED_SIZE.h),
                                   colorize(y, LED_SIZE.w),
                                   colorize(x * y, LED_COUNT))
        ledutils.end_frame(ser)
