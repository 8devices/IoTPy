

class I2C(object):

    def __enter__(self):
        raise NotImplementedError()

    def __exit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError()

    def read(self, address, count):
        raise NotImplementedError()

    def write(self, address, data):
        raise NotImplementedError()

    def transaction(self, address, data, read_len):
        raise NotImplementedError()


class I2CProducer(object):

    def I2C(self, name, clock=15000, *args, **kwargs):
        raise NotImplementedError()
