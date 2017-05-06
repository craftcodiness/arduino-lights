require 'serialport'

module ArduinoLights
  SERIAL_PORT = "/dev/ttyUSB0"
  SERIAL_RATE = 115200
  PIXELS = 24

  def self.serial_port
    @port ||= begin
      res = SerialPort.new(SERIAL_PORT, SERIAL_RATE, 8, 1, SerialPort::NONE)
      sleep(2)
      res
    end
  end

  def self.set_pixel(pixel, red, green, blue)
    # Something about the setup with these LEDs requires a small delay between bytes sent
    # I don't know if this is about the configuration of ruby-serialport, or the pixel 
    # processing code on the Arduino itself.
    #
    # With this set to 0.0009, data runs through the device at about 5kb/s. With this set
    # to 0.0008, the data runs through at >5.5kb/s, which causes some of the data to be lost
    sleep(0.0009)

    # first byte is whice led number to switch on
    self.serial_port.write(pixel.chr)     

    # next 3 bytes are red, green and blue values
    # Note: 255 signifies the end of the command, so don't try and set an led value to that
    self.serial_port.write(red.chr)    
    self.serial_port.write(green.chr)    
    self.serial_port.write(blue.chr)

    # then end with a termination character
    self.serial_port.write(255.chr)  
  end

  def self.radial_pixel_index(value, range)
    (((PIXELS.to_f * value) / range).floor + PIXELS) % PIXELS
  end

  def self.draw_pixel_map(pixels)
    pixels.each_with_index do |pixel,i|
      set_pixel(PIXELS - i - 1, pixel[0], pixel[1], pixel[2])
    end
  end

end

if __FILE__ == $0
  pixel = 0
  while (true)
    pixels = (0..(ArduinoLights::PIXELS-1)).map { [0,0,0] }
    pixels[pixel] = [100,50,50]
    ArduinoLights::draw_pixel_map(pixels)
    pixel = (pixel + 1) % ArduinoLights::PIXELS
  end
end
