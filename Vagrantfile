# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    # Base box to build off, and download URL for when it doesn't exist on the user's system already
    config.vm.box = "debian/jessie64"

    # Boot with a GUI so you can see the screen. (Default is headless)
    # config.vm.boot_mode = :gui

    # Forward a port from the guest to the host, which allows for outside
    # computers to access the VM, whereas host only networking does not.
    config.vm.network "forwarded_port", guest: 8000, host: 8000

    config.vm.provider :virtualbox do |vb|
        vb.customize ["modifyvm", :id, "--memory", "1024"]
    end


    # Share an additional folder to the guest VM. The first argument is
    # an identifier, the second is the path on the guest to mount the
    # folder, and the third is the path on the host to the actual folder.
    config.vm.synced_folder ".", "/home/vagrant/project"

    # Forward ssh agent to share host credentials with the guest VM.
    config.ssh.forward_agent = true

    # Provision the vagrant box with Ansible
    config.vm.provision "ansible" do |ansible|
        ansible.playbook = "provisioning/vagrant.yml"
        ansible.groups = {
            "development" => ["default"],
        }
        ansible.host_key_checking = false

        ansible.extra_vars = {
            ansible_ssh_user: 'vagrant',
            ansible_connection: 'ssh',
            ansible_ssh_args: '-o ForwardAgent=yes'
        }
    end
end
