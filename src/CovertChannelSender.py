# import of ad-hoc implemented libraries
import utils

# import of implemented channels
import sys
sys.path.append('./channels')

# sender class
class CovertChannelSender:
	# initialization
	def __init__(self, method, config, sync):
		mod = __import__('{}'.format(method), fromlist=['CovertChannelType'])
		covertchanneltype_class = getattr(mod, 'CovertChannelType')
		self.obj = covertchanneltype_class(config, sync)

	# send of a sequence of bits `bits_array`
	def send_bits(self, bits_array):
		self.obj.send(self.obj.__class__.allocate_channel, bits_array)

	# send of a message `message`
	def send_string(self, message):
		bits_array = utils.converttobitsequence(message)
		self.send_bits(bits_array)
