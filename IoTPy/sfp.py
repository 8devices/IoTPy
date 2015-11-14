from IoTPy.errors import IoTPy_APIError
from builtins import chr
from six import binary_type, integer_types
from struct import pack, unpack


def _encode_int(intarg):
    if intarg < 64:
        return chr(intarg).encode('latin-1')
    packedint = pack('>I', intarg).lstrip(b'\x00')
    return chr(0xc0 | (len(packedint) - 1)).encode('latin-1') + packedint


def _encode_bytes(byte_string):
    if len(byte_string) < 64:
        return chr(0x40 | len(byte_string)).encode('latin-1') + byte_string
    packedlen = pack('>I', len(byte_string)).lstrip(b'\x00')
    if len(packedlen) == 1:
        return b'\xc4' + packedlen + byte_string
    elif len(packedlen) == 2:
        return b'\xc5' + packedlen + byte_string
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
        integer_types[0]: _encode_int   # [0] - kinda hack to get class int
    }

    sfp_command = chr(command).encode('latin-1') + b''.join(functions[type(arg)](arg) for arg in args)
    sfp_command = b'\xd4' + pack('>H', len(sfp_command)) + sfp_command
    return sfp_command


def decode_sfp(io_buffer):
    """
    Decode SFP command from byte buffer.

    :param io_buffer: A byte buffer which stores SFP command.
    :type io_buffer: bytes string
    :return: SFP function ID and arguments list.
    """
    if io_buffer[0:1] != b'\xd4':
        return
    command_length = unpack('>H', io_buffer[1:3])[0] + 3    # get SFP command length located in two bytes
    sfp_command = unpack('B', io_buffer[3:4])[0]            # get SFP command code
    pointer = 4
    args = []
    while pointer < command_length:
        arg_type = ord(io_buffer[pointer:pointer + 1])
        pointer += 1
        if arg_type < 64:                    # short int
            args.append(arg_type)
        elif arg_type < 128:                    # short str
            arg_len = arg_type & 0x3f
            args.append(io_buffer[pointer:pointer + arg_len])
            pointer += arg_len
        else:
            arg_len = arg_type & 0x0f
            if arg_len < 4:            # decoding integers
                if arg_len == 0:
                    args.append(ord(io_buffer[pointer:pointer + 1]))
                elif arg_len == 1:
                    args.append(unpack('>H', io_buffer[pointer:pointer + 2])[0])
                elif arg_len == 2:
                    args.append(unpack('>I', b'\x00' + io_buffer[pointer:pointer + 3])[0])
                elif arg_len == 3:
                    args.append(unpack('>I', io_buffer[pointer:pointer + 4])[0])
                pointer += arg_len + 1
            else:
                if arg_type == 0xc4:        # decoding strings
                    arg_len = ord(io_buffer[pointer:pointer + 1])
                elif arg_type == 0xc5:
                    arg_len = unpack('>H', io_buffer[pointer:pointer + 2])[0]
                    pointer += 1
                else:
                    raise IoTPy_APIError("UPER API: Bad parameter type in decodeSFP method.")
                pointer += 1
                args.append(io_buffer[pointer:pointer + arg_len])
                pointer += arg_len
    return sfp_command, args


def valid_message(io_buffer):
    if len(io_buffer) < 3:
        return False

    cmd, length = unpack('!BH', io_buffer[:3])
    if cmd != 0xD4:
        raise Exception("IoTPy wrong command in socket")

    return len(io_buffer) >= length + 3


def command_slicer(io_buffer):
    commands_list = []
    while io_buffer:
        if not valid_message(io_buffer):
            return io_buffer, commands_list

        cmd, length = unpack('!BH', io_buffer[:3])

        if len(io_buffer) < (length + 3):
            return io_buffer, commands_list

        sfp_command = io_buffer[:length + 3]      # SFP header + data
        io_buffer = io_buffer[length + 3:]
        commands_list.append(sfp_command)

    return io_buffer, commands_list
