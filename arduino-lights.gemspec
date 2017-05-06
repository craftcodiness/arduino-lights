Gem::Specification.new do |s|
  s.name        = 'arduino-lights'
  s.version     = '0.6.0'
  s.date        = '2017-04-09'
  s.summary     = "LED control for ruby via arduino"
  s.description = "Simple gem to wrap the serial port control for ruby projects controlling an Arduino with LEDs attached"
  s.authors     = ["Arthur Taylor"]
  s.email       = 'arthur.taylor@gmail.com'
  s.files       = ["lib/arduino-lights.rb"]
  s.add_runtime_dependency "serialport", ["= 1.3.1"]
  s.homepage    =
    'http://github.com/codders/arduino-lights'
  s.license       = 'MIT'
end
