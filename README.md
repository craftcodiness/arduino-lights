# Arduino Lights

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

> Tiny polyglot (Ruby/Python) wrapper on serial-port to control ws2801/ws2812 LED lights via Arduino

This polyglot (Ruby/Python) library opens a serial port to communicate with an Arduino, allowing programs to send messages to a receiving process on the Arduino that controls ws2801- and ws2812-chipset LED strips. The Arduino must have been programmed with [@edwardmccaughan's](https://github.com/edwardmccaughan) [rgb_led_control](https://github.com/edwardmccaughan/rgb_led_control) firmware.

Today, this supports two devices - the LED ring, and the LED matrix. Both have similar APIs, but the LED matrix requires an explicit `draw_screen` command to be sent after the pixel data has been updated before anything will be rendered.

## Table of Contents

 - [Background](#background)
 - [Install](#install)
   - [Ruby Install](#ruby-install)
   - [Python Install](#python-install)
 - [Usage](#usage)
 - [API](#api)
   - [serial_port](#serial_portportdevttyUSB0)
   - [set_pixel](#set_pixelpixel-red-green-blue)
   - [draw_pixel_map](#draw_pixel_mappixels)
   - [end_frame](#end_frame)
 - [Simulator](#simulator)
 - [Maintainer](#maintainer)
 - [Contribute](#contribute)
 - [License](#license)

## Background

[Ed](https://github.com/edwardmccaughan) is a master of all things crafty. He builds strange and wonderful contraptions with his bare hands, then shares the contraptions with his friends so that they can create their own artistic wonders. This library is to support the development of crafty LED-driving code in Ruby and Python.

## Install

### Ruby Install

To install this library in Ruby, add this gem to your Gemfile:

```
source "https://rubygems.org"

gem "arduino-lights"
```

If you are modifying this Gem, update the version information in `arduino-lights.gemspec` and build a new version using `gem`:

```
gem build arduino-lights.gemspec
gem push arduino-lights-<VERSION>.gem
```

N.B. You will need an appropriate rubygems API key to be able to push the package.

### Python Install

To install this library in Python, fetch it from PyPI:

```
pip install arduino_lights
```

If you are modifying the library, update the version information and download URL in `setup.py` and push a new version with `setup.py`:

```
python setup.py sdist upload -r arduino_lights
git tag <VERSION> -m "Your comment"
git push --tags origin master

```

N.B. You will need appropriate entries in your `~/.pypirc`, including a valid username and password, to be able to push the package.

## Usage

### Usage Ruby

From your ruby script, simply import `arduino-lights`. You can then write simple code to drive the LEDs. For example, for the LED ring:

```
require 'arduino-lights'

pixel = 0
while (true)
  pixels = (0..(ArduinoLights::PIXELS-1)).map { [0,0,0] }
  pixels[pixel] = [100,50,50]
  ArduinoLights::draw_pixel_map(pixels)
  pixel = (pixel + 1) % ArduinoLights::PIXELS
end

```

Note that the LED ring does not explicitly require `ArduinoLights::draw_screen` to be called to render the pixles, but the LED matrix will do before any changes can be seen. 

### Usage Python

From your python script, simply import `ledutils` from the `arduino_lights` package:

```
import time
from arduino_lights import ledutils

ser = ledutils.serial_port()

x = 0
y = 0
first = True
while(True):
  if not first:
    ledutils.set_pixel(ser, x, y, 0, 0, 0)
  first = False
  x = (x + 1) % 12
  if x == 0:
    y = (y + 1) % 12
  ledutils.set_pixel(ser, x, y, 0, 255, 0)
  ledutils.end_frame(ser)
  time.sleep(0.05)

```

## API

The APIs for Ruby and Python are similar. Note that for the Python library, the API calls' first argument must be a reference to the target serial port (the Ruby library maintains a singleton reference to the opened port).

The Ruby library will automatically open the serial port when the first pixel data needs to be sent. For the Python library, the serial port must be opened explicitly and a reference to the port retained for future API calls.

### serial_port(port = '/dev/ttyUSB0')

This function will open and return the serial port. By default, the serial port is expected to be at `/dev/ttyUSB0`. The port will be configured for 115200 baud (8N1). You can change the target port by passing the path as the argument to this function. For the Ruby library, it is not always necessary to call this function directly - it will implicitly be called by the pixel drawing routines with default values.

For testing purposes, you can pass a path to a named pipe as the port address. In this case, bytes will be written to the pipe, and no attempt will be made to configure baud rate etc.

### set_pixel(pixel, red, green, blue)

This will set the pixel with index `pixel` to the colour `#RRGGBB` where `red`, `green` and `blue` are numbers in the range 0 to 253 (values 254 and 255 are reserved as control codes - best avoid them).

### draw_pixel_map(pixels)

This function takes an array of `[red, green, blue]` values - one for each pixel - and renders them to the device.

### end_frame()

This function sends the control code to render the current buffer to the screen for the WS2801-type displays

## Simulator

If you want to develop programs using this library, but without the hardware available, you can check out the [blinky-sim](https://github.com/craftcodiness/blinky-sim). The instructions there explain how to render your output to a local named pipe rather than a serial port for testing purposes.

## Maintainer

This library is maintained by [@codders](https://github.com/codders).

## Contribute

Pull requests are more than welcome! We have very low standards.

## License

This code is licensed under the [GNU GPLv3](https://www.gnu.org/licenses/gpl.txt), a [copy of which](LICENSE) is included in this repository.

Copyright Arthur Taylor and Edward McCaughan, 2017
