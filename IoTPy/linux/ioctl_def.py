
IOCTL_NRBITS = 8
IOCTL_TYPEBITS = 8
IOCTL_SIZEBITS = 13
IOCTL_DIRBITS = 2

IOCTL_NRSHIFT = 0
IOCTL_TYPESHIFT = IOCTL_NRSHIFT + IOCTL_NRBITS
IOCTL_SIZESHIFT = IOCTL_TYPESHIFT + IOCTL_TYPEBITS
IOCTL_DIRSHIFT = IOCTL_SIZESHIFT + IOCTL_SIZEBITS


def IOC(d, t, nr, size):
    return (d << IOCTL_DIRSHIFT) | (t << IOCTL_TYPESHIFT) |\
            (nr << IOCTL_NRSHIFT) | (size << IOCTL_SIZESHIFT)


def IO(t, nr):
    return IOC(1, t, nr, 0)


def IOW(t, nr, size):
    return IOC(4, t, nr, size)


def IOR(t, nr, size):
    return IOC(2, t, nr, size)


def IOWR(t, nr, size):
    return IOC(6, t, nr, size)