# Project name

## Developer setup

 1. Ensure you have ansible installed

    ```bash
    $ sudo apt-get install software-properties-common
    $ sudo apt-add-repository ppa:ansible/ansible
    $ sudo apt-get update
    $ sudo apt-get install ansible
    ```

 2. Ensure you have vagrant installed

    ```bash
    $ wget https://releases.hashicorp.com/vagrant/1.8.1/vagrant_1.8.1_x86_64.deb
    $ sudo dpkg -i vagrant_1.8.1_x86_64.deb
    ```

 3. Ensure you have `vagrant-vbguest` installed.

    ```bash
    $ vagrant plugin install vagrant-vbguest
    ```

 5. Ensure you have nodejs installed (also installs `npm`)

    ```bash
    $ curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
    $ sudo apt-get install -y nodejs
    ```

    If you have trouble here you likely have a legacy version of nodejs
    installed this is solved by executing:

    ```bash
    $ sudo apt-get remove --purge nodejs npm
    ```

 4. Ensure you have the scss-lint ruby gem installed

    ```bash
    $ sudo gem install scss-lint
    ```

 6. Install the front end asset processing pipeline (including `gulp`) then
    process and install frontend dependencies

    ```bash
    $ sudo npm install -g gulp
    $ npm install
    $ gulp
    ```

 7. Bring the vagrant box up and start the development server

    ```bash
    $ vagrant up
    $ vagrant ssh
    $ cd project/project
    $ ./manage.py runserver 0.0.0.0:8000
    ```
