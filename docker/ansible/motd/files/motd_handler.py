
import socket
import requests
import datetime
import hashlib
import json

MOTD_DATA_HOST = 'http://localhost:5000'
MOTD_FILE = '/etc/motd'

def get_local_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.connect(('1.2.3.4',80))                                                                                                                          
        return sock.getsockname()[0]

host_data = {}

now = datetime.datetime.now()

host_data['current_date'] = '{y}-{m}-{d}'.format(y=now.year,m=now.month,d=now.day)
host_data['current_date_hash'] = hashlib.md5(host_data['current_date'].encode()).hexdigest()

host_data['current_time'] = '{h}-{m}-{s}'.format(h=now.hour,m=now.minute,s=now.second)
host_data['local_ip'] = get_local_ip()

with open(MOTD_FILE, 'w') as f:
    f.write('Data for today:\nDate: {current_date}\nTime: {current_time}\nIP: {local_ip}\nhash: {current_date_hash}'.format(**host_data))


send = requests.post('{}/set_motd_data'.format(MOTD_DATA_HOST), data={'host_data': json.dumps(host_data)})

