from IoTPy.ioboard.utils import IoTPy_APIError
from builtins import chr
from six import binary_type, integer_types
import struct
import types


def _encode_int(intarg):
    if intarg < 64:
        return chr(intarg).encode('latin-1')
    packedint = struct.pack('>I', intarg).lstrip(b'\x00')
    return chr(0xc0 | (len(packedint) - 1)).encode('latin-1') + packedint


def _encode_bytes(bytestr):
    if len(bytestr) < 64:
        return chr(0x40 | len(bytestr)).encode('latin-1') + bytestr
    packedlen = struct.pack('>I', len(bytestr)).lstrip(b'\x00')
    if len(packedlen) == 1:
        return b'\xc4' + packedlen + bytestr
    elif len(packedlen) == 2:
        return b'\xc5' + packedlen + bytestr
    else:
        raise IoTPy_APIError("UPER API: - too long string passed to UPER, encode_bytes can't handle it.")


def encode_sfp(command, args):
    """
    Construct binary SFP command.

    :param command: SFP command ID.
    :type command: int
    :param args: A list of SFP arguments, which can be either an integer or a byte collection (string).
    :type args: list
    :return: Binary SFP command.
    :rtype: str
    """
    functions = {
        binary_type: _encode_bytes,
        integer_types[0]: _encode_int   #[0] - kinda hack to get class int
    }

    sfp_command = chr(command).encode('latin-1') + b''.join(functions[type(arg)](arg) for arg in args)
    sfp_command = b'\xd4' + struct.pack('>H', len(sfp_command)) + sfp_command
    return sfp_command


def decode_sfp(buffer):
    """
    Decode SFP command from byte buffer.

    :param buffer: A byte buffer which stores SFP command.
    :type buffer: str
    :return: A list containing decoded SFP function ID and arguments (if any).
    """
    result = []
    if buffer[0:1] != b'\xd4':
        return result
    buflen = struct.unpack('>H', buffer[1:3])[0] + 3    # get SFP msg lenght
    result.append(struct.unpack('B', buffer[3:4])[0])   # get SFP command code
    pointer = 4
    args = []
    while pointer < buflen:
        argtype = ord(buffer[pointer:pointer + 1])
        pointer += 1
        if argtype < 64:                    # short int
            args.append(argtype)
        elif argtype < 128:                    # short str
            arglen = argtype & 0x3f
            args.append(buffer[pointer:pointer + arglen])
            pointer += arglen
        else:
            arglen = argtype & 0x0f
            if arglen < 4:            # decoding integers
                if arglen == 0:
                    args.append(ord(buffer[pointer:pointer + 1]))
                elif arglen == 1:
                    args.append(struct.unpack('>H', buffer[pointer:pointer + 2])[0])
                elif arglen == 2:
                    args.append(struct.unpack('>I', b'\x00' + buffer[pointer:pointer + 3])[0])
                elif arglen == 3:
                    args.append(struct.unpack('>I', buffer[pointer:pointer + 4])[0])
                pointer += arglen + 1
            else:
                if argtype == 0xc4:        # decoding strings
                    arglen = ord(buffer[pointer:pointer + 1])
                elif argtype == 0xc5:
                    arglen = struct.unpack('>H', buffer[pointer:pointer + 2])[0]
                    pointer += 1
                else:
                    raise IoTPy_APIError("UPER API: Bad parameter type in decodeSFP method.")
                pointer += 1
                args.append(buffer[pointer:pointer + arglen])
                pointer += arglen
    result.append(args)
    return result
