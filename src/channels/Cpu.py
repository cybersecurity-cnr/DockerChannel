# importing custom libraries
import utils

# importing standard libraries
import time
import psutil

# implementing the channel
class CovertChannelType(utils.CovertChannelTypeTemplate):
	# the resource type
	resource_type = utils.ResourceType.NORMAL
	# given an input b bit, computes cpu operations (n operations for each round), for t seconds
	def allocate_channel(b, n, t):
		if b == 0:
			time.sleep(t)
			return
		tmp = 0
		begin_time = utils.gettime()
		while True:
			for i in range(0, int(n)): tmp += i
			elapsed_time = utils.gettime() - begin_time
			if elapsed_time >= t: break
	# returns the cpu usage, in percentage
	def get_channel_resource(config): return psutil.cpu_percent(config.get('allocation_time_s')-1)
