import argparse
import controller
from controller import LED_SIZE, LED_COUNT


def colorize(val, max_val):
    return int(1.0 * val / max_val * 255)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test that blinkenbox maan!')
    parser.add_argument('dev', help='The device to send commands to')
    args = parser.parse_args()

    with controller.connect(args.dev) as con:
        for x in range(LED_SIZE.w):
            for y in range(LED_SIZE.h):
                controller.set_pixel(con, (x, y),
                                     colorize(x, LED_SIZE.h),
                                     colorize(y, LED_SIZE.w),
                                     colorize(x * y, LED_COUNT))
        controller.end_frame(con)
