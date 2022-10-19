# ODP ANSIBLE API

This Projects aims at installing [ODP](https://www.opensourcedataplatform.com) clusters
managed by [Apache Ambari](https://ambari.apache.org/) using [Ansible](https://www.ansible.com/).

It uses Ambari's REST API to populate the database and install HDP Stack.

## Version Supports

- Ambari
  *  2.6.x
  *  2.7.x


- ODP Stacks

It's supports all ODP Stack than Ambari >2.6.x version supports.

You should adjust your VDF file to match the stack you need.
Look at an example on [ODPrepositories VDF definitions](https://www.opensourcedataplatform.com).


## Hosts - Cluster definition - Playbook file

Check the folder examples

Each services in "cluster_services" needs specific groups in your cluster file. Check examples/cluster.yaml

## Run

Bare metal:

`ansible-playbook -i hosts playbook.yml -u root -k myRootPassword`

Vagrant:

`ansible-playbook -i hosts playbook.yml -u vagrant -b`

## Requirements

- Ansible on your deployment machine
- JDK 1.8 installed on your hosts
- Ambari-server and Ambari-agent installed
- Mysql/MariaDB or PostgreSQL Database installed for Ambari Server Backend
- NTPD Installed
- Network Resolution
- Certificates in keystore/truststore jks if you want to enable SSL

