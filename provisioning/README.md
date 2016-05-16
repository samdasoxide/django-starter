# Server provisioning

All three environments (`development`, `staging`, and `production`) are fully
provisioned and managed using the [Ansible](https://www.ansible.com/)
[playbooks](http://docs.ansible.com/ansible/playbooks.html) provided herein.

## Configuration

Most of the modifications that you will want to make to these playbooks should
be made in `provisioning/group_vars/all/vars.yml`. Here variables are defined
for the majority of configurable options for each role. Rather than modify a
role (where possible) you should look to modify a configuration variable.

There are also environment specific configuration files for overriding variables
based on the deployment environment:

 - `provisioning/group_vars/development.yml`
 - `provisioning/group_vars/staging.yml`
 - `provisioning/group_vars/production.yml`

### Inventory

The [inventory](http://docs.ansible.com/ansible/intro_inventory.html) of all
hosts managed by Ansible (`provisioning/hosts.ini`) should be updated to
include your staging and production hosts.

## Secrets

Secrets such as authentication tokens, private keys, database passwords etc.
are stored using
[`ansible-vault`](http://docs.ansible.com/ansible/playbooks_vault.html).

The vault password is currently set to "examplepassword". You should
[rekey](http://docs.ansible.com/ansible/playbooks_vault.html#rekeying-encrypted-files)
the vault using a secure password that you transfer out-of-band between
colaborators and ensure is never commited to version control.

To edit the secrets file create `.vault_pass.txt` with the password you
provided when rekeying the vault and execute the following command:

```
$ ansible-vault edit provisioning/group_vars/all/vault.yml --vault-password-file .vault_pass.txt
```

## Environments

This project has three supported environments (`development`, `staging`, and
`production`). `staging` and `production` are largely the same, however,
`development` differs slightly in that it is designed for use when running the
application using `./manage.py runserver` rather than
[uWSGI](http://uwsgi-docs.readthedocs.io/en/latest/) and
[nginx](https://www.nginx.com/).

An instance of any environment can be created locally using
`vagrant up development|staging|production`. This is especially useful when
testing configuration changes before running the playbooks against production
hosts. That said, there are some slight differences between running the
playbook against a vagrant machine and against a production machine. These are
handled by the `is_vagrant` ansible variable.

## Deployment user

A given project has a single deployment user. This user has the application
and environment specific settings injected into its `.pam-environment` file.
Configuration variables (e.g. `CFG_SERVER_NAME`) are thus available as
environment variables when logged in as the deployment user. These variables
are also injected into the uWSGI vassal's environment. For a full list of
these environment variables see `env_vars` in
`provisioning/group_vars/all/vars.yml`.

## Technology stack

The technology stack provided by this project is comprised of the following:

 - [uWSGI](http://uwsgi-docs.readthedocs.io/en/latest/) as the WSGI server
 - [nginx](https://www.nginx.com/) for serving static files and reverse
   proxying to `uwsgi`
 - [PostgreSQL](http://www.postgresql.org/) as the database backend
 - [Redis](http://redis.io/) as both a cache and a optionally a queue
 - [Postfix](http://www.postfix.org/) for email

Each of these either has a distinct role within the playbook or a 3rd party
`ansible-galaxy` role is used.

## Roles

A basic description of each role is provided below. For more detail please
read the `tasks/main.yml` of each individual role. The syntax is relatively
straightforward and should read like English to those with a sysadmin
background.

#### `provisioning/roles/base`

This role installs commonly needed `apt` packages and generally gets the
system to the bare minimum state for a Python oriented system.

#### `provisioning/roles/security`

This role handles locking down sshd and configuring the firewall. Further,
security hardening should be implemented here in the future.

#### `provisioning/roles/users`

This role handles the creation of users (*including the deployment user*)
and general user configuration. This includes configuring
[PAM](http://tldp.org/HOWTO/User-Authentication-HOWTO/x115.html) to load
the deployment users `.pam-environment` file.

Additionally if `sftp_users` is specified a special sftp-only group is
configured and a user account for each of `sftp_users` is created.

#### `provisioning/roles/nodejs`

This role installs nodejs 5.x to enable the execution of the frontend asset
pipeline.

#### `provisioning/roles/newrelic`

This role installs and configures `newrelic-sysmond` for sending system
metrics to the New Relic Server Monitoring service.

#### `provisioning/roles/backups`

This role configures automatic backups to Amazon S3 using
[`backup2l`](http://backup2l.sourceforge.net/) and
[`s3cmd`](http://s3tools.org/s3cmd).

It also configures automatic differential PostgreSQL backups.

#### `provisioning/roles/nginx`

This role installs and configures nginx. Optionally SSL certifcates from
[LetsEncrypt](https://letsencrypt.org/) can be installed and configured.

If so a strong DHE paramater is generated and secure SSL parameters
configured.

#### `provisioning/roles/uwsgi`

Installs and configures
[uWSGI](http://uwsgi-docs.readthedocs.io/en/latest/) and
[uWSGI Emperor](http://uwsgi-docs.readthedocs.io/en/latest/Emperor.html).

Vassals for individual applications are created in `/etc/uwsgi-emperor/vassals`
and can be restarted by logging in as the deployment user and executing the
alias `restart`.

#### `provisioning/roles/postfix`

Installs and configures postfix for sending email from the Django application.
This set-up is far from optimal and will need to be improved upon in the
future.

#### `provisioning/roles/django`

Finally, the Django role handles creating the relevant folders for logging,
installing related `apt` packages, installing requirements, etc. In addition
this role also installs and executes the frontend asset pipeline.

In both the `staging` and `production` environment the Django module also
handles the checking out of the repository (this isn't required in the
`development` environment as the repository is synchronized between your
host machine and the vagrant machine).

#### [`ANXS.postgresql`](https://galaxy.ansible.com/ANXS/postgresql/)

Used to install and configure [PostgreSQL](http://www.postgresql.org/) and
optionally [PostGIS](http://postgis.net/).

#### [`geerlingguy.redis`](https://galaxy.ansible.com/geerlingguy/redis/)

Used to install and configure redis. Very simple setup, only setting modified
is use of Redis append only file (`appendonly.aof`) as we often use Redis as a
queue and we want the durability.

#### [`thefinn93.letsencrypt`](https://galaxy.ansible.com/thefinn93/letsencrypt/)

Used to install the ~~letsencrypt~~
[Certbot](https://github.com/certbot/certbot) (the LetsEncrypt client) and
generate SSL certificates for the required domains.

Also creates a cronjob for the renewal of certificates.

## Provisioning live hosts

Live hosts (e.g. your live `staging` and `production` environments as opposed
to the equivalent vagrant environments) can be provisioned by executing the
following:

```bash
$ ansible-playbook -i provisioning/hosts.ini provisioning/{production,staging}.yml --vault-password-file .vault_pass.txt
```
