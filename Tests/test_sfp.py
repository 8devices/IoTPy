import unittest
import IoTPy.sfp as sfp


class Test_sfp(unittest.TestCase):

    def test_simple_sfp_encode(self):
        self.assertEqual(sfp.encode_sfp(255, []), b'\xd4\x00\x01\xff')

    def test_simple_sfp_decode(self):
        self.assertEqual(sfp.decode_sfp(b'\xd4\x00\x01\xff'),[255, []])

    def test_encode_sfp(self):
        sfp_parameters = [b'09876543210987654321098765432109876543210987654321098765432109876543210987654321', b'0987654321', 0, 1, 64, 6000, 70000]
        sfp_command = 255
        encode_result = sfp.encode_sfp(sfp_command, sfp_parameters)
        self.assertEqual(encode_result, b'\xd4\x00i\xff\xc4P09876543210987654321098765432109876543210987654321098765432109876543210987654321J0987654321\x00\x01\xc0@\xc1\x17p\xc2\x01\x11p')

    def test_decode_sfp(self):
        decode_result = sfp.decode_sfp(b'\xd4\x00i\xff\xc4P09876543210987654321098765432109876543210987654321098765432109876543210987654321J0987654321\x00\x01\xc0@\xc1\x17p\xc2\x01\x11p')
        sfp_parameters = [b'09876543210987654321098765432109876543210987654321098765432109876543210987654321', b'0987654321', 0, 1, 64, 6000, 70000]
        sfp_command = 255
        self.assertEqual(decode_result, [sfp_command, sfp_parameters])

if __name__ == '__main__':
    unittest.main()