"""DROP Discovery."""
from __future__ import annotations

import json
import logging

_LOGGER = logging.getLogger(__name__)

KEY_DEVICE_TYPE = "devType"
KEY_DEVICE_DESCRIPTION = "devDesc"
KEY_DEVICE_NAME = "name"


class DropDiscovery:
    """Class for parsing MQTT discovery messages for DROP devices."""

    def __init__(self, domain: str) -> None:
        """Initialize."""
        self._domain = domain
        self._hub_id = ""
        self._device_id = ""
        self._device_type = ""
        self._device_desc = ""
        self._name = ""
        self._owner_id = ""
        self._data_topic = ""
        self._command_topic = ""

    async def parse_discovery(self, discovery_topic: str, payload: str | bytes) -> bool:
        """Parse an MQTT discovery message and return True if successful."""
        try:
            json_data = json.loads(payload)
        except ValueError:
            _LOGGER.error(
                "Invalid DROP MQTT discovery payload on %s: %s",
                discovery_topic,
                payload,
            )
            return False

        # Extract the DROP hub ID and DROP device ID from the MQTT topic.
        topic_elements = discovery_topic.split("/")
        if not (
            topic_elements[2].startswith("DROP-") and topic_elements[3].isnumeric()
        ):
            return False
        self._hub_id = topic_elements[2]
        self._device_id = topic_elements[3]

        # Discovery data must include the DROP device type and name.
        if (
            KEY_DEVICE_TYPE in json_data
            and KEY_DEVICE_DESCRIPTION in json_data
            and KEY_DEVICE_NAME in json_data
        ):
            self._device_type = json_data[KEY_DEVICE_TYPE]
            self._device_desc = json_data[KEY_DEVICE_DESCRIPTION]
            self._name = json_data[KEY_DEVICE_NAME]
        else:
            _LOGGER.error(
                "Incomplete MQTT discovery payload on %s: %s", discovery_topic, payload
            )
            return False

        self._data_topic = f"{self._domain}/{self._hub_id}/data/{self._device_id}/#"
        self._command_topic = f"{self._domain}/{self._hub_id}/cmd/{self._device_id}"
        self._owner_id = f"{self._hub_id}_255"  # Hub has static device ID
        _LOGGER.debug("MQTT discovery on %s: %s", discovery_topic, payload)
        return True

    @property
    def hub_id(self):
        """Return DROP Hub ID."""
        return self._hub_id

    @property
    def device_id(self):
        """Return DROP device ID."""
        return self._device_id

    @property
    def name(self):
        """Return device name."""
        return self._name

    @property
    def device_type(self):
        """Return device type."""
        return self._device_type

    @property
    def device_desc(self):
        """Return device description."""
        return self._device_desc

    @property
    def data_topic(self):
        """Return MQTT data topic."""
        return self._data_topic

    @property
    def command_topic(self):
        """Return MQTT command topic."""
        return self._command_topic

    @property
    def owner_id(self):
        """Return device owner ID."""
        return self._owner_id
