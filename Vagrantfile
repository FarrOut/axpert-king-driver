cd# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
config.vm.synced_folder ".", "/vagrant", disabled: true

  # The Attacker's battle station.
  config.vm.define "kali", primary: true do |subconfig|
  subconfig.vm.box = "kalilinux/rolling"
  subconfig.vm.network :private_network, ip: "10.0.3.10"
  subconfig.vm.synced_folder "./scripts/", "/home/vagrant/Scripts"
  subconfig.vm.provider "virtualbox" do |v|
    v.gui = false
    v.name = "axpert-king-hacklab"
    v.memory = 1024
    v.cpus = 1
    end
  end

  # The Mocked device
  config.vm.define "mock", autostart: true do |subconfig|
  subconfig.vm.box = "ubuntu/trusty64"
  subconfig.vm.network :private_network, ip: "10.0.3.11"
  subconfig.vm.synced_folder "./scripts/", "/home/vagrant/Scripts"
  subconfig.vm.provider "virtualbox" do |v|
    v.gui = false
    v.name = "axpert-king-mocked-device"
    v.memory = 1024
    v.cpus = 1
    v.customize ["modifyvm", :id, '--uart1', '0x3f8', 4, "--uartmode1", "tcpserver", 2023]
    end
  end

  # Execute automated deployment scripts
  config.vm.provision "ansible", after: :all do |ansible|
    ansible.compatibility_mode = "auto"
    ansible.verbose = "v"

    # Call the default playbook.
    ansible.playbook = "provisioning/site.yml"

    # Optionally filter tags (string or array of strings)
    ansible.tags = ["all"]

    # Set of inventory groups to be included in the auto-generated inventory file.
    ansible.groups = {
      "attackers" => ["kali"],
      "kali:vars" => {"ansible_sudo_pass" => "vagrant"}
    }

    # Limit target boxes to a subset.
    # ansible.limit = ""

    ansible.ask_become_pass = false

    # default password for vagrant boxes to allow sudo priviledges
    ansible.extra_vars = {
      ansible_sudo_pass: "vagrant"
    }
  end

end
