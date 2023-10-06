#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers,
using the function do_deploy
"""

import os
from fabric.api import env, put, run, sudo
from datetime import datetime

env.user = 'ubuntu'
env.key_filename = ['~/.ssh/id_rsa']
env.hosts = ['54.90.44.16', '54.157.176.138']


def do_deploy(archive_path):
    """ Deploys the archive to the web servers """

    if not os.path.exists(archive_path):
        return False

    try:
        # Get the filename without extension
        filename = os.path.basename(archive_path).split('.')[0]

        # Upload the archive to /tmp/ directory on the server
        put(archive_path, '/tmp/')

        # Create the destination directory on the server
        run('mkdir -p /data/web_static/releases/{}'.format(filename))

        # Uncompress the archive to the destination directory
        run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}'.format(filename, filename))

        # Delete the archive from the server
        run('rm /tmp/{}.tgz'.format(filename))

        # Move the contents of the archive to the appropriate location
        run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'
            .format(filename, filename))

        # Remove the old symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s /data/web_static/releases/{} /data/web_static/current'.format(filename))

        print('New version deployed!')
        return True

    except Exception as e:
        print('Deployment failed:', str(e))
        return False


if __name__ == '__main__':
    # Usage example: fab -f deploy_script.py do_deploy:archive_path=path/to/your/archive.tgz
    pass
