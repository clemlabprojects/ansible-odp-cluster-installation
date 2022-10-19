# -*- mode: ruby -*-
# vi: set ft=ruby :

#box = "centos/7"
#box = "ubuntu/bionic64"
# box = "centos120/7"
# box = "centos/8"
box = "openlogic/rockylinux-8"



if Vagrant::VERSION == '1.8.5'
  ui = Vagrant::UI::Colored.new
  ui.error 'Unsupported Vagrant Version: 1.8.5'
  ui.error 'Version 1.8.5 introduced an SSH key permissions bug, downgrade until version 1.8.6'
  ui.error ''
end


Vagrant.configure("2") do |config|
  config.vm.synced_folder ".", "/vagrant", disabled: true
  config.ssh.insert_key = false
  config.vm.box_check_update = false
  # config.vm.box_version = '1703.01'
  # config.vm.box_version = '20190914.0.0'

# uncomment to use official centos
# config.vm.box_version = '1902.01'
  config.vm.provider :virtualbox do |vb|
      config.vbguest.no_remote = true
      config.vbguest.auto_update = false
  # config.vm.provider :libvirt do |libvirt|
  #   libvirt.storage_pool_name="vagrant-libvirt"
  #   libvirt.driver = "kvm"
  #   libvirt.uri="qemu:///system"
  end
  # config.vm.define :ldap01 do |node|
  #   node.vm.box = box
  #   node.vm.network :private_network, ip: "10.10.10.19"
  #   node.vm.network :forwarded_port, guest: 22, host: 24011, auto_correct: true
  #   # node.vm.provider "libvirt" do |d|
  #   node.vm.provider "libvirt" do |d|
  #     d.memory = 2048
  #   end
  # end
  config.vm.define :admin01 do |node|
    node.vm.box = box
    node.vm.network :private_network, ip: "10.10.10.19"
    node.vm.network :forwarded_port, guest: 22, host: 24011, auto_correct: true
    node.vm.provider "virtualbox" do |d|
      d.memory = 2048
      d.cpus = 2    # node.vm.provider "libvirt" do |d|
    #   d.memory = 1024
    #   d.cpus = 2
    end
  end
  config.vm.define :admin02 do |node|
    node.vm.box = box
    node.vm.network :private_network, ip: "10.10.10.20"
    node.vm.network :forwarded_port, guest: 22, host: 24011, auto_correct: true
    node.vm.provider "virtualbox" do |d|
      d.memory = 2048
      d.cpus = 2
    # node.vm.provider "libvirt" do |d|
    #   d.memory = 1024
    #   d.cpus = 2
  
    end
  end

  config.vm.define :master01 do |node|
    node.vm.box = box
    node.vm.network :private_network, ip: "10.10.10.11"
    node.vm.network :forwarded_port, guest: 22, host: 24011, auto_correct: true
    node.vm.provider "virtualbox" do |d|
      d.memory = 12288
      d.cpus = 4
    end
  end
  config.vm.define :master02 do |node|
    node.vm.box = box
    node.vm.network :private_network, ip: "10.10.10.12"
    node.vm.network :forwarded_port, guest: 22, host: 24012, auto_correct: true
    node.vm.provider "virtualbox" do |d|
      d.memory = 4096
      d.cpus = 2
    end
  end
  config.vm.define :master03 do |node|
    node.vm.box = box
    node.vm.network :private_network, ip: "10.10.10.13"
    node.vm.network :forwarded_port, guest: 22, host: 24013, auto_correct: true
    node.vm.provider "virtualbox" do |d|
      d.memory = 4096
      d.cpus = 2
    end
  end
  config.vm.define :edge01 do |node|
    node.vm.box = box
    node.vm.network :private_network, ip: "10.10.10.14"
    node.vm.network :forwarded_port, guest: 22, host: 24014, auto_correct: true
    node.vm.provider "virtualbox" do |d|
      d.memory = 2048
    end
  end
  config.vm.define :worker01 do |node|
    node.vm.box = box
    node.vm.network :private_network, ip: "10.10.10.16"
    node.vm.network :forwarded_port, guest: 22, host: 24015, auto_correct: true
    node.vm.provider "virtualbox" do |d|
      d.memory = 4096
      d.cpus = 1
    end
  end
  config.vm.define :worker02 do |node|
    node.vm.box = box
    node.vm.network :private_network, ip: "10.10.10.17"
    node.vm.network :forwarded_port, guest: 22, host: 24016, auto_correct: true
    node.vm.provider "virtualbox" do |d|
      d.memory = 4096
      d.cpus = 1
    end
  end
  config.vm.define :worker03 do |node|
    node.vm.box = box
    node.vm.network :private_network, ip: "10.10.10.18"
    node.vm.network :forwarded_port, guest: 22, host: 24017, auto_correct: true
    node.vm.provider "virtualbox" do |d|
      d.memory = 4096
      d.cpus = 1
    end
  end
end

