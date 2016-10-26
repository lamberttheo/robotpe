from nanpy import (ArduinoApi, SerialManager, Servo)
import time, threading
import globalConfig

# Initiates the Arduino link
serialConnection = SerialManager()
arduino = None
try:
  arduino = ArduinoApi(connection=serialConnection)
  print("Arduino link correctly established")
except:
  print("Arduino link unreachable")

# The 13 LED is embedded on most of Arduino boards
def toggleLED():
  if arduino is not None:
    arduino.pinMode(13, arduino.OUTPUT)
    arduino.digitalWrite(13, 1)
    time.sleep(5)
    arduino.digitalWrite(13, 0)

def moveRobot():
  if arduino is not None:
    # Sets pin definition constants
    M1_pin_direction = 4  # Left motor, forward/backward
    M2_pin_direction = 7  # Right motor, forward/backward
    M1_pin_speed = 5
    M2_pin_speed = 6
    SERVO_pin = 16

    # Sets pins initialization
    arduino.pinMode(M1_pin_direction, arduino.OUTPUT)
    arduino.pinMode(M2_pin_direction, arduino.OUTPUT)
    arduino.pinMode(M1_pin_speed, arduino.OUTPUT)
    arduino.pinMode(M2_pin_speed, arduino.OUTPUT)
    # servo = Servo(SERVO_pin)

    # Sets default values
    motor1_direction = motor2_direction = arduino.HIGH
    motor1_speed = motor2_speed = 0
    servo_angle = 100

    while True:
      # Security in case of connection lost by the client, once every 1s
      # These variables are not thread-locked because it's a fallback state
      if time.time() - globalConfig.lastHTTPrequest > 1:
        globalConfig.leftJoystickX = 0
        globalConfig.leftJoystickY = 0
        globalConfig.rightJoystickX = 0
        globalConfig.rightJoystickY = 0


      # Motors in opposite direction at same speed, only if left joystick is not used
      if globalConfig.leftJoystickY == 0:
        # Generates a larger joystick dead point, to not be too fast
        if globalConfig.rightJoystickY > 10:
          motor1_direction = arduino.LOW
          motor2_direction = arduino.HIGH
          motor1_speed = motor2_speed = globalConfig.rightJoystickY * 255 / globalConfig.maxJoystickValue
        elif globalConfig.rightJoystickY < 10:
          motor1_direction = arduino.HIGH
          motor2_direction = arduino.LOW
          motor1_speed = motor2_speed = globalConfig.rightJoystickY * 255 / globalConfig.maxJoystickValue
        else:
          motor1_speed = motor2_speed = 0
      # Motors operating in the same direction, at same speed if right joystick is not used
      else:
        # Forward acceleration
        if globalConfig.leftJoystickY > 0:
          motor1_direction = arduino.HIGH
          motor2_direction = arduino.HIGH
        # Backward acceleration
        elif globalConfig.leftJoystickY < 0:
          motor1_direction = arduino.LOW
          motor2_direction = arduino.LOW

        # Turns left
        if globalConfig.rightJoystickX < 0:
          # Joystick values are negative in this case. Will decrease the power of the left motor.
          motor1_speed = (globalConfig.rightJoystickX + globalConfig.maxJoystickValue) * 255 / globalConfig.maxJoystickValue
          # Right motor has the acceleration power's value
          motor2_speed = globalConfig.leftJoystickY * 255 / globalConfig.maxJoystickValue
        # Turns right
        elif globalConfig.rightJoystickX > 0:
          # Left motor has the acceleration power's value
          motor1_speed = globalConfig.leftJoystickY * 255 / globalConfig.maxJoystickValue
          # Right motor has the direction power's value
          motor2_speed = globalConfig.rightJoystickX * 255 / globalConfig.maxJoystickValue
        # Doesn't turn! Just go!
        else:
          motor1_speed = motor2_speed = globalConfig.leftJoystickY * 255 / globalConfig.maxJoystickValue


      # Generates an artificial dead point for security
      # and a continuous movement for servo preservation
      # Turns left
      if globalConfig.leftJoystickX > 30 and servo_angle < 255:
        servo_angle += 5
      # Turns right
      elif globalConfig.leftJoystickX < -30 and servo_angle > 10:
        servo_angle -= 5


      # Executor for engines part
      arduino.digitalWrite(M1_pin_direction, motor1_direction)
      arduino.digitalWrite(M2_pin_direction, motor2_direction)
      arduino.analogWrite(M1_pin_speed, motor1_speed)
      arduino.analogWrite(M2_pin_speed, motor2_speed)

      # Executor for servo part
      # servo.write(servo_angle)


      # Slows down the refresh of values, once every 100ms
      time.sleep(0.05)


# Turns on the LED on start without blocking the program
ledThread = threading.Thread(None, toggleLED)
ledThread.start()
ledThread._Thread__stop()

# Monitors variables and applies changes on the robot
pilotThread = threading.Thread(None, moveRobot)
pilotThread.start()
pilotThread._Thread__stop()
