# importing custom libraries
import utils

# importing standard libraries
import time
import psutil

# implementing the channel
class CovertChannelType(utils.CovertChannelTypeTemplate):
	# the resource type
	resource_type = utils.ResourceType.NORMAL
	# given an input bit_to_transmit, computes cpu operations (allocation_amount operations for each round), for period seconds
	def allocate_channel(bit_to_transmit, allocation_amount, period):
		if bit_to_transmit == 0:
			time.sleep(period)
			return
		tmp = 0
		begin_time = utils.gettime()
		while True:
			for i in range(0, int(allocation_amount)): tmp += i
			elapsed_time = utils.gettime() - begin_time
			if elapsed_time >= period: break
	# returns the cpu usage, in percentage
	def get_channel_resource(config): return psutil.cpu_percent(config.get('allocation_time_s')-1)
