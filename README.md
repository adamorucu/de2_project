# GitHub stargazer prediction

Use `startinstances.py` to setup two instances - for development and production. Then, configure them using Ansible and `configuration.yml`.

## Steps needed to start a ray cluster
```
ssh -i ~/keys/key appuser@192.168.2.30
ray start --head
# copy output
exit
# paste into dev_server/configuration.yml
python3 scale_dev.py
# copy slaves ip address 192.168.2.195
sudo vim /etc/ansible/hosts
# make the changes
# ssh -i ~/keys/key appuser@192.168.2.195
# inside dev_server do the following
ansible-playbook configuration.yml --private-key=/home/ubuntu/keys/key -l slaveserver
```
## Some of the steps to set up production server
```
ssh development
ssh-keygen
copy key to prodserver > authoresize_keys
create git hook
chmod +x hooks/post-receive
# in dev /star_predict
git remote add production appuser@192.168.2.148:/home/appuser/star_predict
```
