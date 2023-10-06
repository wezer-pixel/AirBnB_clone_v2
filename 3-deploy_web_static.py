#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.
import os.path
from datetime import datetime
from fabric.api import env, local, put, run

# Define the IP addresses of the remote hosts
env.hosts = ["54.90.44.16", "54.157.176.138"]

# Function to create a tar gzipped archive of the directory "web_static"
def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow()
    
    # Define the filename for the archive using a timestamp
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

    # Create the "versions" directory if it doesn't exist
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None

     # Create the tar gzipped archive
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None

     # Return the path to the created archive
    return file


def do_deploy(archive_path):
    """Distributes an archive to a web server.
    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    return True


def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
