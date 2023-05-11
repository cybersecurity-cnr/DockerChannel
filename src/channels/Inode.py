# importing custom libraries
import utils

# importing standard libraries
import os
import time
import subprocess

# files main directory
FILES_DIR = '/tmp'

# implementing the channel
class CovertChannelType(utils.CovertChannelTypeTemplate):
	# the resource type
	resource_type = utils.ResourceType.REVERSE
	# given an input bit_to_transmit, creates allocation_amount files for period seconds
	def allocate_channel(bit_to_transmit, allocation_amount, period):
		if bit_to_transmit == 0:
			time.sleep(period)
			return
		for i in range(0, int(allocation_amount)):
			with open('{}/covertchannel_file_{}.txt'.format(FILES_DIR, i), 'w') as f: f.write(str(i))
		time.sleep(period)
		for i in range(0, int(allocation_amount)): os.remove('{}/covertchannel_file_{}.txt'.format(FILES_DIR, i))
	# returns the number of created files
	def get_channel_resource(config):
		proc = subprocess.Popen(['df', '-i'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
		data = proc.stdout.read().decode()
		data = data.split('\n')[1].split()[3]
		return int(data)
