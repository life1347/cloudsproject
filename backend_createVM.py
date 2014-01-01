import logging
import pprint
import time
from time import sleep, asctime
from keystoneclient.v2_0 import client as ksclient
from novaclient.v1_1 import client as nclient
from neutronclient.v2_0 import client as neclient

logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.DEBUG)

KEYSTONE_URL='https://openstack.nctu.edu.tw/keystone/v2.0'

#username = "0256547"
#password = "03067"
global vm_counter
vm_counter=0


def createVM(now):
	global vm_counter
	username = ['0256547','0256081','0256017','0156153']
	password = ['03067','2','3','swluo@cs.nctu.edu.tw']
	tenant_name=['CloudOS2013_0256547','CloudOS2013_0256081','CloudOS2013_0256017','CloudOS2013_0156153']

	ne=neclient.Client(auth_url=KEYSTONE_URL, username = username[now], tenant_name = tenant_name[now], password = password[now], insecure = True)

	nc=nclient.Client(auth_url=KEYSTONE_URL, username = username[now], api_key = password[now], project_id=tenant_name[now], service_type='compute', insecure = True)

	if not nc.keypairs.findall(name="0256547_key"):
		    with open(os.path.expanduser('~/.ssh/id_rsa.pub')) as fpubkey:
			nc.keypairs.create(name="0256547_key", public_key=fpubkey.read())

	image = nc.images.find(name = "webserver-cloudOSproject")
	flavor = nc.flavors.find(name = "m1.tiny")

	network_name = username[now] + '_network'
	mynet = ne.list_networks(name = network_name)
	mynet_id = mynet['networks'][0]['id']

	vm_name = 'VM_' + username[now] + '_' + str(vm_counter)
	server1 = nc.servers.create(name = vm_name, 
				   image = image.id, 
				   flavor = flavor.id, 
		                   nics = [{'net-id' : mynet_id}],
		                   key_name = '0256547_key')

	vm_counter = vm_counter + 1

	status = server1.status
	while status == 'BUILD':
		    time.sleep(5)
		    # Retrieve the instance again so the status field updates
		    server1 = nc.servers.get(server1.id)
		    status = server1.status
	print "status: %s" % status

	for network_label, address_list in server1.addresses.items():
		        server1.networks[network_label] = [a['addr'] for a in address_list]
		        print server1.networks[network_label]


	ip0 = str(server1.networks[network_label])


	ip1 = ip0.split('\'')[1]
	ip2 = str(ip1).translate(None, "'")
	f = open('iplist_back.txt', 'a')
	f.write(str(ip2) + '\n')




#createVM(0)
