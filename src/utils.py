import enum
import time

BITS_PER_CHARACTER = 8

DEFAULT_ARGS = {
	'sync_time_s': 20.0,
	'allocation_time_s': 5.0,
	'allocation_factor': 0.8
}

# type of resource: normal (increasing and decreasing), or always increasing
class ResourceType(enum.Enum):
	NORMAL = 0
	REVERSE = 1
	ALWAYSINCREASING = 2

# template for the covert channel sender/receiver
class CovertChannelTypeTemplate:
	#resource_type = ResourceType.NORMAL
	def __init__(self, config, sync):
		self.config = config
		self.sync = sync
		sleepuntilnextsync(sync)
	def send(self, allocate_channel_callback, bit_array):
		for b in bit_array:
			if self.config.get('verbose'): print('Sending bit: {}'.format(b))
			allocate_channel_callback(b, self.config.get('allocation_amount'), self.config.get('allocation_time_s') * self.config.get('allocation_factor'))
			sleepuntilnextsync(self.sync, self.config.get('allocation_time_s'))
	def receive(self, get_channel_resource_callback, parameters=None):
		received_bits = []
		full_text_received = ''
		data_t0 = None
		while True:
			data_current = get_channel_resource_callback(parameters)
			if data_t0 is None: data_t0 = data_current
			data_samples = [data_current]
			last_sample_received_time = None
			read_one = None
			if self.config.get('samples_count') is None:
				read_one = ((data_current - data_t0) >= self.config.get('threshold'))
			else:
				for i in range(len(data_samples), self.config.get('samples_count')):
					sleep_time = getadjustedsleeptime(self.sync, (self.config.get('allocation_time_s') / self.config.get('samples_count')), last_sample_received_time)
					sleep_time *= self.config.get('allocation_factor')
					time.sleep(sleep_time)
					data_samples.append(get_channel_resource_callback(parameters))
					last_sample_received_time = gettime()
				if self.resource_type == ResourceType.NORMAL:
					data_avg = sum(data_samples) / len(data_samples)
					read_one = ((data_avg - data_t0) >= self.config.get('threshold'))
				if self.resource_type == ResourceType.REVERSE:
					data_avg = sum(data_samples) / len(data_samples)
					read_one = ((data_t0 - data_avg) >= self.config.get('threshold'))
				if self.resource_type == ResourceType.ALWAYSINCREASING:
					read_one = ((max(data_samples) - data_t0) >= self.config.get('threshold'))
					data_t0 = max(data_samples)
			read_value = 1 if read_one else 0
			if self.config.get('verbose'): print('Received bit: {}'.format(read_value))
			received_bits.append(read_value)
			if len(received_bits) >= BITS_PER_CHARACTER:
				if received_bits[-BITS_PER_CHARACTER:] == [0] * BITS_PER_CHARACTER: break
			sleepuntilnextsync(self.sync, self.config.get('allocation_time_s'))
		print('Full text received: \'{}\''.format(convertfrombitsequence(received_bits).decode()[:-1]))

# converts a byte-encoded message m to a sequence of bits, where each character is composed by 8 bits
def converttobitsequence(m):
	if m[-1] != 0: m += '\0'.encode()
	r = []
	for e in m:
		s = '{0:08b}'.format(e)
		r += [int(x) for x in list(s)]
	return r

# converts a sequence of bits to a byte-encoded message m
def convertfrombitsequence(s):
	chars = []
	for b in range(int(len(s) / 8)):
		byte = s[b*8:(b+1)*8]
		chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
	return ''.join(chars).encode()

# gets current time in milliseconds
def gettime(): return time.time()

# gets the sleep time, given a fixed timeout to adjust, current time and previous time
def getsleeptime(timeout, current_time, previous_time):
	elapsed_time = float(current_time) - float(previous_time)
	if elapsed_time > timeout: return timeout
	res = float(timeout) - elapsed_time
	if res > timeout: return timeout
	if res < 0: return 0
	return res

# gets the adjusted sleep time, if configured to adjust it
def getadjustedsleeptime(sync_config, timeout, last_measured_time):
	if not sync_config.get('adjust_timeout_allocation'): return timeout
	if last_measured_time is None: return timeout
	time_since_last_bit_sent = gettime() - last_measured_time
	sleep_time = float(timeout) - float(time_since_last_bit_sent)
	return sleep_time

# syncronizes sender and receiver to communicate at `sync['seconds'] + delay` multiples
def sleepuntilnextsync(sync_config, delay=None):
	sync = sync_config.get('sync_type')
	if sync.get('type') == 'time':
		if delay is None: delay = sync.get('seconds')
		time_to_wait = delay - (gettime() % delay)
		time.sleep(time_to_wait)
