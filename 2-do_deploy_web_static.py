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
    archive_path = "versions/web_static_{}.tgz".format(date)
    result_file = local("tar -cvzf {} web_static".format(archive_path))
    if result_file.succeeded:
        return archive_file
    else:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to web servers.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ on the remote server
        put(archive_path, '/tmp/')
        # Extract the archive to the release directory
        file_name = os.path.basename(archive_path).split(".")[0]
        file_path = f"/data/web_static/releases/{file_name}"
        run(f'mkdir -p {file_path}')
        run(f'tar -xzf /tmp/{file_name}.tgz -C {file_path}')
        # Remove the uploaded archive
        run(f'rm /tmp/{file_name}.tgz')
        # Update symbolic links
        current_path = '/data/web_static/current'
        run(f'rm -rf {current_path}')
        run(f'ln -s {file_path} {current_path}')
        return True
    except Exception as e:
        print(e)
        return False
