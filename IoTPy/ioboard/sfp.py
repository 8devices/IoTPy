__author__ = 'jonas'
from IoTPy.ioboard.utils import IoTPy_APIError
import struct
import types

def _encode_int(intarg):
    if intarg < 64:
        return chr(intarg)
    packedint = struct.pack('>I', intarg).lstrip('\x00')
    return chr(0xc0 | (len(packedint) - 1)) + packedint

def _encode_bytes(bytestr):
    if len(bytestr) < 64:
        return chr(0x40 | len(bytestr)) + bytestr
    packedlen = struct.pack('>I', len(bytestr)).lstrip('\x00')
    if len(packedlen) == 1:
        return '\xc4' + packedlen + bytestr
    elif len(packedlen) == 2:
        return '\xc5' + packedlen + bytestr
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
        types.StringType: _encode_bytes,
        bytearray: _encode_bytes,
        types.IntType: _encode_int
    }
    sfp_command = chr(command) + ''.join(str(functions[type(arg)](arg)) for arg in args)
    sfp_command = '\xd4' + struct.pack('>H', len(sfp_command)) + sfp_command
    return sfp_command

def decode_sfp(buffer):
    """
    Decode SFP command from byte buffer.

    :param buffer: A byte buffer which stores SFP command.
    :type buffer: str
    :return: A list containing decoded SFP function ID and arguments (if any).
    """
    result = []
    if buffer[0:1] != '\xd4':
        return result
    buflen = struct.unpack('>H', buffer[1:3])[0] + 3
    result.append(struct.unpack('b', buffer[3:4])[0])
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
                    args.append(struct.unpack('>I', '\x00' + buffer[pointer:pointer + 3])[0])
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
