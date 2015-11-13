from IoTPy.errors import IoTPy_APIError
from builtins import chr
from six import binary_type, integer_types
from struct import pack, unpack


def _encode_int(intarg):
    if intarg < 64:
        return chr(intarg).encode('latin-1')
    packedint = pack('>I', intarg).lstrip(b'\x00')
    return chr(0xc0 | (len(packedint) - 1)).encode('latin-1') + packedint


def _encode_bytes(bytestr):
    if len(bytestr) < 64:
        return chr(0x40 | len(bytestr)).encode('latin-1') + bytestr
    packedlen = pack('>I', len(bytestr)).lstrip(b'\x00')
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
    sfp_command = b'\xd4' + pack('>H', len(sfp_command)) + sfp_command
    return sfp_command


def decode_sfp(buffer):
    """
    Decode SFP command from byte buffer.

    :param buffer: A byte buffer which stores SFP command.
    :type buffer: bytes string
    :return: SFP function ID and arguments list.
    """
    if buffer[0:1] != b'\xd4':
        return
    command_length = unpack('>H', buffer[1:3])[0] + 3    # get SFP command length located in two bytes
    sfp_command = unpack('B', buffer[3:4])[0]            # get SFP command code
    pointer = 4
    args = []
    while pointer < command_length:
        arg_type = ord(buffer[pointer:pointer + 1])
        pointer += 1
        if arg_type < 64:                    # short int
            args.append(arg_type)
        elif arg_type < 128:                    # short str
            arg_len = arg_type & 0x3f
            args.append(buffer[pointer:pointer + arg_len])
            pointer += arg_len
        else:
            arg_len = arg_type & 0x0f
            if arg_len < 4:            # decoding integers
                if arg_len == 0:
                    args.append(ord(buffer[pointer:pointer + 1]))
                elif arg_len == 1:
                    args.append(unpack('>H', buffer[pointer:pointer + 2])[0])
                elif arg_len == 2:
                    args.append(unpack('>I', b'\x00' + buffer[pointer:pointer + 3])[0])
                elif arg_len == 3:
                    args.append(unpack('>I', buffer[pointer:pointer + 4])[0])
                pointer += arg_len + 1
            else:
                if arg_type == 0xc4:        # decoding strings
                    arg_len = ord(buffer[pointer:pointer + 1])
                elif arg_type == 0xc5:
                    arg_len = unpack('>H', buffer[pointer:pointer + 2])[0]
                    pointer += 1
                else:
                    raise IoTPy_APIError("UPER API: Bad parameter type in decodeSFP method.")
                pointer += 1
                args.append(buffer[pointer:pointer + arg_len])
                pointer += arg_len
    return sfp_command, args


def valid_message(buf):
    if len(buf) < 3:
        return False

    cmd, length = unpack('!BH', buf[:3])
    if cmd != 0xD4:
        raise Exception("IoTPy wrong command in socket")

    return len(buf) >= length + 3


def command_slicer(buf):
    commands_list = []
    while buf:
        if not valid_message(buf):
            return buf, commands_list

        cmd, length = unpack('!BH', buf[:3])

        if len(buf) < (length + 3):
            return buf, commands_list

        sfp = buf[:length + 3]      # SFP header + data
        buf = buf[length + 3:]
        commands_list.append(sfp)

    return buf, commands_list

