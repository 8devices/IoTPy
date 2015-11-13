from IoTPy.sfp import decode_sfp, encode_sfp
from IoTPy.pinmaps import *
from IoTPy.interfaces.gpio import GPIO


class DigitalPin(object):
    def __init__(self, mode=GPIO.PULL_UP, value=GPIO.LOW, primary=True):
        self.mode = mode
        self.value = value
        self.primary = primary

    def set_primary(self):
        self.primary = True

    def set_secondary(self):
        self.primary = False

    def set_mode(self, mode):
        if mode in (GPIO.PULL_UP, GPIO.PULL_DOWN, GPIO.HIGH_Z, GPIO.OUTPUT):
            self.mode = mode

    def write(self, value):
        if value == GPIO.LOW:
            self.value = GPIO.LOW
        else:
            self.value = GPIO.HIGH

    def read(self):
        return self.value


class AnalogPin(object):
    def __init__(self, value=0):
        self.value = value


class PwmPin(object):
    def __init__(self, duty_cycle=0):
        self.value = duty_cycle


class SfpMachine(object):

    def __init__(self):
        self.pin_states = {}
        self.pin_id_list = []
        for pin in pin_list:
            pin_id = pin[0]
            pin_caps = pin[1]
            pin_extras = pin[2]
            if pin_caps & CAP_ADC:
                secondary_function = AnalogPin()
            elif pin_caps & CAP_PWM:
                secondary_function = PwmPin()
            else:
                secondary_function = None
            self.pin_states[pin_id] = (pin_caps, pin_extras, DigitalPin(), secondary_function)
            self.pin_id_list.append(pin_id)
        self.sfp_comands = {}
        self.sfp_comands[1] = self.set_primary
        self.sfp_comands[2] = self.set_secondary
        self.sfp_comands[3] = self.set_pin_mode
        self.sfp_comands[4] = self.digital_write
        self.sfp_comands[5] = self.digital_read
        self.sfp_comands[6] = self.attach_interrupt
        self.sfp_comands[7] = self.detach_interrupt
        #self.sfp_comands[9] =
        self.sfp_comands[255] = self.get_device_info

    def set_primary(self,arg_list):
        pin_id = arg_list[0]
        if pin_id in self.pin_id_list:
            self.pin_states[pin_id][2].set_primary()

    def set_secondary(self, arg_list):
        pin_id = arg_list[0]
        if pin_id in self.pin_id_list:
            self.pin_states[pin_id][2].set_secondary()

    def set_pin_mode(self, arg_list):
        pin_id = arg_list[0]
        mode = arg_list[1]
        if pin_id in self.pin_id_list:
            self.pin_states[pin_id][2].set_mode(mode)

    def digital_write(self, arg_list):
        pin_id = arg_list[0]
        value = arg_list[1]
        if pin_id in self.pin_id_list:
            self.pin_states[pin_id][2].write(value)

    def digital_read(self, arg_list):
        pin_id = arg_list[0]
        if pin_id in self.pin_id_list:
            return pin_id, self.pin_states[pin_id][2].read()

    def attach_interrupt(self, arg_list):
        pass

    def detach_interrupt(self, arg_list):
        pass

    def get_device_info(self, arg_list):
        return 44,0,44,0

    def execute_sfp(self, binary_sfp_command):
        decoded_sfp_command = decode_sfp(binary_sfp_command)
        results = self.sfp_comands[decoded_sfp_command[0]](decoded_sfp_command[1])
        if results:
            return encode_sfp(decoded_sfp_command[0], results)