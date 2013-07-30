"""
Deployment toolbox for EC2
"""
import os
import time

import logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('fabfile')

from fabric.api import *
from fabric.contrib.files import *

TEST = False

project_git_url = 'git@github.com:JollyDream/picmobo-server.git'
project_dir = '/var/www/picmobo'
local_project_dir = '/home/han/projects/picmobo'

settings_file = None
db_values = None
home_dir = None
remove_home_dir = None

def development_db():
    pass

def create_production_database():
    """
    reset the postgres database. use with caution.
    """
    global db_values
    
    db_values['tempdb'] = 'tempdb'
    db_values['tempfil'] = '/tmp/tempfil'
    append('$HOME/.pgpass', '*:*:%(db_name)-s:%(db_user)-s:%(db_pass)-s' %(db_values))
    run('chmod 0600 $HOME/.pgpass')
    with settings(warn_only=True):
        sudo('echo "drop database %(db_name)-s;" | psql' %(db_values), user='postgres')
        sudo('echo "drop user %(db_user)-s;" | psql' %(db_values), user='postgres')
    sudo('echo "create user %(db_user)-s with password \'%(db_pass)-s\';" | psql' %(
        db_values), user='postgres')
    sudo('echo "drop database tempdb" | psql', 
         user='postgres')
    sudo('echo "create database %(tempdb)-s" | psql' %(db_values), user='postgres')
    sudo('pg_dump -Fc --no-owner %(tempdb)-s --file %(tempfil)-s' %(db_values), 
         user='postgres')
    sudo('echo "drop database %(tempdb)-s" | psql' %(db_values), 
         user='postgres')
    sudo('echo "create database %(db_name)-s with owner %(db_user)-s" | psql' %(
        db_values), user='postgres')
    sudo('rm %(tempfil)-s' %(db_values))
    sudo('psql -d %(db_name)-s -f /usr/share/postgresql/9.1/contrib/postgis-2.0/postgis.sql' %(db_values), user='postgres')
    sudo('psql -d %(db_name)-s -f /usr/share/postgresql/9.1/contrib/postgis-2.0/spatial_ref_sys.sql' %(db_values), user='postgres')
    sudo('psql -d %(db_name)-s -f /usr/share/postgresql/9.1/contrib/postgis-2.0/rtpostgis.sql' %(db_values), user='postgres')
    sudo('psql -d %(db_name)-s -f /usr/share/postgresql/9.1/contrib/postgis-2.0/topology.sql' %(db_values), user='postgres')
    
def install_latest_postgis():
    upload_template('%s/project/setupfiles/postgis.tar.gz' % (local_project_dir),
                    '%s/postgis.tar.gz' % (remote_home_dir))
    run('tar -xvf %s/postgis.tar.gz' % (remote_home_dir))
    run('cd %s/postgis-2.0.1 && ./configure --with-geosconfig=/opt/geos/bin/geos-config --with-gdalconfig=/opt/gdal/bin/gdal-config' % (remote_home_dir))
    run('cd %s/postgis-2.0.1 && make -j2' % (remote_home_dir))
    sudo('cd %s/postgis-2.0.1 && checkinstall' % (remote_home_dir))
    
def install_latest_geos():
    upload_template('%s/project/setupfiles/geos.tar.bz2' % (local_project_dir),
                    '%s/geos.tar.bz2' % (remote_home_dir))
    run('tar -xvf %s/geos.tar.bz2' % (remote_home_dir))
    run('cd %s/geos-3.3.5 && ./configure --prefix=/opt/geos --enable-python' % (remote_home_dir))
    run('cd %s/geos-3.3.5 && make -j2' % (remote_home_dir))
    sudo('cd %s/geos-3.3.5 && checkinstall' % (remote_home_dir))

def install_latest_gdal():
    upload_template('%s/project/setupfiles/gdal.tar.gz' % (local_project_dir),
                    '%s/gdal.tar.gz' % (remote_home_dir))
    run('tar -xvf %s/gdal.tar.gz' % (remote_home_dir))
    run('cd %s/gdal-1.9.1 && ./configure --prefix=/opt/gdal --with-geos=/opt/geos/bin/geos-config --with-python' % (remote_home_dir))
    run('cd %s/gdal-1.9.1 && make -j2' % (remote_home_dir))
    sudo('cd %s/gdal-1.9.1 && checkinstall' % (remote_home_dir))
    
def production_db():    
    global settings_file
    global db_values
    global home_dir
    global remote_home_dir
    
    home_dir = '/home/ubuntu'
    remote_home_dir = '/home/ubuntu'

    env.user="ubuntu"
    env.host_string = "ec2-23-20-233-73.compute-1.amazonaws.com"
    env.key_filename=os.environ['HOME'] + "/.ssh/picmobo.pem"
    
    db_values = {
        'db_master_user':'jollydream',
        'db_master_password':'dreamsofinnistrad',
        'db_user': 'picmobo',
        'db_pass': 'picmobo',
        'db_name': 'picmobo',
        'db_dump': '',
    }

def init_production_database_instance():
    sudo("""apt-get update""")
    sudo("""apt-get upgrade""")
    sudo("""aptitude install -y --quiet=2 ntp \
         gcc g++ \
         build-essential checkinstall libjson0-dev \
         postgresql-9.1 postgresql-client \
         python-psycopg2 \
         postgresql-server-dev-9.1 \
         libxml2 libxml2-dev \
         libgeos-c1 libgeos-dev \
         libproj0 libproj-dev \
         python-psycopg2 libdbd-pg-perl \
         sendmail \
         memcached \
         make \
         python2.7-dev \
         swig \
         """)

def setup_production_db():
    init_production_database_instance()
    install_latest_geos()
    install_latest_gdal()
    install_latest_postgis()
    create_production_database()
    
def development():
    global settings_file
    global db_values
    global home_dir
    global remote_home_dir
    
    home_dir = '/home/ubuntu'
    remote_home_dir = '/home/ubuntu'

    env.user="ubuntu"
    env.host_string = "107.22.162.59"
    env.key_filename=os.environ['HOME'] + "/.ssh/picmobo.pem"
    
    db_values = {
        'db_master_user':'jollydream',
        'db_master_password':'arcamdarien1234',
        'db_user': 'picmobo',
        'db_pass': 'picmobo',
        'db_name': 'picmobo',
        'db_host': 'picmobo-dev.cfky2ehdmykw.us-east-1.rds.amazonaws.com',
        'db_port': '3306',
        'project_dir': project_dir,
        'db_dump': '',
    }
    settings_file = 'development_settings.py'
    
def demo():
    global settings_file
    global db_values
    global home_dir
    global remote_home_dir

    home_dir = '/Users/jingchan'
    remote_home_dir = '/home/ubuntu'

    env.user="ubuntu"
    env.host_string = "ec2-184-72-211-115.compute-1.amazonaws.com"
    env.key_filename=os.environ['HOME'] + "/.ssh/picmobo.pem"

    db_values = {
        'db_master_user':'jollydream',
        'db_master_password':'arcamdarien1234',
        'db_user': 'picmobo',
        'db_pass': 'picmobo',
        'db_name': 'picmobo',
        'db_host': '127.0.0.1',
        'db_port': '5432',
        'project_dir': project_dir,
        'db_dump': '',
    }
    settings_file = 'demo_settings.py'

def production_webserver():
    global settings_file
    global db_values
    global home_dir
    global remote_home_dir
    
    home_dir = '/home/han'
    remote_home_dir = '/home/ubuntu'

    env.user="ubuntu"
    env.host_string = "ec2-50-17-76-91.compute-1.amazonaws.com"
    env.key_filename=os.environ['HOME'] + "/.ssh/picmobo.pem"
    
    settings_file = 'production_settings.py'

def test():
    global settings_file
    
    env.user="ubuntu"
    env.host_string = "ec2-107-22-99-34.compute-1.amazonaws.com"
    env.key_filename=os.environ['HOME'] + "/.ssh/picmobo-dev.pem"
    print env
    settings_file = 'development_settings.py'
    
def initialize():
    """
    initialize ebs volumes, etc. This is a destructive operation, use
    carefully
    """
    sudo('apt-get -y install lvm2')
    sudo('/sbin/modprobe dm_mod')
    append('/etc/modules', 'dm_mod', use_sudo=True)
    sudo('pvcreate /dev/sdf /dev/sdg')
    sudo('vgcreate vgMedia /dev/sdf')
    sudo('vgcreate vgPg /dev/sdg')
    sudo('lvcreate -n media -l 2559 vgMedia')
    sudo('lvcreate -n pgdata -l 2559 vgPg')
    sudo('echo "y\n" | mke2fs -j /dev/vgMedia/media')
    sudo('echo "y\n" | mke2fs -j /dev/vgPg/pgdata')
    sudo('mkdir -p /ebs/picmobo-media')
    append('/etc/fstab', '/dev/vgPg/pgdata /var/lib/postgres/8.4/main  auto    defaults    0 0', use_sudo=True)
    append('/etc/fstab', '/dev/vgMedia/media /ebs/picmobo-media    auto    defaults    0 0', use_sudo=True)
    sudo('mkdir -p /var/lib/postgres/8.4/main')
    sudo('mount /var/lib/postgres/8.4/main')
    sudo('mount /ebs/picmobo-media')

def install_packages():
    sudo("""apt-get update""")
    sudo("""aptitude install -y --quiet=2 ntp \
         apache2 libapache2-mod-wsgi apache2-mpm-worker \
         postgresql-client-9.1 \
         python-psycopg2 libdbd-pg-perl \
         python-mysqldb \
         libgeos-c1 libgeos-dev \
         libgdal1-1.7.0 \
         python-dev \
         sendmail \
         python-simplejson python-jinja2 python-crypto  python-setuptools \
         python-lxml \
         memcached python-memcache \
         python-imaging \
         git-core \
         varnish \
         lynx \
         """)
    
def init_production_webserver_instance():
    """
    prepare env.hosts to serve django sites

    expects an ubuntu lucid platform. handles installing system-level
    dependencies and configuring them for autostart

    """
    install_packages()
    sudo('a2enmod wsgi proxy_http status')
    append('/etc/apache2/conf.d/extendedstatus.conf', 'ExtendedStatus On', 
           use_sudo=True)
    comment('/etc/apache2/ports.conf', 'Listen 80', use_sudo=True)
    append('/etc/apache2/ports.conf', 'Listen 127.0.0.1:80', use_sudo=True)
    sudo('update-rc.d apache2 enable')
    sudo('/etc/init.d/apache2 restart')

    sudo('update-rc.d memcached enable')
    sudo('/etc/init.d/memcached restart')

    sudo('update-rc.d varnish enable')
    upload_template('varnish-default.vcl', 
                    '/etc/varnish/default.vcl',
                    context=env,
                    use_sudo=True
                   )
    sudo('chmod 0644 /etc/varnish/default.vcl')
    upload_template('varnish-default', 
                    '/etc/default/varnish',
                    use_sudo=True
                   )
    sudo('/etc/init.d/varnish restart')

def reset_postgres():
    """
    reset the postgres database. use with caution.
    """
    db_values['tempdb'] = 'tempdb'
    db_values['tempfil'] = '/tmp/tempfil'
    append('$HOME/.pgpass', '*:*:%(db_name)-s:%(db_user)-s:%(db_pass)-s' %(db_values))
    run('chmod 0600 $HOME/.pgpass')
    with settings(warn_only=True):
        sudo('echo "drop database %(db_name)-s;" | psql' %(db_values), user='postgres')
        sudo('echo "drop user %(db_user)-s;" | psql' %(db_values), user='postgres')
    sudo('echo "create user %(db_user)-s with password \'%(db_pass)-s\';" | psql' %(
        db_values), user='postgres')
    sudo('echo "drop database tempdb" | psql', 
         user='postgres')
    sudo('echo "create database %(tempdb)-s" | psql' %(db_values), user='postgres')
    sudo('pg_dump -Fc --no-owner %(tempdb)-s --file %(tempfil)-s' %(db_values), 
         user='postgres')
    sudo('echo "drop database %(tempdb)-s" | psql' %(db_values), 
         user='postgres')
    sudo('echo "create database %(db_name)-s with owner %(db_user)-s" | psql' %(
        db_values), user='postgres')
    sudo('rm %(tempfil)-s' %(db_values))

def reset_rds():
    mysql_cmd = "mysql --batch --user=%(db_master_user)-s --password=%(db_master_password)-s --host=%(db_host)-s --port=%(db_port)-s" % (db_values)
    db_values['mysql_cmd'] = mysql_cmd
    with settings(warn_only=True):
        sudo('echo "drop database %(db_name)-s;" | %(mysql_cmd)-s' % (db_values))
        sudo('echo "drop user %(db_user)-s;" | %(mysql_cmd)-s' % (db_values))
    sudo('echo "create user \'%(db_user)-s\' identified by \'%(db_pass)-s\';" | %(mysql_cmd)-s' % (db_values))
    sudo('echo "create database %(db_name)-s CHARACTER SET utf8;" | %(mysql_cmd)-s' % (db_values))
    sudo('echo "grant all on %(db_name)-s.* to \'%(db_user)-s\';" | %(mysql_cmd)-s' % (db_values))
    
def load_sql():
    db_values['tempdb'] = 'tempdb'
    db_values['tempfil'] = '/tmp/tempfil'
    sudo('psql --quiet %(tempdb)-s < %(project_dir)-s/sql/%(db_dump)-s' %(db_values),
         user='postgres')
    run('pg_restore -O -h %(db_host)-s -d %(db_name)-s -U%(db_user)-s %(tempfil)-s' %(
        db_values))

def init_log():
    run('cd %s && touch test.log' %(project_dir))
    run('chmod 777 %s/test.log' %(project_dir))
    run('cd %s && touch queries.log' %(project_dir))
    run('chmod 777 %s/queries.log' %(project_dir))
    
def git_deploy_production():
    sudo('rm -rf %s' %(project_dir))
    sudo('mkdir %s' %(project_dir))
    sudo('chown %s %s' %(env.user, project_dir))
    run('git clone %s %s' % (project_git_url, project_dir))
    run('cd %s && python bootstrap.py' %(project_dir))
    init_log()
    git_update_production()

def git_deploy_development():
    sudo('rm -rf %s' %(project_dir))
    sudo('mkdir %s' %(project_dir))
    sudo('chown %s %s' %(env.user, project_dir))
    run('git clone %s %s' % (project_git_url, project_dir))
    run('cd %s && python bootstrap.py' %(project_dir))
    init_log()
    git_update_development()

def git_deploy_demo():
    sudo('rm -rf %s' %(project_dir))
    sudo('mkdir %s' %(project_dir))
    sudo('chown %s %s' %(env.user, project_dir))
    run('git clone %s %s' % (project_git_url, project_dir))
    run('cd %s && python bootstrap.py' %(project_dir))
    reset_postgres()
    init_log()
    git_update_development()

def git_update_production():
    """
    update the site via git
    """
    run('cd %s && git pull origin master' %(project_dir))
    run('cd %s && bin/buildout' %(project_dir))
    upload_template(settings_file, 
                    '%s/project/local_settings.py' %(project_dir))
        
    run('chmod 0644 %s/project/local_settings.py' %(project_dir))

    upload_template('apache2-default.conf',
                    '/etc/apache2/sites-available/default',
                    context = {'project_dir': project_dir, },
                    use_sudo=True
                   )
    sudo('/etc/init.d/apache2 stop')
    sudo("""
         touch /var/log/apache2/picmobo-wsgi.log
         chown www-data /var/log/apache2/picmobo-wsgi.log
         """
        )
    run('cd %s && bin/django syncdb' %(project_dir,))
    run('cd %s && bin/django migrate' %(project_dir,))
    sudo('/etc/init.d/apache2 start')
    
def git_update_development():
    """
    update the site via git
    """
    run('cd %s && git pull origin master' %(project_dir))
    run('cd %s && bin/buildout' %(project_dir))
    upload_template(settings_file, 
                    '%s/project/local_settings.py' %(project_dir))
        
    run('chmod 0644 %s/project/local_settings.py' %(project_dir))

    upload_template('apache2-default.conf',
                    '/etc/apache2/sites-available/default',
                    context = {'project_dir': project_dir, },
                    use_sudo=True
                   )
    sudo('/etc/init.d/apache2 stop')
    sudo("""
         touch /var/log/apache2/picmobo-wsgi.log
         chown www-data /var/log/apache2/picmobo-wsgi.log
         """
        )
    run('cd %s && bin/django syncdb' %(project_dir,))
    run('cd %s && bin/django migrate' %(project_dir,))
    sudo('/etc/init.d/apache2 start')

def upload_production_ssh_keys():
    upload_template('%s/.ssh/picmobo_server' % (home_dir),
                    '%s/.ssh/id_rsa' % (remote_home_dir))
    upload_template('%s/.ssh/picmobo_server.pub' % (home_dir),
                    '%s/.ssh/id_rsa.pub' % (remote_home_dir))
    run('chmod 600 %s/.ssh/id_rsa' % (remote_home_dir))

def full_deploy_production():
    """
    staged full deployment, from scratch.
    """
    upload_production_ssh_keys()
    init_production_webserver_instance()
    git_deploy_production()

def full_deploy_demo():
    """
    staged full demo server, from scratch.
    """
    initialize()
    upload_ssh_keys()
    prepare()
    git_deploy_demo()