"""DROP MQTT API."""
from __future__ import annotations

import json
import logging
from typing import Any

_LOGGER = logging.getLogger(__name__)


class DropAPI:
    """Class for parsing MQTT data messages for DROP devices."""

    _data_cache: dict[str, Any] = {}

    def parse_drop_message(
        self, topic: str, payload: str | bytes, qos: int, retain: bool
    ) -> bool:
        """Parse an MQTT payload message and return True if any of the data has changed."""
        data_changed = False
        try:
            json_data = json.loads(payload)
            if isinstance(json_data, dict):
                for k, v in json_data.items():
                    if isinstance(k, str):
                        if k not in self._data_cache or self._data_cache[k] != v:
                            self._data_cache[k] = v
                            data_changed = True
            if data_changed:
                _LOGGER.debug("New data for %s: %s", topic, payload)
        except ValueError:
            _LOGGER.error("Invalid JSON (%s): %s", topic, payload)
            return False
        return data_changed

    # API mapping
    def battery(self) -> int | None:
        """Return battery percentage."""
        return self.get_int_val("battery")

    def current_flow_rate(self) -> float | None:
        """Return current flow rate in gpm."""
        return self.get_float_val("curFlow")

    def peak_flow_rate(self) -> float | None:
        """Return peak flow rate in gpm."""
        return self.get_float_val("peakFlow")

    def water_used_today(self) -> float | None:
        """Return water used today in gallons."""
        return self.get_float_val("usedToday")

    def average_water_used(self) -> float | None:
        """Return average water used in gallons."""
        return self.get_float_val("avgUsed")

    def capacity_remaining(self) -> float | None:
        """Return softener capacity remaining in gallons."""
        return self.get_float_val("capacity")

    def current_system_pressure(self) -> float | None:
        """Return current system pressure in PSI."""
        return self.get_float_val("psi")

    def high_system_pressure(self) -> int | None:
        """Return high system pressure today in PSI."""
        return self.get_int_val("psiHigh")

    def low_system_pressure(self) -> int | None:
        """Return low system pressure in PSI."""
        return self.get_int_val("psiLow")

    def temperature(self) -> float | None:
        """Return temperature."""
        return self.get_float_val("temp")

    def inlet_tds(self) -> int | None:
        """Return inlet TDS in PPM."""
        return self.get_int_val("tdsIn")

    def outlet_tds(self) -> int | None:
        """Return outlet TDS in PPM."""
        return self.get_int_val("tdsOut")

    def cart1(self) -> int | None:
        """Return cartridge 1 life remaining."""
        return self.get_int_val("cart1")

    def cart2(self) -> int | None:
        """Return cartridge 2 life remaining."""
        return self.get_int_val("cart2")

    def cart3(self) -> int | None:
        """Return cartridge 3 life remaining."""
        return self.get_int_val("cart3")

    def get_int_val(self, key: str) -> int | None:
        """Return the specified API value as an int or None if it is unknown."""
        if key in self._data_cache and self._data_cache[key] is not None:
            return int(self._data_cache[key])
        return None

    def get_float_val(self, key: str) -> float | None:
        """Return the specified API value as a float or None if it is unknown."""
        if key in self._data_cache and self._data_cache[key] is not None:
            return float(self._data_cache[key])
        return None
