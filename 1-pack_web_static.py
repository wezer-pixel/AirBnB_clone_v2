from fabric.api import local
from datetime import datetime

def do_pack():
    """Packs the contents of web_static into a .tgz archive."""

    # Create the versions folder if it doesn't exist
    local("mkdir -p versions")

    # Generate the archive name with the current date and time
    now = datetime.now()
    archive_name = "web_static_{:04}{:02}{:02}{:02}{:02}{:02}.tgz".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second)

    # Create the .tgz archive
    result = local("tar -cvzf versions/{} web_static".format(archive_name))

    if result.succeeded:
        return "versions/{}".format(archive_name)
    else:
        return None
