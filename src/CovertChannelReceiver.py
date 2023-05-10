# import of ad-hoc implemented libraries
import utils

# import of implemented channels
import sys
sys.path.append('./channels')

# sender class
class CovertChannelReceiver:
	# initialization
	def __init__(self, method, config, sync):
		mod = __import__('{}'.format(method), fromlist=['CovertChannelType'])
		covertchanneltype_class = getattr(mod, 'CovertChannelType')
		self.obj = covertchanneltype_class(config, sync)
	# receives of a sequence of bits `bits_array`
	def receive(self, config):
		data = self.obj.receive(self.obj.__class__.get_channel_resource, config)
