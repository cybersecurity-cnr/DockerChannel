# DockerChannel

DockerChannel is a Python framework that allows to test covert channels among containers.

In particular, it contains 5 different covert channels that exploit difference resources "poorly" isolated when deploying containers via Docker, i.e., the free memory, the CPU load, the number of processes, the number of TCP sockets, and the number of inodes.
DockerChannel allows to use and evaluate the already implemented channels, as well as create new channels.

This repository represents an outcome of a joint research by [CNR-IMATI](https://imati.cnr.it) and [CNR-IEIIT](https://www.ieiit.cnr.it).
In case of exploitation for research purposes, please mention the following paper.

*TO BE ADDED ONCE THE PAPER IS ACCEPTED*

### Installation ###

* Clone the repository:
```
git clone https://github.com/cybersecurity-cnr/DockerChannel
```
* `cd` into the cloned repository source files:
```
cd DockerChannel/src
```
* Build the Docker image:
```
docker build -t dockerchannel .
```
* Optionally, save the Docker image to file:
```
docker save dockerchannel:latest|gzip > dockerchannel.tar.gz
```

### Usage ###

Although a Docker execution is suggested, it's possible to run the program also manually.
For the Docker case, some environment variables have to be configured.
Instead, for the manual case, all variables can be provided in input to the program as arguments.
In both the cases, it is needed to run two separate instances of the program: one for the sender, one for the receiver.

#### Execution through Docker ####

In this case, the following environment variables can be used.

| Environment variable              | Mandatory        | Default value | Type            | Units                            | Accepted values                               | Required by      | Same value for sender and receiver | Details                                                                                                     |
| --------------------------------- | ---------------- | ------------- | --------------- | -------------------------------- | --------------------------------------------- | ---------------- | ---------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `container_role`                  | Yes              | -             | `string`        | -                                | `sender`, `receiver`                          | sender, receiver | No                                 | Specifies the role of the current container                                                                 |
| `channel_type`                    | Yes              | -             | `string`        | -                                | All names of classes in the `channels` folder | sender, receiver | Yes                                | Specifies the channel type                                                                                  |
| `adjust_timeout_allocation`       | No               | `1`           | `boolean`       | -                                | `0` (for `False`), `1` (for `True`)           | sender, receiver | Yes                                | Specifies if the timeout allocation has to be periodically decreased in function of the time needed to execute other operations, to strictly respect/syncronize with the given timeout for each send/reception |
| `verbose`                         | No               | `0`           | `boolean`       | -                                | `0` (for `False`), `1` (for `True`)           | sender, receiver | Yes                                | Specifies if a verbose ouput should be provided or not |
| `sync_time_s`                     | No               | 20            | `float`         | seconds                          | Any float value greater than zero             | sender, receiver | Yes                                | Specifies the multiple to use for initial sync between sender and receiver                                  |
| `allocation_time_s`               | No               | 5             | `float`         | seconds                          | Any float value greater than zero             | sender, receiver | Yes                                | Specifies the time needed to allocate a single bit,                                                         |
| `allocation_factor`               | No               | 0.8           | `float`         | percentage                       | Any float value in `(0, 1]`                   | sender, receiver | Yes                                | Specifies the amount of time to use for send/reception of a single bit, over the entire allocation time     |
| `allocation_amount`               | Yes (`sender`)   | -             | `float`         | depending on the adopted channel | Any float value                               | sender           | -                                  | Specifies the amount of resource to allocate to send a single bit                                           |
| `message`                         | Yes (`sender`)   | -             | `string`        | -                                | Any 8 bit ASCII string                        | sender           | -                                  | Specifies the message to transmit over the covert channel                                                   |
| `threshold`                       | Yes (`receiver`) | -             | `float`         | depending on the adopted channel | Any float value                               | receiver         | -                                  | Specifies the threshold to use to discriminate between `0` and `1` bit values                               |
| `samples_count`                   | No               | 5             | `integer`       | -                                | Any integer value greater than zero           | receiver         | -                                  | Specifies the number of samples to consider for each round, to compute an average of the resource allocation |

##### Sample executions #####

**Memory**

In this case, the `allocation_amount` and `threshold` variables are expressed in terms of megabytes.
For further information, please refer to the scientific paper mentioned above.

* sender:
```
docker run \
	-e container_role=sender \
	-e channel_type=Memory \
	-e adjust_timeout_allocation=1 \
	-e sync_time_s=20 \
	-e allocation_time_s=5 \
	-e allocation_factor=0.8 \
	-e allocation_amount=500 \
	-e message=secret \
	-e verbose=1 \
	-t dockerchannel
```
* receiver:
```
docker run \
	-e container_role=receiver \
	-e channel_type=Memory \
	-e adjust_timeout_allocation=1 \
	-e sync_time_s=20 \
	-e allocation_time_s=5 \
	-e allocation_factor=0.8 \
	-e threshold=200 \
	-e samples_count=5 \
	-e verbose=1 \
	-t dockerchannel
```

**CPU**

In this case, the `allocation_amount` variable is expressed in terms of operations to execute for each round, while the `threshold` variable is expressed in terms of a percentage increase of the CPU.
For further information, please refer to the scientific paper mentioned above.

* sender:
```
docker run \
	-e container_role=sender \
	-e channel_type=Cpu \
	-e adjust_timeout_allocation=1 \
	-e sync_time_s=20 \
	-e allocation_time_s=5 \
	-e allocation_factor=0.8 \
	-e allocation_amount=1000000 \
	-e message=secret \
	-e verbose=1 \
	-t dockerchannel
```
* receiver:
```
docker run \
	-e container_role=receiver \
	-e channel_type=Cpu \
	-e adjust_timeout_allocation=1 \
	-e sync_time_s=20 \
	-e allocation_time_s=5 \
	-e allocation_factor=0.8 \
	-e threshold=15 \
	-e samples_count=1 \
	-e verbose=1 \
	-t dockerchannel
```

**StatProcesses**

In this case, the `allocation_amount` and `threshold` variables are expressed in terms of the number of processes generated by the sender at each round.
For further information, please refer to the scientific paper mentioned above.

* sender:
```
docker run \
	-e container_role=sender \
	-e channel_type=StatProcesses \
	-e adjust_timeout_allocation=1 \
	-e sync_time_s=20 \
	-e allocation_time_s=5 \
	-e allocation_factor=0.8 \
	-e allocation_amount=1000 \
	-e message=secret \
	-e verbose=1 \
	-t dockerchannel
```
* receiver:
```
docker run \
	-e container_role=receiver \
	-e channel_type=StatProcesses \
	-e adjust_timeout_allocation=1 \
	-e sync_time_s=20 \
	-e allocation_time_s=5 \
	-e allocation_factor=0.8 \
	-e threshold=800 \
	-e samples_count=5 \
	-e verbose=1 \
	-t dockerchannel
```

**Inode**

In this case, the `allocation_amount` and `threshold` variables are expressed in terms of the number of files created at each round.
For further information, please refer to the scientific paper mentioned above.

* sender:
```
docker run \
	-e container_role=sender \
	-e channel_type=Inode \
	-e adjust_timeout_allocation=1 \
	-e sync_time_s=20 \
	-e allocation_time_s=5 \
	-e allocation_factor=0.8 \
	-e allocation_amount=500 \
	-e message=secret \
	-e verbose=1 \
	-t dockerchannel
```
* receiver:
```
docker run \
	-e container_role=receiver \
	-e channel_type=Inode \
	-e adjust_timeout_allocation=1 \
	-e sync_time_s=20 \
	-e allocation_time_s=5 \
	-e allocation_factor=0.8 \
	-e threshold=100 \
	-e samples_count=5 \
	-e verbose=1 \
	-t dockerchannel
```

**Sockstat**

In this case, the `allocation_amount` and `threshold` variables are expressed in terms of the number of bind [sockets created](https://sleeplessbeastie.eu/2019/08/07/how-to-count-tcp-connections/) at each round.
For further information, please refer to the scientific paper mentioned above.

* sender:
```
docker run \
	-e container_role=sender \
	-e channel_type=Sockstat \
	-e adjust_timeout_allocation=1 \
	-e sync_time_s=20 \
	-e allocation_time_s=5 \
	-e allocation_factor=0.8 \
	-e allocation_amount=10 \
	-e message=secret \
	-e verbose=1 \
	-t dockerchannel
```
* receiver:
```
docker run \
	-e container_role=receiver \
	-e channel_type=Sockstat \
	-e adjust_timeout_allocation=1 \
	-e sync_time_s=20 \
	-e allocation_time_s=5 \
	-e allocation_factor=0.8 \
	-e threshold=5 \
	-e samples_count=5 \
	-e verbose=1 \
	-t dockerchannel
```

#### Manual execution by command line ####

It is also possible to launch the following command to get information on the syntax to use for executing DockerChannel via CLI.
Required parameters and their reference is similar (although not exactly the same; see, i.e., the `adjust_timeout_allocation` parameter) to the one reported in the table above for the Docker case.
```
python3 CovertChannel.py -h
```

### Implementation of a new channel ###

Choose a `<filename>` for the Python file to create.
Hence, create a file `<filename>.py` under the `channels` folder.

A starting point to implement the new channel is given by the following code snippet.
```
# importing custom libraries
import utils

# importing standard libraries, if needed

# implementing the channel: do not change class and methods definitions
class CovertChannelType(utils.CovertChannelTypeTemplate):
	# used by the receiver: specify which resource type is this one: NORMAL, REVERSE, ALWAYSINCREASING
	resource_type = utils.ResourceType.NORMAL
	# used by the sender: given an input bit `bit_to_transmit` and an input `allocation_amount` related to a specific configuration for the current channel, allocates the channel for `period` seconds
	def allocate_channel(bit_to_transmit, allocation_amount, period):
		# TODO implement
		pass # does not return anything
	# used by the receiver: returns channel information/bit, given the current receiver configuration file `config`
	def get_channel_resource(config):
		# TODO implement
		return 0 # return either 0 or 1
```
For real samples, see the files under the `channels` folder.

In case the installation of specific libraries is required, properly update the `requirements.txt` file.

If you intend to implement a new channel, open a merge request to include it in this repository and you to the contributors list.

### Credits ###

* [Enrico Cambiaso](https://www.ieiit.cnr.it/people/Cambiaso-Enrico)
* [Luca Caviglione](https://www.imati.cnr.it/mypage.php?idk=PG-44)
* [Marco Zuppelli](https://www.imati.cnr.it/mypage.php?idk=PG-157)

### Acknowledgement ###

This work was partially supported by project [SERICS](https://serics.eu) (PE00000014) under the NRRP MUR program funded by the EU - NGEU.
