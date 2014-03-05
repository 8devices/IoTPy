import uper,time

data_pin = 1
clk_pin = 2

LOW = 0
HIGH =1
LSBFIRST = 1
MSBFIRST = 0
OUTPUT = 1
INPUT = 0

TempCmd  = 0x03

def shiftOut(data_pin, clk_pin, bit_order, byte, bits):
	for i in range(bits):
		if bit_order == LSBFIRST:
			u.digitalWrite(data_pin, byte & (1 << i))
		else:
			u.digitalWrite(data_pin, byte & (1 << (7 -i)))
		u.digitalWrite(clk_pin, HIGH)
		time.sleep(0.0003)
		u.digitalWrite(clk_pin, LOW)

def sendCommandSHT(command, data_pin, clk_pin):
	u.digitalWrite(data_pin, HIGH)
	u.digitalWrite(clk_pin, HIGH)
	u.digitalWrite(data_pin, LOW);
	u.digitalWrite(clk_pin, LOW);
	u.digitalWrite(clk_pin, HIGH);
	u.digitalWrite(data_pin, HIGH);
	u.digitalWrite(clk_pin, LOW);
	u.digitalWrite(data_pin, LOW);

	shiftOut(data_pin, clk_pin, MSBFIRST, command, 8)
	u.digitalWrite(clk_pin, HIGH)
	ack = u.digitalRead(data_pin)
	if ack != LOW:
		print "Ack Error 0"
	u.digitalWrite(clk_pin, LOW)
	ack = u.digitalRead(data_pin)
	if ack != HIGH:
		print "Ack Error 1"

def shiftIn(data_pin, clk_pin, bits):
	ret = 0
	for i in range(bits):
		u.digitalWrite(clk_pin, HIGH)
		time.sleep(0.01)
		ret = ret * 2 + u.digitalRead(data_pin)
		u.digitalWrite(clk_pin, LOW)
	return(ret)

def waitForResultSHT(data_pin):
	for i in range(100):
		time.sleep(0.002)
		ack = u.digitalRead(data_pin)
		if ack == LOW:
			break
	if ack == HIGH:
		print "Ack Error 2"

def getData16SHT(data_pin, clk_pin):
	val = shiftIn(data_pin,clk_pin,8)
	val = val *256
	u.digitalWrite(data_pin, HIGH)
	u.digitalWrite(data_pin, LOW)
	u.digitalWrite(clk_pin, HIGH)
	u.digitalWrite(clk_pin, LOW)
	val |= shiftIn(data_pin, clk_pin, 8)
	return(val)

def skipCrcSHT(data_pin, clk_pin):
	u.digitalWrite(data_pin, HIGH)
	u.digitalWrite(clk_pin, HIGH)
	u.digitalWrite(clk_pin, LOW)

def readTemperatureRaw():
	sendCommandSHT(0x03, data_pin, clk_pin)
	waitForResultSHT(data_pin)
	val = getData16SHT(data_pin, clk_pin)
	skipCrcSHT(data_pin, clk_pin)
	return(val)

def readTemperatureC():
	return((readTemperatureRaw() * 0.01) - 40.0)

def readTemperatureF():
	return((readTemperatureRaw() * 0.018) - 40.0)

def readHumidity():
	C1 = -4.0;       # for 12 Bit
	C2 =  0.0405;    # for 12 Bit
	C3 = -0.0000028; # for 12 Bit
 	T1 =  0.01;      # for 14 Bit @ 5V
	T2 =  0.00008;   # for 14 Bit @ 5V
	sendCommandSHT(0x05, data_pin, clk_pin)
	waitForResultSHT(data_pin)
	val = getData16SHT(data_pin, clk_pin)
	skipCrcSHT(data_pin, clk_pin)
	linearHumidity = C1 + C2 * val + C3 * val * val
	return((readTemperatureC() - 25.0 ) * (T1 + T2 * val) + linearHumidity)

if __name__ == '__main__':
	u = uper.Uper()
	"""
	print "Temperature RAW = ", readTemperatureRaw()
	"""
	while 1:
		print "Temperature in C = ", readTemperatureC()
		print "Temperature in F = ", readTemperatureF()
		print "Humidity = ", readHumidity()
		time.sleep(0.5)
