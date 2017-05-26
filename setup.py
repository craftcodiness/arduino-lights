from distutils.core import setup
setup(
    name = 'arduino_lights',
    packages = ['arduino_lights'],
    version = '0.7.4',
    description = 'Control LED lights via Arduino',
    author = 'Arthur Taylor',
    author_email = 'arthur.taylor@gmail.com',
    url = 'https://github.com/craftcodiness/arduino-lights',
    download_url = 'https://github.com/craftcodiness/arduino-lights/archive/0.7.4.tar.gz',
    keywords = ['led', 'serial', 'arduino'],
    classifiers = [],
    install_requires=[
        'pyserial'
    ]
)
