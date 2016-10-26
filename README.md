# robotpe
Travaux Personel Encadré

Arduino installation

    Download and unzip Arduino 1.5+
    Unzip dependencies/nanpy-firmware-master.zip
    Launch dependencies/nanpy-firmware-master/configure.sh
    Copy dependencies/nanpy-firmware-master/Nanpy into dependencies/arduino-1.5.7/examples
    Launch dependencies/arduino-1.5.7/arduino
    Go in Files/Examples/Nanpy and download it to your board (if necessary, set your model in the Tools menu)

Setup the embedded computer

    Launch as root:

    apt-get install python-setuptools python-bottle python-opencv python-redis redis-server

    Unzip dependencies/nanpy-master.zip

    Launch as root:

    python dependencies/nanpy-master/setup.py install


The script will send you a mail at the address written in the globalConfig.py file, containing a link to control the robot.
