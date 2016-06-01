from __future__ import with_statement

import os
import uuid

from fabric.api import *

STAGING_HOST = 'staging.{{ cookiecutter.domain_name }}'
PRODUCTION_HOST = '{{ cookiecutter.domain_name }}'

env.roledefs = {
    'staging': ['{{ cookiecutter.project_slug }}@{}'.format(STAGING_HOST)],
    'production': ['{{ cookiecutter.project_slug }}@{}'.format(PRODUCTION_HOST)],
}
env.always_use_pty = False

PROJECT_NAME = '{{ cookiecutter.project_slug }}'
LOCAL_DB_NAME = '{{ cookiecutter.project_slug }}'
LOCAL_DB_USERNAME = 'postgres'
LOCAL_DUMP_PATH = '/tmp/'

REMOTE_DB_NAME = '$CFG_DB_NAME'
REMOTE_DB_USERNAME = '$CFG_DB_USER'
REMOTE_PROJECT_PATH = '$D/'
REMOTE_DUMP_PATH = '{}tmp/'.format(REMOTE_PROJECT_PATH)


def populate_remote_variables(input_string):
    """ Runs `echo $SOMEVAR`, with no terminal assigned, so that the server
    doesn't add extra bumf to stdout.
    """
    return run('echo {}'.format(input_string), pty=False)


def deploy():

    if env['host'] == STAGING_HOST:
        branch = 'staging'
    elif env['host'] == PRODUCTION_HOST:
        branch = 'master'
    else:
        raise RuntimeError("Unrecognised host.")

    run('git pull origin {}'.format(branch))
    run('pip install -r requirements/production.txt')
    run('dj migrate --noinput')
    run('dj collectstatic --noinput')

    # 'restart' should be an alias to a script that restarts the web server
    run('restart')

    if env['host'] == PRODUCTION_HOST:
        register_deployment('.')


def pull_data():
    if env['host'] == STAGING_HOST:
        # NOTE use absolute path to `pg_dump`, due to Postgres-Debian mismatches
        pg_dump_path = '/usr/bin/pg_dump'
    elif env['host'] == PRODUCTION_HOST:
        pg_dump_path = 'pg_dump'
    else:
        raise RuntimeError("Unrecognised host.")

    filename = "{}-{}.sql".format(PROJECT_NAME, uuid.uuid4())
    local_path = "{}{}".format(LOCAL_DUMP_PATH, filename)
    remote_path = "{}{}".format(REMOTE_DUMP_PATH, filename)
    local_db_backup_path = "{}vagrant-{}-{}.sql".format(LOCAL_DUMP_PATH, LOCAL_DB_NAME, uuid.uuid4())
    non_env_remote_path = populate_remote_variables(remote_path)

    run('{} -U{} -xOf {} {}'.format(pg_dump_path, REMOTE_DB_USERNAME, remote_path, REMOTE_DB_NAME))
    run('gzip {}'.format(remote_path))
    get("{}.gz".format(non_env_remote_path), "{}.gz".format(local_path))
    run('rm {}.gz'.format(remote_path))

    local('pg_dump -U{} -xOf {} {}'.format(LOCAL_DB_USERNAME, local_db_backup_path, LOCAL_DB_NAME))
    puts('Previous local database backed up to {}'.format(local_db_backup_path))

    local('dropdb -U{} {}'.format(LOCAL_DB_USERNAME, LOCAL_DB_NAME))
    local('createdb -U{} {}'.format(LOCAL_DB_USERNAME, LOCAL_DB_NAME))
    local('gunzip {}.gz'.format(local_path))
    local('psql -U{} {} -f {}'.format(LOCAL_DB_USERNAME, LOCAL_DB_NAME, local_path))
    local('rm {}'.format(local_path))


def pull_media():
    media_filename = "{}-{}-media.tar.gz".format(PROJECT_NAME, uuid.uuid4())
    local_media_dump = "{}{}".format(LOCAL_DUMP_PATH, media_filename)
    remote_media_dump = "{}{}".format(REMOTE_DUMP_PATH, media_filename)
    non_env_remote_media_dump = populate_remote_variables(remote_media_dump)

    run('tar cvf - media | gzip -1 >{}'.format(remote_media_dump))
    get('{}'.format(non_env_remote_media_dump), '{}'.format(local_media_dump))
    run('rm -f {}'.format(remote_media_dump))

    local('rm -rf media.old')
    local('mv media media.old || true')
    local('gzip -dc {} | tar xvf -'.format(local_media_dump))
    local('rm -f {}'.format(local_media_dump))


deploy_staging = roles('staging')(deploy)
deploy_production = roles('production')(deploy)

pull_staging_data = roles('staging')(pull_data)
pull_production_data = roles('production')(pull_data)

pull_staging_media = roles('staging')(pull_media)
pull_production_media = roles('production')(pull_media)


@roles('staging')
def pull_staging_content():
    pull_staging_data()
    pull_staging_media()


@roles('production')
def pull_production_content():
    pull_production_data()
    pull_production_media()


@runs_once
def register_deployment(git_path):
    with(lcd(git_path)):
        revision = local('git log -n 1 --pretty="format:%H"', capture=True)
        branch = local('git rev-parse --abbrev-ref HEAD', capture=True)
        local('curl https://intake.opbeat.com/api/v1/organizations/{org_id}/apps/{app_id}/releases/'
              ' -H "Authorization: Bearer {secret_token}"'
              ' -d rev="{rev}"'
              ' -d branch="{branch}"'
              ' -d status=completed'.format(
                  rev=revision,
                  branch=branch,
                  org_id=os.getenv('CFG_OPBEAT_ORGANIZATION_ID'),
                  app_id=os.getenv('CFG_OPBEAT_APP_ID'),
                  secret_token=os.getenv('CFG_OPBEAT_SECRET_TOKEN')))
