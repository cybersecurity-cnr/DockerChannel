# importing custom libraries
import utils

# importing standard libraries
import subprocess

# implementing the channel
class CovertChannelType(utils.CovertChannelTypeTemplate):
	# the resource type
	resource_type = utils.ResourceType.ALWAYSINCREASING
	# given an input bit_to_transmit, computes processes (allocation_amount operations for each round), while period is ignored
	def allocate_channel(bit_to_transmit, allocation_amount, period):
		if bit_to_transmit == 0: return
		for i in range(0, int(allocation_amount)): subprocess.call(['ls', '-lha'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	# returns the number of active processes
	def get_channel_resource(config):
		with open('/proc/stat', 'r') as mem: lines = mem.readlines()
		return int(lines[-4].split()[1])
