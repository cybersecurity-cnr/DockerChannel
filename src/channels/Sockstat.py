# importing custom libraries
import utils

# importing standard libraries
import time
import socket

# local variables
BIND_HOST = '127.0.0.1'
PORTS = range(1024, 65535)

# implementing the channel
class CovertChannelType(utils.CovertChannelTypeTemplate):
	# the resource type
	resource_type = utils.ResourceType.NORMAL
	# given an input bit_to_transmit, binds to allocation_amount sockets for period seconds
	def allocate_channel(bit_to_transmit, allocation_amount, period):
		if bit_to_transmit == 0:
			time.sleep(period)
			return
		sockets = []
		for port in PORTS:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			try:
				s.bind((BIND_HOST, port))
				sockets.append(s)
				if len(sockets) == allocation_amount: break
			except: pass
		time.sleep(period)
		for s in sockets: s.close()
	# returns the number of opened TCP sockets
	def get_channel_resource(config):
		with open('/proc/net/sockstat', 'r') as f: lines = f.readlines()
		return int(lines[1].split()[8])
