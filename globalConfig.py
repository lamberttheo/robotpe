# Bottle.py global variable
webserverPort = 8080
lastHTTPrequest = 0

# Email informations
mailFrom = "anymail@yourhost.tld"
mailTo = "yourmail@yourhost.tld"
mailUsername = "yourmail@yourhost.tld"
mailPassword = "your_strong_password"
mailStartTLS = True # True or None
mailSMTPserver = "smtp.provider.tld"
mailSMTPport = "587"

# Arduino conf
maxServoAngle = 120 # /255

# Javascript related
maxJoystickValue = 100   # Same value as in views/gamepad.tpl
leftJoystickX = 0       # Unused
leftJoystickY = 0       # Used for acceleration
rightJoystickX = 0      # Used for direction
rightJoystickY = 0      # Used to change the webcam angle
