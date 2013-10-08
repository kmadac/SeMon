__author__ = 'kmadac'
from fabric.api import *
import datetime

# the user to use for the remote commands
env.user = 'kmadac'
appname = 'SeMon'

SUPERVISOR_DIR = '/etc/supervisor/conf.d/'
NGINX_DIR = '/etc/nginx/sites-'


def pack():
    last_tag = local('git describe --tags', capture=True).strip()

    timestring = datetime.datetime.now().strftime('%y%m%d%H%M%S')

    new_file_lines = []
    with open("setup.py") as f:
        setup_contents = f.readlines()
        for line in setup_contents:
            if 'version' in line:
                new_file_lines.append("    version='{0}-{1}',\n".format(last_tag, timestring))
            else:
                new_file_lines.append(line)

    with open("setup.py", 'w') as f:
        f.writelines(new_file_lines)

    local('python setup.py sdist --formats=gztar', capture=False)
    local('~/PycharmProjects/VirtualEnvs/{0}/bin/pip freeze > requirements.txt'.format(appname), capture=True)


def bootstrap():
    with settings(warn_only=True):
        sudo('mkdir /tmp/{0}'.format(appname))

    sudo('aptitude install -y build-essential python-dev nginx python-pip uwsgi uwsgi-plugin-python supervisor')
    sudo('pip install virtualenv')
    sudo('mkdir -p /var/www/{0}'.format(appname))
    with cd('/var/www/{0}'.format(appname)):
        sudo('virtualenv env --no-site-packages')
        put('requirements.txt', 'requirements.txt'.format(appname), use_sudo=True)
        with prefix('source /var/www/{0}/env/bin/activate'.format(appname)):
            sudo('pip install -r requirements.txt')


def deploy():
    # figure out the release name and version
    dist = local('python setup.py --fullname', capture=True).strip()

    # upload the source tarball to the temporary folder on the server
    put('dist/%s.tar.gz' % dist, '/tmp/{0}.tar.gz'.format(appname))
    # create a place where we can unzip the tarball, then enter
    # that directory and unzip it
    with settings(warn_only=True):
        sudo('mkdir /tmp/{0}'.format(appname))
    with cd('/tmp/{0}'.format(appname)):
        sudo('tar xzf /tmp/{0}.tar.gz'.format(appname))
        # now setup the package with our virtual environment's
        # python interpreter
        sudo('cd /tmp/{0}/{1}; /var/www/{0}/env/bin/python setup.py install'.format(appname, dist))
    # now that all is set up, delete the folder again
    sudo('rm -rf /tmp/{0} /tmp/{0}.tar.gz'.format(appname))
    # and finally touch the .wsgi file so that mod_wsgi triggers
    # a reload of the application
    # run('touch /var/www/yourapplication.wsgi')
    put('fab-files/SeMon.ini', '/etc/uwsgi/apps-available/SeMon.ini', use_sudo=True)
    with settings(warn_only=True):
        sudo('ln -s /etc/uwsgi/apps-available/SeMon.ini /etc/uwsgi/apps-enabled/SeMon.ini')
    put('fab-files/wsgi.py', '/var/www/{0}/wsgi.py'.format(appname), use_sudo=True)
    sudo('service uwsgi restart')
