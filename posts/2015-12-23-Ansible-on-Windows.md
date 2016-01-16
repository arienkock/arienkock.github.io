---
title: Ansible on Windows
teaser: A little Getting Started guide
---


When I wanted to try out Ansible on my dev machine I felt like booting a sufficiently large EC2 instance was a bit of a waste. So, I used Vagrant. Vagrant makes using VirtualBox directly seem like a terrible chore. So this is what you need to start playing around with Ansible on Windows.

## Install Vagrant
Requires VirtualBox to run as the default provider on Windows.

## Create two VM's
One Ansible host (let's call it VM1) and one Ansible target (let's call it VM2). The separate target machine is useful, because your Ansible playbooks will surely wreck the config at some point or cause side-effects that cause your commands to have different outcomes than you would have with a correct playbook. Now you can tear down VM2 whenever you need to and apply the playbook to a fresh machine. To keep the environment lite (low memory usage), consider using one of these [minimal boxes](https://atlas.hashicorp.com/minimal) for the host VM1 and maybe even the target (depending on your needs). Run the following command twice in separate directories.

    vagrant init minimal/trusty64

## Install Ansible on VM1
Read [the documentation for your OS](http://docs.ansible.com/ansible/intro_installation.html).

## Configure a static IP address for VM2
You don't want to have to update your Ansible configuration (the inventory file) each time your Ansible target gets a new IP address. So, somewhere in your `Vagrantfile` set something along the lines of:

    config.vm.network "private_network", ip: "192.168.33.10"

Now start both VM's running `vagrant up` in the two directories.

## Setup password-less authentication between Ansible host and target
Since all Ansible commands run over SSH by default and Vagrant uses private_key authentication, the host has to be known and trusted on the target machine. Since (by default, anyway) there is no password for VM2 you can't use `ssh-copy-id`. You can perform this step in several ways, but this is the way I did it:

On VM1 run `ssh-keygen` to generate a key pair (use default values for every prompt). Copy the resulting `/home/vagrant/.ssh/id_rsa.pub` public key file to the `/vagrant/` directory on VM1. 

Since Vagrant automounts this directory to the same directory your Vagrantfile is in, you now have access to the `id_rsa.pub` file on your Windows machine. Now copy that file to VM2's directory which is also automounted giving you access to the file inside VM2. 

Now, append the contents of the file to the `authorized_keys` file running `cat id_rsa.pub >> ~/.ssh/authorized_keys`. Now your identity on VM1 is known and trusted on VM2.

## Try it out
Create the inventory file on VM1 contianing only VM2's IP address: `sudo sh -c "echo 192.168.33.10 > /etc/ansible/hosts"`. Now, run your first ad-hoc play (don't worry about the terminology if you're just getting started): `ansible all -m setup`. If you're having connection issues, make sure the IP address is pointing to VM2's IP address on your windows machine (the IP addresses in the commands on this page are just examples).
