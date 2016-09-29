# {{ cookiecutter.project_name }}

## Developer setup

 1. Ensure you have Ansible installed

    ```bash
    $ sudo apt-get install software-properties-common
    $ sudo apt-add-repository ppa:ansible/ansible
    $ sudo apt-get update
    $ sudo apt-get install ansible
    ```
 2. Install the required 3rd party Ansible playbooks

    ```bash
    $ sudo ansible-galaxy install -r provisioning/requirements.yml
    ```

 3. Ensure you have vagrant installed

    ```bash
    $ wget https://releases.hashicorp.com/vagrant/1.8.1/vagrant_1.8.1_x86_64.deb
    $ sudo dpkg -i vagrant_1.8.1_x86_64.deb
    ```

 4. Ensure you have `vagrant-vbguest` installed.

    ```bash
    $ vagrant plugin install vagrant-vbguest
    ```

 5. Ensure you have nodejs 5.x installed (also installs `npm`)

    ```bash
    $ curl -sL https://deb.nodesource.com/setup_5.x | sudo -E bash -
    $ sudo apt-get install -y nodejs
    ```

    If you have trouble here you likely have a legacy version of nodejs
    installed this is solved by executing before the above:

    ```bash
    $ sudo apt-get remove --purge nodejs npm
    ```

 6. Install the front end asset processing pipeline

    ```bash
    $ npm install
    ```

 7. Ensure that your ssh key  is registered with ssh-agent

    ```bash
    $ ssh-add -L
    ```

    If your key is not listed:

    ```bash
    $ ssh-add
    ```

 8. Ensure that you have the project's Ansible vault password stored in
    `.vault_pass.txt` (see `provisioning/README.md` for more information).

 9. Bring the vagrant box up and start the development server

    ```bash
    $ vagrant up development
    $ vagrant ssh development
    $ cd {{ cookiecutter.project_slug }}/
    $ ./manage.py runserver 0.0.0.0:8000
    ```
 10. Start the frontend asset processing pipeline. This will automatically open
    a browser window with [Browsersync](https://www.browsersync.io/) which
    automatically refreshes when changes are made to templates or static assets.

    ```bash
    $ npm start
    ```
