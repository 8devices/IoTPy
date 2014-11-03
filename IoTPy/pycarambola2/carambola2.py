import subprocess

from IoTPy.core.gpio import GPIOProducer
from IoTPy.linux.gpio import LinuxGPIO


class Carambola2(GPIOProducer):

    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def execute(self, cmd):
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = proc.communicate()

        return proc.returncode, out, err

    def GPIO(self, name, *args, **kwargs):
        _names = [1, 11, 12, 15, 16, 17, 18, 19, 20, 21, 22, 23]
        if name not in _names:
            raise ValueError("Invalid GPIO name %s. Must be one of %s." % (name, ", ".join(sorted(_names))))

        return LinuxGPIO(name)