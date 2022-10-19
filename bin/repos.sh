#!/bin/bash

#scp -i ~/.ssh/id_rsa.luc-data.com root@build.luc-data.com:/var/www/html/repos.tar.gz ~/ryba/ryba-repos/public/centos7/
#rm -rf ~/ryba/ryba-repos/public/centos7/dph_1.0.0.0-1/*
#tar -xzf ~/ryba/ryba-repos/public/centos7/repos.tar.gz -C ~/ryba/ryba-repos/public/centos7/dph_1.0.0.0-1/ --strip-component 1

 scp -i ~/.ssh/id_rsa.luc-data.com centos@ns3132122.ip-51-75-128.eu:/var/www/html/repos.tar.gz ~/ryba/ryba-repos/public/centos8/
 rm -rf ~/ryba/ryba-repos/public/centos8/dph_1.0.0.0-1/*
 tar -xzf ~/ryba/ryba-repos/public/centos8/repos.tar.gz -C ~/ryba/ryba-repos/public/centos8/dph_1.0.0.0-1/ --strip-component 1
