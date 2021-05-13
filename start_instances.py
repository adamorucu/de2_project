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

cfg_file_path = os.getcwd() + '/prod-cfg.txt'
if os.path.isfile(cfg_file_path):
    userdata_prod = open(cfg_file_path)
else:
    sts.exit("prod-cfg.txt is not in current working directory")


cfg_file_path = os.getcwd() + '/dev-cfg.txt'
if os.path.isfile(cfg_file_path):
    userdata_dev = open(cfg_file_path)
else:
    sys.exit("dev-cfg.txt is not in current working directory")

secgroups = ['default']

print('Creating instances ...')
instance_prod = nova.servers.create(name="team16_prod"+str(identifier),
                                    image=image,
                                    flavor=flavor,
                                    key_name=key,
                                    userdata=userdata_prod,
                                    nics=nics,
                                    security_groups=secgroups)

instance_dev = nova.servers.create(name="team16_dev"+str(identifier),
                                    image=image,
                                    flavor=flavor,
                                    key_name=key,
                                    userdata=userdata_dev,
                                    nics=nics,
                                    security_groups=secgroups)

inst_status_prod = instance_prod.status
inst_status_dev = instance_dev.status

print("waiting for 10 secs..")
time.sleep(10)

while inst_status_prod == 'BUILD' or inst_status_dev == 'BUILD':
    print(f'Instance: {instance_prod.name} is in {inst_status_prod} state, sleeping for 5 secs more')
    print(f'Instance: {instance_dev.name} is in {inst_status_dev} state, sleeping for 5 secs more')
    time.sleep(5)
    instance_prod = nova.servers.get(instance_prod.id)
    inst_status_prod = instance_prod.status
    instance_dev = nova.servers.get(instance_dev.id)
    inst_status_dev = instance_dev.status

ip_address_prod = None
for network in instance_prod.networks[private_net]:
    if re.match('\d+\.\d+\.\d+\.\d+', network):
        ip_address_prod = network
        break
if ip_address_prod is None:
    raise RuntimeError('No IP address assigned')

ip_address_dev = None
for network in instance_dev.networks[private_net]:
    if re.match('\d+\.\d+\.\d+\.\d+', network):
        ip_address_dev = network
        break
if ip_address_dev is None:
    raise RuntimeError('No IP address assigned')

print(f'Instance: {instance_prod.name} is in {inst_status_prod} state ip address {ip_address_prod}')
print(f'Instance: {instance_dev.name} is in {inst_status_dev} state ip address {ip_address_dev}')
