import math

class Servo(object):
    MAX_PW = 2500
    MIN_PW = 500
    _freq = 50
    def __init__(self, pwm):
        super().__init__()
        self.pwm = pwm
        self.pwm.period(4095)
        # self.angle(90)

    def map(self, x, in_min, in_max, out_min, out_max):
        mapping = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        print(f"mapping set to: {mapping}")
        return mapping
        
    # angle ranges -90 to 90 degrees
    def angle(self, angle):
        print('servo set to angel: {angle}')
        pass
        
class PWM():
    def __init__(self, channel, debug="critical"):
        super().__init__()
        if isinstance(channel, str):
            if channel.startswith("P"):
                channel = int(channel[1:])
            else:
                raise ValueError("PWM channel should be between [P1, P14], not {0}".format(channel))

        self.debug = debug
        # self._debug("PWM address: {:02X}".format(self.ADDR))
        self.channel = channel
        self.timer = int(channel/4)
        self._pulse_width = 0
        self._freq = 50
        self.freq(50)

    def freq(self, *freq):
        if len(freq) == 0:
            print(f"frequency: {self._freq}")
            return self._freq
        else:
            pass

    def prescaler(self, *prescaler):
        if len(prescaler) == 0:
            print(f"prescaler: {self._prescaler}")
            return self._prescaler
        else:
            pass

    def period(self, *arr):
        global timer
        if len(arr) == 0:
            print(f"timer: {timer[self.timer]['arr']}")
            return timer[self.timer]["arr"]
        else:
            timer = [
            {
                "arr": 0
            }
        ] * 4
            timer[self.timer]["arr"] = int(arr[0]) - 1
            pass

    def pulse_width(self, *pulse_width):
        if len(pulse_width) == 0:
            return self._pulse_width
        else:
            pass

    def pulse_width_percent(self, *pulse_width_percent):
        global timer
        if len(pulse_width_percent) == 0:
            print(f"pulse width %: {self._pulse_width_percent}")
            return self._pulse_width_percent
        else:
            pass
            
class fileDB(object):
	"""A file based database.

    A file based database, read and write arguements in the specific file.
    """
	def __init__(self, db=None):
		'''Init the db_file is a file to save the datas.'''
		# Check if db_file is defined
		if db != None:
			self.db = db
		else:
			self.db = "config"

	def get(self, name, default_value=None):
		"""Get value by data's name. Default value is for the arguemants do not exist"""
		try:
			conf = open(self.db,'r')
			lines=conf.readlines()
			conf.close()
			file_len=len(lines)-1
			flag = False
			# Find the arguement and set the value
			for i in range(file_len):
				if lines[i][0] != '#':
					if lines[i].split('=')[0].strip() == name:
						value = lines[i].split('=')[1].replace(' ', '').strip()
						flag = True
			if flag:
				return value
			else:
				return default_value
		except FileNotFoundError:
			conf = open(self.db,'w')
			conf.write("")
			conf.close()
			return default_value
		except :
			return default_value
	
	def set(self, name, value):
		"""Set value by data's name. Or create one if the arguement does not exist"""

		# Read the file
		conf = open(self.db,'r')
		lines=conf.readlines()
		conf.close()
		file_len=len(lines)-1
		flag = False
		# Find the arguement and set the value
		for i in range(file_len):
			if lines[i][0] != '#':
				if lines[i].split('=')[0].strip() == name:
					lines[i] = '%s = %s\n' % (name, value)
					flag = True
		# If arguement does not exist, create one
		if not flag:
			lines.append('%s = %s\n\n' % (name, value))

		# Save the file
		conf = open(self.db,'w')
		conf.writelines(lines)
		conf.close()
        
class Pin(object):

    _dict = {
        "BOARD_TYPE": 12,
    }

    _dict_1 = {
        "D0":  17,
        "D1":  18,
        "D2":  27,
        "D3":  22,
        "D4":  23,
        "D5":  24,
        "D6":  25,
        "D7":  4,
        "D8":  5,
        "D9":  6,
        "D10": 12,
        "D11": 13,
        "D12": 19,
        "D13": 16,
        "D14": 26,
        "D15": 20,
        "D16": 21,
        "SW":  19,
        "LED": 26,
        "BOARD_TYPE": 12,
        "RST": 16,
        "BLEINT": 13,
        "BLERST": 20,
        "MCURST": 21,
    }

    _dict_2 = {
        "D0":  17,
        "D1":   4, # Changed
        "D2":  27,
        "D3":  22,
        "D4":  23,
        "D5":  24,
        "D6":  25, # Removed
        "D7":   4, # Removed
        "D8":   5, # Removed
        "D9":   6,
        "D10": 12,
        "D11": 13,
        "D12": 19,
        "D13": 16,
        "D14": 26,
        "D15": 20,
        "D16": 21,
        "SW":  25, # Changed
        "LED": 26,
        "BOARD_TYPE": 12,
        "RST": 16,
        "BLEINT": 13,
        "BLERST": 20,
        "MCURST":  5, # Changed
    }

    def __init__(self, *value):
        super().__init__()

        self.check_board_type()

        if len(value) > 0:
            pin = value[0]
        if len(value) > 1:
            mode = value[1]
        else:
            mode = None
        if len(value) > 2:
            setup = value[2]
        else:
            setup = None
        if isinstance(pin, str):
            try:
                self._board_name = pin
                self._pin = self.dict()[pin]
            except Exception as e:
                print(e)
        elif isinstance(pin, int):
            self._pin = pin
        else:
            self._error('Pin should be in %s, not %s' % (self._dict.keys(), pin))
        self._value = 0
        self.init(mode)
        # self._info("Pin init finished.")
        
    def check_board_type(self):
        type_pin = self.dict()["BOARD_TYPE"]

    def init(self, mode):
        self._mode = mode
        if mode != None:
            if pull != None:
                GPIO.setup(self._pin, mode, pull_up_down=pull)
            else:
                GPIO.setup(self._pin, mode)

    def dict(self, *_dict):
        if len(_dict) == 0:
            return self._dict
        else:
            if isinstance(_dict, dict):
                self._dict = _dict
            else:
                self._error(
                    'argument should be a pin dictionary like {"my pin": ezblock.Pin.cpu.GPIO17}, not %s' % _dict)

    def __call__(self, value):
        return self.value(value)

    def value(self, *value):
        if len(value) == 0:
            self.mode(self.IN)
            result = GPIO.input(self._pin)
            # self._debug("read pin %s: %s" % (self._pin, result))
            return result
        else:
            value = value[0]
            return value

    def on(self):
        return self.value(1)

    def off(self):
        return self.value(0)

    def high(self):
        return self.on()

    def low(self):
        return self.off()

    def mode(self, *value):
        if len(value) == 0:
            return self._mode
        else:
            mode = value[0]
            self._mode = mode
            GPIO.setup(self._pin, mode)

    def pull(self, *value):
        return self._pull

    def irq(self, handler=None, trigger=None, bouncetime=200):
        self.mode(self.IN)
        GPIO.add_event_detect(self._pin, trigger, callback=handler, bouncetime=bouncetime)

    def name(self):
        return "GPIO%s"%self._pin

    def names(self):
        return [self.name, self._board_name]

    class cpu(object):
        GPIO17 = 17
        GPIO18 = 18
        GPIO27 = 27
        GPIO22 = 22
        GPIO23 = 23
        GPIO24 = 24
        GPIO25 = 25
        GPIO26 = 26
        GPIO4  = 4
        GPIO5  = 5
        GPIO6  = 6
        GPIO12 = 12
        GPIO13 = 13
        GPIO19 = 19
        GPIO16 = 16
        GPIO26 = 26
        GPIO20 = 20
        GPIO21 = 21

        def __init__(self):
            pass
        
class ADC():
    ADDR=0x14                   # 扩展板的地址为0x14

    def __init__(self, chn):    # 参数，通道数，树莓派扩展板上有8个adc通道分别为"A0, A1, A2, A3, A4, A5, A6, A7"
        super().__init__()
        if isinstance(chn, str):
            if chn.startswith("A"):     # 判断穿境来的参数是否为A开头，如果是，取A后面的数字出来
                chn = int(chn[1:])
            else:
                raise ValueError("ADC channel should be between [A0, A7], not {0}".format(chn))
        if chn < 0 or chn > 7:          # 判断取出来的数字是否在0~7的范围内
            self._error('Incorrect channel range')
        chn = 7 - chn
        self.chn = chn | 0x10           # 给从机地址
        self.reg = 0x40 + self.chn
        # self.bus = smbus.SMBus(1)
        
    def read(self):                     # adc通道读取数---写一次数据，读取两次数据 （读取的数据范围是0~4095）
        # self._debug("Write 0x%02X to 0x%02X"%(self.chn, self.ADDR))
        # self.bus.write_byte(self.ADDR, self.chn)      # 写入数据
        self.send([self.chn, 0, 0], self.ADDR)

        # self._debug("Read from 0x%02X"%(self.ADDR))
        # value_h = self.bus.read_byte(self.ADDR)
        value_h = self.recv(1, self.ADDR)[0]            # 读取数据

        # self._debug("Read from 0x%02X"%(self.ADDR))
        # value_l = self.bus.read_byte(self.ADDR)
        value_l = self.recv(1, self.ADDR)[0]            # 读取数据（读两次）

        value = (value_h << 8) + value_l
        # self._debug("Read value: %s"%value)
        return value

    def read_voltage(self):                             # 将读取的数据转化为电压值（0~3.3V）
        return self.read*3.3/4095