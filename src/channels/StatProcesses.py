# importing custom libraries
import utils

# importing standard libraries
import subprocess

# implementing the channel
class CovertChannelType(utils.CovertChannelTypeTemplate):
	# the resource type
	resource_type = utils.ResourceType.ALWAYSINCREASING
	# given an input b bit to send over the channel, computes processes (n operations for each round), while t is ignored
	def allocate_channel(b, n, t):
		if b == 0: return
		for i in range(0, int(n)): subprocess.call(['ls', '-lha'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	# returns the number of active processes
	def get_channel_resource(config):
		with open('/proc/stat', 'r') as mem: lines = mem.readlines()
		return int(lines[-4].split()[1])
