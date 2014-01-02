import time
import string
import logging
from time import sleep, asctime

from keystoneclient.v2_0 import client as ksclient

from neutronclient.v2_0 import client as neclient

from novaclient.v1_1 import client as nclient
import novaclient.exceptions as nova_exc


logging.basicConfig(level=logging.INFO)

#logging.basicConfig(level=logging.DEBUG)



KEYSTONE_URL='https://openstack.nctu.edu.tw/keystone/v2.0'


username = ['0256547','0256081','0256017','0156153']

password = ['03067','2','persevere80419@gmail.com','swluo@cs.nctu.edu.tw']

tenant_name=['CloudOS2013_0256547','CloudOS2013_0256081','CloudOS2013_0256017','CloudOS2013_0156153']


def delete_all_vm(now):

        ne=neclient.Client(auth_url=KEYSTONE_URL, username = username[now], tenant_name = tenant_name[now], password = password[now], insecure = True)
        nc=nclient.Client(auth_url=KEYSTONE_URL, username = username[now], api_key = password[now], project_id=tenant_name[now],service_type='compute', insecure = True)
        servers=nc.servers.list()
        num=len(servers)
        i=0
        while i<num:
                if string.split(servers[i].name,'_')[0] == 'VM':
                        print 'Delete %s'%servers[i].name
                        try:
                                nc.servers.delete(servers[i].id)
                        except:
                                pass
                i=i+1
def delete_network(now): 
        
        ne=neclient.Client(auth_url=KEYSTONE_URL, username = username[now], tenant_name = tenant_name[now], password = password[now], insecure = True)
        nc=nclient.Client(auth_url=KEYSTONE_URL, username = username[now], api_key = password[now], project_id=tenant_name[now],service_type='compute', insecure = True)

        router_name = username[now] + '_router'
        network_name = username[now] + '_network'
        subnet_name = username[now] + '_subnet'
        if ne.list_networks(name = network_name):
                try:
                        router1 = ne.list_routers(name = router_name)
                        router1_id = router1['routers'][0]['id']
                        sub = ne.list_subnets(name = subnet_name)
                        sub_id = sub['subnets'][0]['id']
                        ne.remove_interface_router(router1_id,{'subnet_id': sub_id})
                        ne.delete_router(router1_id)
                        ne.delete_network(ne.list_networks(name= network_name)['networks'][0]['id'])
                except:
                        pass

delete_all_vm(2)
delete_network(2)

      
