#!/bin/bash

import os
import argparse

import utils

# lists all implemented channels, by looking at their implementation inside of the `channels` folder
def getimplementedchannels():
	r = []
	f = os.listdir('channels')
	ext = '.py'
	for e in f:
		if e[-len(ext):] == ext: r.append(e[:-len(ext)])
	return r

containerrole = os.environ.get('container_role')
obj = os.environ

if containerrole is None:
	parser = argparse.ArgumentParser(description='DockerChannel - Covert channel tools for containerized environments')

	# generic
	parser.add_argument('-r','--containerrole', dest='container_role', type=str, help='Specifies if the current container acts as \'sender\' or \'receiver\'', required=True)
	notes = 'must be the same value between sender and receiver'
	parser.add_argument('-c','--channeltype', dest='channel_type', type=str, help='Specifies the channel type: allowed once are: {} ({})'.format(', '.join(getimplementedchannels()), notes), required=True)

	# for both sender and receiver
	notes = 'must be the same value between sender and receiver'
	parser.add_argument('-j','--adjusttimeoutallocation', dest='adjust_timeout_allocation', type=bool, action=argparse.BooleanOptionalAction, help='Specifies if the timeout allocation has to be periodically decreased in function of the time needed to execute other operations, to strictly respect/syncronize with the given timeout for each send/reception ({})'.format(notes), required=False)
	parser.set_defaults(adjusttimeoutallocation=True)
	parser.add_argument('-v','--verbose', dest='verbose', type=bool, action=argparse.BooleanOptionalAction, help='Specifies if a verbose output has to be provided ({})'.format(notes), required=False)
	parser.set_defaults(verbose=False)
	parser.add_argument('-s','--synctime', dest='sync_time_s', type=float, help='Specifies the multiple to use for initial sync between sender and receiver, in seconds ({})'.format(notes), required=False, default=utils.DEFAULT_ARGS.get('sync_time_s'))
	parser.add_argument('-t','--allocationtime', dest='allocation_time_s', type=float, help='Specifies the time needed to allocate a single bit, in seconds ({})'.format(notes), required=False, default=utils.DEFAULT_ARGS.get('allocation_time_s'))
	parser.add_argument('-f','--allocationfactor', dest='allocation_factor', type=float, help='Specifies the amount of time to use for send/reception of a single bit, in percentage, over the entire allocation time ({})'.format(notes), required=False, default=utils.DEFAULT_ARGS.get('allocation_factor'))

	# for sender only
	notes = 'required just for the sender'
	parser.add_argument('-a','--allocationamount', dest='allocation_amount', type=float, help='Specifies the amount of resource to allocate to send a single bit ({})'.format(notes), required=False)
	parser.add_argument('-m','--message', dest='message', type=str, help='Specifies the message to transmit over the covert channel ({})'.format(notes), required=False)

	# for receiver only
	notes = 'required just for the receiver'
	parser.add_argument('-e','--threshold', dest='threshold', type=float, help='Specifies the threshold to use to discriminate between 0 and 1 bits ({})'.format(notes), required=False)
	parser.add_argument('-l','--samplescount', dest='samples_count', type=int, help='Specifies the number of samples to consider for each round, to compute an average of the resource allocation ({})'.format(notes), required=False)

	# arguments parsing
	args = vars(parser.parse_args())

	# setting obj
	obj = args
	containerrole = args.get('container_role')
else:
	fields = ['container_role', 'channel_type', 'adjust_timeout_allocation', 'sync_time_s', 'allocation_time_s', 'allocation_factor', 'allocation_amount', 'message', 'threshold', 'samples_count', 'verbose']
	new_obj = {e:obj.get(e) for e in fields}
	obj = new_obj
	fields = ['adjust_timeout_allocation', 'verbose']
	for f in fields:
		if not obj.get(f) is None: obj[f] = (int(obj.get(f)) == 1)
	fields = ['sync_time_s', 'allocation_time_s', 'allocation_factor', 'allocation_amount', 'threshold']
	for f in fields:
		if not obj.get(f) is None: obj[f] = float(obj.get(f))
	fields = ['samples_count']
	for f in fields:
		if not obj.get(f) is None: obj[f] = int(obj.get(f))
	for k in utils.DEFAULT_ARGS: obj[k] = utils.DEFAULT_ARGS.get(k)

fields = ['adjust_timeout_allocation']
sync = {e:obj.get(e) for e in fields}
sync['sync_type'] = {'type':'time', 'seconds':float(obj.get('sync_time_s'))}

fields = ['allocation_time_s', 'allocation_factor', 'verbose']
config = {e:obj.get(e) for e in fields}

print('Selected channel: {}'.format(obj.get('channel_type')))

if containerrole.lower() == 'sender':
	print('Sending message: \'{}\''.format(obj.get('message')))
	from CovertChannelSender import *
	fields = ['allocation_amount']
	config.update({e:obj.get(e) for e in fields})
	sender = CovertChannelSender(obj.get('channel_type'), config, sync)
	data = obj.get('message').encode()
	sender.send_string(data)

if containerrole.lower() == 'receiver':
	from CovertChannelReceiver import *
	fields = ['threshold', 'samples_count']
	config.update({e:obj.get(e) for e in fields})
	#config['resource_type'] = utils.ResourceType.NORMAL
	#if obj.get('resource_type').lower() == 'alwaysincreasing': config['resource_type'] = utils.ResourceType.ALWAYSINCREASING
	receiver = CovertChannelReceiver(obj.get('channel_type'), config, sync)
	receiver.receive(config)
