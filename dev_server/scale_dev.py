# Script that will creat instances just like start-instances. (maybe with ability to specify number of sslaves)
# You should also input the IP and port for ray
import time, os, sys,  random
import inspect
from os import environ as env

from  novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session

flavor = "ssc.medium" 
private_net = "UPPMAX 2020/1-3 Internal IPv4 Network"
floating_ip_pool_name = None
floating_ip = None
image_name = "Ubuntu 20.04 - 2021.03.23"
key = "project"

identifier = random.randint(1000,9999)

loader = loading.get_plugin_loader('password')

auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                project_domain_id=env['OS_PROJECT_DOMAIN_ID'],
                                #project_id=env['OS_PROJECT_ID'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
print("User authorization completed.")

image = nova.glance.find_image(image_name)
flavor = nova.flavors.find(name=flavor)

if private_net != None:
    net = nova.neutron.find_network(private_net)
    nics = [{'net-id': net.id}]
else:
    sys.exit("private-net not defined")

cfg_file_path = os.getcwd() + '/slave-cfg.txt'
if os.path.isfile(cfg_file_path):
    userdata_prod = open(cfg_file_path)
else:
    sts.exit("slave-cfg.txt is not in current working directory")

secgroups = ['default']

print('Creating instances ...')
instance_slave = nova.servers.create(name="team16_slave"+str(identifier),
                                    image=image,
                                    flavor=flavor,
                                    key_name=key,
                                    userdata=userdata_prod,
                                    nics=nics,
                                    security_groups=secgroups)

inst_status_slave = instance_slave.status

print("waiting for 10 secs..")
time.sleep(10)

while inst_status_slave == 'BUILD':
    print(f'Instance: {instance_slave.name} is in {inst_status_slave} state, sleeping for 5 secs more')
    time.sleep(5)
    instance_slave = nova.servers.get(instance_slave.id)
    inst_status_slave = instance_slave.status

ip_address_slave = None
for network in instance_slave.networks[private_net]:
    if re.match('\d+\.\d+\.\d+\.\d+', network):
        ip_address_slave = network
        break
if ip_address_slave is None:
    raise RuntimeError('No IP address assigned')

print(f'Instance: {instance_slave.name} is in {inst_status_slave} state ip address {ip_address_slave}')
