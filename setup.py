from distutils.core import setup
setup(
  name = 'arduino_lights',
  packages = ['arduino_lights'], # this must be the same as the name above
  version = '0.1',
  description = 'Control LED lights via Arduino',
  author = 'Arthur Taylor',
  author_email = 'arthur.taylor@gmail.com',
  url = 'https://github.com/craftcodiness/arduino-lights', # use the URL to the github repo
  download_url = 'https://github.com/craftcodiness/arduino-lights/archive/0.1.tar.gz', # I'll explain this in a second
  keywords = ['led', 'serial', 'arduino'],
  classifiers = [],
)
