import os, glob, urllib, urllib2, platform

class Upgrader:
	def __init__(self):
		return

	def puttoFile(self, content, file_name):
		try:
			file_id = os.open(file_name, os.O_WRONLY)
			os.write(file_id, content)
			os.close(file_id)
		except OSError:
			pass

	def resetUper(self):
		self.puttoFile("1","/sys/class/gpio/gpio22/value")
		self.puttoFile("0","/sys/class/gpio/gpio22/value")

	def upgradeFirmware(self, fwUrl = "https://github.com/8devices/UPER/raw/master/dist/UPER-Release.bin"):
		acm_interface = "/dev/ttyACM0"
		sd_devices = "/dev/sd*"
		fw_file = "/tmp/latest_UPER_firmware.bin"
		UPER_flash_pattern = "CRP DISABLD"
		new_dev_list = []

		# put UPER1 in to programming mode
		self.puttoFile("22","/sys/class/gpio/export") # 14'th Carambola2 dev bord pin - reset on UPER
		self.puttoFile("23","/sys/class/gpio/export") # 15'th Carambola2 dev bord pin - prog on UPER
		self.puttoFile("out","/sys/class/gpio/gpio22/direction")
		self.puttoFile("out","/sys/class/gpio/gpio23/direction")
		self.puttoFile("1","/sys/class/gpio/gpio22/value")
		self.puttoFile("1","/sys/class/gpio/gpio23/value")
		self.puttoFile("0","/sys/class/gpio/gpio22/value")
		time.sleep(2) # wait for linux to settle after UPER reboot in to pgm state
		self.puttoFile("0","/sys/class/gpio/gpio23/value")

		# find UPER1 block device
		list_block_devs = glob.glob("/sys/block/sd*")
		block_device_name = ''
		header = ''
		for try_device_name in list_block_devs:
			try_device_name = "/dev/" + try_device_name.split('/')[-1]
			try:
				block_device = os.open(try_device_name, os.O_RDWR)
				os.lseek(block_device, 3 * 512, os.SEEK_SET)
				header = os.read(block_device,11)
				os.close(block_device)
			except OSError:
				print "neradau ant", try_device_name
				pass
			if header == UPER_flash_pattern: # "CRP DISABLD"
				#found UPER
				block_device_name = try_device_name
				break;
		if block_device_name == '':
			print "UPER: firmware upgrade error, no UPPER board found"
			return

		# download firmware file 
		print "Will get firmware from URL:" 
		print fwUrl
		
		try:
			req = urllib2.Request(fwUrl)
			handle = urllib2.urlopen(req)
		except urllib2.HTTPError, e:
			print "UPER: Can't download firmware, error code - %s." % e.code
			self.resetUper()
			return
		except urllib2.URLError:
			print "UPER: Bad URL for firmware file: %s" % fwUrl
			self.resetUper()
			return
		else:
			urllib.urlretrieve(fwUrl, fw_file + '.new')
			if os.path.isfile(fw_file + '.new'):
				os.rename(fw_file + '.new', fw_file)

		#os.system("dd if="+fw_file+" of="+new_dev_list[0]+" seek=4")

		# read the fw from file	
		fw_file_id = open(fw_file)
		firmware = fw_file_id.read()
		fw_file_id.close()

		block_device = os.open( block_device_name, os.O_RDWR)
		os.lseek(block_device, 4 * 512, os.SEEK_SET)
		os.write(block_device, firmware)
		os.close(block_device)

		# reset UPER
		self.resetUper()
		time.sleep(2)
		return
