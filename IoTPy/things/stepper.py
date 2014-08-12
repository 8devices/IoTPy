# Stepper motor driver
# Uros Petrevski, 2014
# Implemented both full step and half-step control
from IoTPy.core.gpio import GPIO
from time import sleep

FULL_STEP = 0
HALF_STEP = 1


class Stepper:
    """
    Stepper motor class.

    :param uperObj: Uper or similar IoBoard
    :type uperObj: :class:`IoTPy.pyuper.ioboard.IoBoard`
    :param stepsIn360: The number of steps in full (360 degree) rotation.
    :type stepsIn360: int
    :param coilA0: GPIO of coil A pin 0.
    :type coilA0: GPIO
    :param coilA1: GPIO of coil A pin 1.
    :type coilA1: GPIO
    :param coilB0: GPIO of coil B pin 0.
    :type coilB0: GPIO
    :param coilB1: GPIO of coil B pin 1.
    :type coilB1: GPIO
    """

    def __init__(self, uperObj, stepsIn360, coilA0, coilA1, coilB0, coilB1):
        self.u = uperObj
        self.totalSteps = stepsIn360
        self.delayLength = 0.01

        # Wave stepping scheme, full step
        self.fullStepCoilA = [1,0,-1,0]
        self.fullStepCoilB = [0,1,0,-1]

        # Half stepping scheme
        self.halfStepCoilA = [1,1,0,-1,-1,-1,0,1]
        self.halfStepCoilB = [0,1,1,1,0,-1,-1,-1]

        self.stepperMode = FULL_STEP

        # declare pins
        self.A0 = coilA0
        self.A1 = coilA1

        self.B0 = coilB0
        self.B1 = coilB1

        # declare motor pins in output mode
        self.A0.setup(GPIO.OUTPUT)
        self.A1.setup(GPIO.OUTPUT)

        self.B0.setup(GPIO.OUTPUT)
        self.B1.setup(GPIO.OUTPUT)

    def setStepperMode(self, sMode):
        """
        Set stepper motor step mode.

        :param sMode: Step mode: Stepper.FULL_STEP or Stepper.HALF_STEP
        """
        self.stepperMode = sMode

    def setSpeed(self, rpm):
        """
        Set stepper motor rotation speed.

        :param rpm: Revolutions per second.
        :type rpm: int
        """
        self.delayLength = 30.0/(self.totalSteps*rpm)

    def _fireSignal(self, pin0, pin1, data):
        if data == 0:
            pin0.write(0)
            pin1.write(0)
        elif data == 1:
            pin0.write(1)
            pin1.write(0)
        elif data == -1:
            pin0.write(0)
            pin1.write(1)

    def step(self, steps):
        """
        Step a specified number of steps.

        :param steps: Number of steps.
        :type steps: int
        """
        nSteps = abs(steps)
        for s in xrange(0,nSteps):
            if (self.stepperMode==FULL_STEP):
                phase = s%4
                if (steps>0):
                    self._fireSignal(self.A0,self.A1, self.fullStepCoilA[phase])
                    self._fireSignal(self.B0,self.B1, self.fullStepCoilB[phase])
                else :
                    self._fireSignal(self.A0,self.A1, self.fullStepCoilB[phase])
                    self._fireSignal(self.B0,self.B1, self.fullStepCoilA[phase])
                sleep(self.delayLength)

            elif (self.stepperMode==HALF_STEP):
                phase = s%8
                if (steps>0):
                    self._fireSignal(self.A0,self.A1, self.halfStepCoilA[phase])
                    self._fireSignal(self.B0,self.B1, self.halfStepCoilB[phase])
                else :
                    self._fireSignal(self.A0,self.A1, self.halfStepCoilB[phase])
                    self._fireSignal(self.B0,self.B1, self.halfStepCoilA[phase])
                sleep(self.delayLength)
