import uper, time, struct

I2C_ADDR_AM2321 = 0x5c # 0xB8 >> 1
PARAM_AM2321_READ = '\x03'
REG_AM2321_HUMIDITY_MSB = '\x00'
REG_AM2321_HUMIDITY_LSB = '\x01'
REG_AM2321_TEMPERATURE_MSB = '\x02'
REG_AM2321_TEMPERATURE_LSB = '\x03'
REG_AM2321_DEVICE_ID_BIT_24_31 = '\x0B'

def readRaw( i2caddr, command, regaddr, regcount):	
	up.i2c_trans(i2caddr, '', 1)
	up.i2c_trans(i2caddr, command+regaddr+chr(regcount), 0)
	time.sleep(0.002)
	buf, i2cerror = up.i2c_trans(i2caddr, '', regcount + 4)
	if i2cerror is None:
		crc = struct.unpack('<H', buf[-2:])[0]
		if crc != am_crc16(buf[:-2]):
			return '', -99
		return buf[2:-2], None
	else:
		return '', i2cerror

def am_crc16(buf):
	crc = 0xFFFF
	for c in buf:
		crc ^= ord(c)
		for i in range(8):
			if crc & 0x01:
				crc >>= 1
				crc ^= 0xA001
			else:
				crc >>= 1
	return(crc)

def readUID():
	resp, readraw_error = readRaw(I2C_ADDR_AM2321, PARAM_AM2321_READ, REG_AM2321_DEVICE_ID_BIT_24_31, 4)
	if readraw_error is None:
		uid = struct.unpack('>I', resp)[0]
	else:
		uid = 0
	return uid, readraw_error

def readAM2321():
	rawdata, readraw_error = readRaw(I2C_ADDR_AM2321, PARAM_AM2321_READ, REG_AM2321_HUMIDITY_MSB, 4)
	if readraw_error is None:
		return struct.unpack('>H',rawdata[-2:])[0]/10.0, struct.unpack('>H',rawdata[-4:2])[0]/10.0, None
	else:
		return 0, 0, readraw_error

up = uper.Uper()
up.i2c_begin()
print "UID", hex(readUID()[0])
time.sleep(.45)
print "UID", hex(readUID()[0])

for i in range(0,100):
	time.sleep(0.5)
	temp, hum, read_errorcode = readAM2321()
	if read_errorcode is None:
		print "Temperature =", temp, "C"
		print "Humidity =", hum, "%"
	else:
		print "AM2321 read error, code = ", read_errorcode
up.i2c_end()
