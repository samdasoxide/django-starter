# Django starter

Django starter is a **highly oppionated**
[cookiecutter](https://github.com/audreyr/cookiecutter) template for starting
new Django projects. It's what we use at [RocketPod](http://rocketpod.co.uk)
and [Mediae](http://mediae.org) and may be useful to others.

The project also includes [Wagtail](https://wagtail.io) support behind a flag.

## Technology stack

More information on the technology stack can be found in
`provisioning/README.md`, however, a few key points are listed below.

 - Virtualisation using vagrant and virtualbox
 - Provisioning using Ansible
 - Debian 8.4
 - nginx
 - uWSGI
 - redis
 - PostgreSQL
 - elasticsearch (for wagtail)
 - opbeat
 - etc.

## Usage

 1. Install cookiecutter

    ```bash
    pip install cookiecutter
    ```
 2. Download template and create a new project

    ```bash
    cookiecutter gh:rocketpod/django-starter
    ```
 3. Take a look around: there are a number of other variables to configure in
    `provisioning/group_vars/`.


## Contributing

Pull requests to fix bugs are always welcome. Pull requests implementing or
modifying functionality will be judged on an individual basis as this project
directly affects how we provision our infrastructure.

Some areas we are interested on improving (and where pull requests implementing
new functionality are likely to be merged upstream) are:

 - Security: Whilst basic hardening of `sshd` and a firewall are configured
   there is a lot of scope for improvement here.
 - Well supported Ansible Galaxy roles: More code is bad code. We'd rather not
   include many of the Ansible roles that we have custom written for this
   project. If suitable, well supported, Ansible roles crop up let us know!
 - Monitoring: Currently there is only support for New Relic system monitoring
   built in. A lightweight on-premises solution or solutions would be eagerly
   entertained.

## Licence and contributions

The project is licensed under the MIT Licence and includes major contributions
from other open source projects including
[Gulp Starter](https://github.com/vigetlabs/gulp-starter).
