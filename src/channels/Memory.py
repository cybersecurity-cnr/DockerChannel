# importing custom libraries
import utils

# importing standard libraries
import time

# converts n bytes to n megabytes
def mbtob(n): return n * (2 ** 20)

# implementing the channel
class CovertChannelType(utils.CovertChannelTypeTemplate):
	# the resource type
	resource_type = utils.ResourceType.REVERSE
	# adjusting metrics for channel allocation and thresholds, from megabytes to bytes
	def __init__(self, config, sync):
		super().__init__(config, sync)
		fields = ['allocation_amount', 'threshold']
		for f in fields:
			if not self.config.get(f) is None: self.config[f] = mbtob(self.config.get(f))
	# starting from b value of the current byte, allocates n bytes for t seconds
	def allocate_channel(b, n, t):
		if b == 0:
			time.sleep(t)
			return
		tmp = 'a' * int(n)
		time.sleep(t)
		del tmp
	# returns the free memory, in bytes
	def get_channel_resource(config):
		with open('/proc/meminfo', 'r') as f: lines = f.readlines()
		return int(lines[1].split()[1]) * (2**10)
