#!/usr/bin/python3
"""Fabric script that generates a .tgz
    archive from the contents of the web_static
"""
import os
from datetime import datetime
from fabric.api import local


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
