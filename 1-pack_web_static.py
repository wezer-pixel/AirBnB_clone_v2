#!/usr/bin/python3
from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    Create a compressed archive from the contents of the web_static folder.
    """
    # Create the versions folder if it doesn't exist
    if not os.path.exists("versions"):
        os.makedirs("versions")

    # Generate the archive filename (web_static_<year><month><day><hour><minute><second>.tgz)
    now = datetime.utcnow()
    archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second)

    # Create the archive command
    archive_command = "tar -cvzf versions/{} web_static".format(archive_name)

    # Run the archive command
    local_result = local(archive_command)

    # Check if the command was successful
    if local_result.failed:
        return None
    else:
        return os.path.join("versions", archive_name)

