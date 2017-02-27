"""
Sensor to check the status of a Minecraft server.
"""
import logging
import json
import requests
from homeassistant.helpers.entity import Entity
ATTR_PING = 'Ping'
ATTR_USERS = 'Users'
ATTR_MOTD = 'MOTD'
ATTR_VERSION = 'Version'
ATTR_LATEST = 'Latest Version'
ICON = 'mdi:minecraft'
REQUIREMENTS = ['mcstatus==2.1']

# Get Latest Server Version


def j_get(url):
    return json.loads(requests.get(url).content)

try:
    r = j_get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
except:
    time.sleep(30)  # wait for machine to boot and connect to internet
    r = j_get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
latest_version = r["latest"]["release"]

# pylint: disable=unused-argument


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Minecraft server platform."""
    from mcstatus import MinecraftServer as mcserver
    logger = logging.getLogger(__name__)

    server = config.get('server')
    name = config.get('name')
    latest_version = r["latest"]["snapshot"]

    if server is None:
        logger.error('No server specified')
        return False
    elif name is None:
        logger.error('No name specified')
        return False

    add_devices([
        MCServerSensor(server, name, mcserver)
    ])


class MCServerSensor(Entity):
    """A class for the Minecraft server."""

    # pylint: disable=abstract-method
    def __init__(self, server, name, mcserver):
        """Initialize the sensor."""
        self._mcserver = mcserver
        self._server = server
        self._name = name
        self.update()

    @property
    def name(self):
        """Return the name of the server."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    # pylint: disable=no-member
    def update(self):
        """Update device state."""
        status = self._mcserver.lookup(self._server).status()
        query = self._mcserver.lookup(self._server).query()
        self._state = str(status.players.online) + '/' + str(status.players.max}
        self._ping = status.latency
        self._users = query.players.names
        self._motd = query.motd
        self._version = query.version
        self._latest = latest_version

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
    return {
       ATTR_PING: self._ping,
       ATTR_USERS: self._users,
       ATTR_MOTD: self._motd,
       ATTR_VERSION: self._version,
       ATTR_LATEST: self._latest
    }

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON
