import logging

import pprint

import time

import os

from time import sleep, asctime

from keystoneclient.v2_0 import client as ksclient

from neutronclient.v2_0 import client as neclient

from novaclient.v1_1 import client as nclient



logging.basicConfig(level=logging.INFO)

#logging.basicConfig(level=logging.DEBUG)



KEYSTONE_URL='https://openstack.nctu.edu.tw/keystone/v2.0'



#username = "0256547"

#password = "03067"





def create_proxy(now):



	username = ['0256547','0256081','0256017','0156153']

	password = ['03067','2','3','swluo@cs.nctu.edu.tw']

	tenant_name=['CloudOS2013_0256547','CloudOS2013_0256081','CloudOS2013_0256017','CloudOS2013_0156153']







	ne=neclient.Client(auth_url=KEYSTONE_URL, username = username[now], tenant_name = tenant_name[now], password = password[now], insecure = True)



	nc=nclient.Client(auth_url=KEYSTONE_URL, username = username[now], api_key = password[now], project_id=tenant_name[now],service_type='compute', insecure = True)



	router_name = username[now] + '_router'

	network_name = username[now] + '_network'

	subnet_name = username[now] + '_subnet'

	mynet_id = ''

	sub_id = ''

	router1_id = ''

	if not ne.list_networks(name = network_name)['networks']:

		print 'create network'

		mynet = ne.create_network({'network':{'name': network_name, 'admin_state_up': True, }})

		mynet_id = mynet['network']['id']

	else:

		mynet = ne.list_networks(name = network_name)

		mynet_id = mynet['networks'][0]['id']

		print 'mynet_id=',

		print mynet_id



	if not ne.list_subnets(name = subnet_name)['subnets']:

		print 'create subnet'

		cidr = 250

		subnet_cidr = '192.168.' + str(cidr+now) + '.0/24'

		sub = ne.create_subnet({'subnet':{'name':subnet_name, 'network_id': mynet_id, 'ip_version': 4, 'cidr': subnet_cidr, 'dns_nameservers': ['8.8.8.8']}})

		sub_id = sub['subnet']['id']

	else:

		sub = ne.list_subnets(name = subnet_name)

		sub_id = sub['subnets'][0]['id']

		print 'sub_id=',

		print sub_id



	if not ne.list_routers(name = router_name)['routers']:

		print 'create router'

		ne.create_router({'router':{ 'name': router_name, 'admin_state_up' : True }})

		router1 = ne.list_routers(name = router_name)

		router1_id = router1['routers'][0]['id']

		ext_net = ne.list_networks(name = 'ext-net') 

		ext_net_id = ext_net['networks'][0]['id']

		ne.add_gateway_router(router1_id,{'network_id': ext_net_id})

		ne.add_interface_router(router1_id,{'subnet_id': sub_id})

	#else:

	#	print 'set gateway and interface'

	#	router1 = ne.list_routers(name = router_name)

	#	router1_id = router1['routers'][0]['id']

	#	ext_net = ne.list_networks(name = 'ext-net') 

	#	ext_net_id = ext_net['networks'][0]['id']

	#	ne.add_gateway_router(router1_id,{'network_id': ext_net_id})

	#	ne.add_interface_router(router1_id,{'subnet_id': sub_id})



	if not nc.keypairs.findall(name="0256547_key"):

	    with open(os.path.expanduser('~/.ssh/id_rsa.pub')) as fpubkey:

		nc.keypairs.create(name="0256547_key", public_key=fpubkey.read())



	image = nc.images.find(name = "0156153_ubuntu")

	flavor = nc.flavors.find(name = "cpu4ram4disk20")
        

      

	vm_name = 'VM_' + username[now] + '_proxy' 

	server1 = nc.servers.create(name = vm_name, 

				   image = image.id, 

				   flavor = flavor.id, 

		                   nics = [{'net-id' : mynet_id}],

		                   key_name = '0256547_key')







	status = server1.status

	while status == 'BUILD':

		    time.sleep(5)

		    # Retrieve the instance again so the status field updates

		    server1 = nc.servers.get(server1.id)

		    status = server1.status

	print "status: %s" % status

	
	f = open('iplist_front.txt', 'a')
	#check floating ip to avoid unnecessary  create floating ip

	floatingiplist =  nc.floating_ips.list()
	
	a = 0
	for x in range(len(floatingiplist)) : 
		if floatingiplist[x].instance_id == None and floatingiplist[x].ip != None:
			server1.add_floating_ip(floatingiplist[x].ip)
			f.write(floatingiplist[x].ip + '\n')
			a = 1
			break
	if a == 0:

		floating_ip = nc.floating_ips.create("ext-net")

		server1.add_floating_ip(floating_ip)

		f.write(floating_ip.ip + '\n')




#create_proxy(0)
