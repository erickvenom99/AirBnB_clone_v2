#!/usr/bin/python3
"""Fabric script that generates a .tgz
    archive from the contents of the web_static
"""
import os
from datetime import datetime
from fabric.api import env, local, run, put

env.user = 'ubuntu'
env.hosts = ['54.224.41.162', '54.167.91.167']


def do_pack():
    """generate tgz"""
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    os.makedirs("versions", exist_ok=True)
    archive_file = "versions/web_static_{}.tgz".format(date)
    result_file = local("tar -cvzf {} web_static".format(archive_file))
    if result_file.succeeded:
        return archive_file
    else:
        return None


def do_deploy(archive_path):
    """Distributes an archive to web servers."""
    if not os.path.isfile(archive_path):
        return False
    try:
        put(archive_path, '/tmp/')
        file_name = os.path.basename(archive_path).split(".")[0]
        path = "data/web_static/releases"
        run('mkdir -p {}{}/'.format(path, file_name))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, path, file_name))
        run('rm /tmp/{}'.format(file_name))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, file_name))
        run('rm -rf {}{}/web_static'.format(path, file_name))
        run('rm -rf /data/web_static/current')
        run('ln -s {}/ /data/web_static/current'.format(path, file_name))
        return True
    except Exception as e:
        print(e)
        return False
