# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

    # Debian 8 box
    config.vm.box = "debian/jessie64"
    config.vm.synced_folder ".", "/vagrant", disabled: true

    # Modify virtualbox opts
    config.vm.provider :virtualbox do |vb|
        vb.customize ["modifyvm", :id, "--memory", "1024"]
    end

    # Forward ssh agent to share host credentials with the guest VM.
    config.ssh.forward_agent = true

    # Development machine
    config.vm.define "development" do |development|
        development.vm.network "forwarded_port", guest: 8000, host: 8000

        # Sync project folder
        development.vm.synced_folder ".", "/home/vagrant/project"

        development.vm.provision "ansible" do |ansible|
            ansible.playbook = "provisioning/development.yml"
            ansible.groups = {
                "development" => ["development"],
            }
            ansible.host_key_checking = false
            ansible.vault_password_file = ".vault_pass.txt"

            ansible.extra_vars = {
                ansible_ssh_user: 'vagrant',
                ansible_connection: 'ssh',
                ansible_ssh_args: '-o ForwardAgent=yes',
                is_vagrant: 'yes'
            }
        end
    end

    # Staging machine
    config.vm.define "staging" do |staging|
        staging.vm.network "forwarded_port", guest: 80, host: 9000

        staging.vm.provision "ansible" do |ansible|
            ansible.playbook = "provisioning/production.yml"
            ansible.groups = {
                "staging" => ["staging"],
            }
            ansible.host_key_checking = false
            ansible.vault_password_file = ".vault_pass.txt"

            ansible.extra_vars = {
                ansible_ssh_user: 'vagrant',
                ansible_connection: 'ssh',
                ansible_ssh_args: '-o ForwardAgent=yes',
                is_vagrant: 'yes'
            }
        end
    end

    # Production machine
    config.vm.define "production" do |production|
        production.vm.network "forwarded_port", guest: 80, host: 8080

        production.vm.provision "ansible" do |ansible|
            ansible.playbook = "provisioning/production.yml"
            ansible.groups = {
                "production" => ["production"],
            }
            ansible.host_key_checking = false
            ansible.vault_password_file = ".vault_pass.txt"

            ansible.extra_vars = {
                ansible_ssh_user: 'vagrant',
                ansible_connection: 'ssh',
                ansible_ssh_args: '-o ForwardAgent=yes',
                is_vagrant: 'yes'
            }
        end
    end
end
