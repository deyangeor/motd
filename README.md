# Acronis homework

A project to hold a home assignment from Acronis for SRE engineer

## Prerequisites

Most of the work was done on a debian based machines.

Used tools:
- ansible
- packer
- docker

Install ansible:

```
apt install ansible 
```

A guide of how to install docker on ubuntu:
https://docs.docker.com/install/linux/docker-ce/ubuntu/

Packer can be downloaded from here:
https://www.packer.io/downloads.html

## motd API
### Install system prerequisites
```
yum -y install epel-release && yum clean all
yum -y install python36

pip3 install -r /opt/motd/requiremets.txt
```

### Available resources:

1. /set_motd_data
	Method: POST
	Dataset: JSON containing date, time, ip and date hash  
		example: {'current_date': '', 'current_time': '', 'local_ip': '', 'current_time_hash': ''}  
	Returns: string -- "Row Added" on success

	This resource will save the dataset in a sqlite3 database, so it can be requested via the /info resource

2. /info
	Method: GET  
	Dataset: a parameter having a host_ip to search the database for  
		curl example:  
			```curl -X GET http://localhost:5000/info -d "host_ip=127.0.0.1"```  
	Returns: JSON string containing the matching row in the database:  
		example: "{\"date\": \"2019-7-15\", \"time\": \"10-45-6\", \"ip\": \"10.10.65.178\", \"hash\": \"398c6bf9ec8ba15ea3f9561980efab8a\"}"


## motd handler
### Install system prerequisites
```
yum -y install epel-release && yum clean all
yum -y install python36
```

The script collects local information about the machine it is running on:
1. Date
2. Time
3. IP address
4. Hashes the date using SHA1

Updates the default message of the day file /etc/motd with the data.  
Provides the data to the motd api, so it stores it.
