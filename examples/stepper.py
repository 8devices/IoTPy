# Stepper motor example
# Uros Petrevski, 2014

from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.things.stepper import HALF_STEP, FULL_STEP, Stepper
from IoTPy.pyuper.utils import IoTPy_APIError, die

try:
    u = IoBoard()
except IoTPy_APIError, e: # seems can't establish connection with the UPER board
    details = e.args[0]
    die(details)

# parameters : uper obj, how many steps in 360, first coil pins, second coil pins
motor = Stepper(u,200,11,14,12,13)

print "Motor is in full step mode by default"
motor.step(200)

print "Put motor in half step mode"
motor.setStepperMode(HALF_STEP)
motor.step(-100)

print "Going back to full step mode"
motor.setStepperMode(FULL_STEP)

speed = 40 # Rotations per minute
print "setting speed to %s rotations per minute" %speed
motor.setSpeed(speed)
motor.step(200)