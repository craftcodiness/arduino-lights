from distutils.core import setup
setup(
  name = 'arduino_lights',
  packages = ['arduino_lights'], # this must be the same as the name above
  version = '0.2',
  description = 'Control LED lights via Arduino',
  author = 'Arthur Taylor',
  author_email = 'arthur.taylor@gmail.com',
  url = 'https://github.com/craftcodiness/arduino-lights', # use the URL to the github repo
  download_url = 'https://github.com/craftcodiness/arduino-lights/archive/0.2.tar.gz', # I'll explain this in a second
  keywords = ['led', 'serial', 'arduino'],
  classifiers = [],
)
