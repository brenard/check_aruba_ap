""" SNMP Client """

import logging
import string

from easysnmp import Session
from easysnmp.exceptions import EasySNMPNoSuchNameError

log = logging.getLogger(__name__)

PROFILES = {
    "instant_node": {
        "ap_oids": {
            "ip": "iso.3.6.1.4.1.14823.2.3.3.1.2.1.1.3",
            "name": "iso.3.6.1.4.1.14823.2.3.3.1.2.1.1.2",
            "serial": "iso.3.6.1.4.1.14823.2.3.3.1.2.1.1.4",
            "uptime": "iso.3.6.1.4.1.14823.2.3.3.1.2.1.1.9",
            "status": "iso.3.6.1.4.1.14823.2.3.3.1.2.1.1.11",
            "cpu_usage": "iso.3.6.1.4.1.14823.2.3.3.1.2.1.1.7",
            "free_mem": "iso.3.6.1.4.1.14823.2.3.3.1.2.1.1.8",
            "total_mem": "iso.3.6.1.4.1.14823.2.3.3.1.2.1.1.10",
        },
        "radio_oids": {
            "mac": "iso.3.6.1.4.1.14823.2.3.3.1.2.2.1.3",
            "noise": "iso.3.6.1.4.1.14823.2.3.3.1.2.2.1.6",
            "usage": "iso.3.6.1.4.1.14823.2.3.3.1.2.2.1.8",
            "tx_total_frames": "iso.3.6.1.4.1.14823.2.3.3.1.2.2.1.9",
            "tx_total_bytes": "iso.3.6.1.4.1.14823.2.3.3.1.2.2.1.12",
            "tx_dropped_frames": "iso.3.6.1.4.1.14823.2.3.3.1.2.2.1.13",
            "rx_total_frames": "iso.3.6.1.4.1.14823.2.3.3.1.2.2.1.14",
            "rx_total_bytes": "iso.3.6.1.4.1.14823.2.3.3.1.2.2.1.16",
            "rx_bad_frames": "iso.3.6.1.4.1.14823.2.3.3.1.2.2.1.18",
            "phy_events": "iso.3.6.1.4.1.14823.2.3.3.1.2.2.1.18",
            "status": "iso.3.6.1.4.1.14823.2.3.3.1.2.2.1.20",
            "clients_count": "iso.3.6.1.4.1.14823.2.3.3.1.2.2.1.21",
        },
    },
    "a7010": {
        "ap_oids": {
            "ip": "iso.3.6.1.4.1.14823.2.2.1.5.2.1.4.1.2",
            "name": "iso.3.6.1.4.1.14823.2.2.1.5.2.1.4.1.3",
            "serial": "iso.3.6.1.4.1.14823.2.2.1.5.2.1.4.1.6",
            "model": "iso.3.6.1.4.1.14823.2.2.1.5.2.1.4.1.13",
            "uptime": "iso.3.6.1.4.1.14823.2.2.1.5.2.1.4.1.12",
            "status": "iso.3.6.1.4.1.14823.2.2.1.5.2.1.4.1.19",
            "cpu_usage": None,
            "free_mem": None,
            "total_mem": None,
        },
        "radio_oids": {
            "mac": "iso.3.6.1.4.1.14823.2.2.1.5.2.1.7.1.13",
            "ssid": "iso.3.6.1.4.1.14823.2.2.1.5.2.1.7.1.2",
            "noise": "iso.3.6.1.4.1.14823.2.2.1.1.3.3.1.13",
            "usage": "iso.3.6.1.4.1.14823.2.2.1.5.3.1.6.1.37",
            "tx_total_frames": "iso.3.6.1.4.1.14823.2.2.1.5.3.1.1.1.20",
            "tx_total_bytes": "iso.3.6.1.4.1.14823.2.2.1.5.3.1.1.1.21",
            "tx_dropped_frames": None,
            "rx_total_frames": "iso.3.6.1.4.1.14823.2.2.1.5.3.1.1.1.18",
            "rx_total_bytes": "iso.3.6.1.4.1.14823.2.2.1.5.3.1.1.1.19",
            "rx_bad_frames": "iso.3.6.1.4.1.14823.2.2.1.5.3.1.1.1.27",
            "phy_events": "iso.3.6.1.4.1.14823.2.3.3.1.2.2.1.18",
            "status": "iso.3.6.1.4.1.14823.2.3.3.1.2.2.1.20",
            "clients_count": "iso.3.6.1.4.1.14823.2.2.1.5.3.1.1.1.2",
        },
    },
}
DEFAULT_PROFILE = next(iter(PROFILES))


class SNMPClientException(Exception):
    """SNMP client exception"""


class SNMPClient:
    """SNMP client (based on easysnmp session usage)"""

    _default = {
        "hostname": "localhost",
        "community": "public",
        "version": 1,
        "timeout": 5,
        "remote_port": 161,
    }

    def __init__(self, profile=None, **kwargs):
        for key, default_value in self._default.items():
            kwargs[key] = kwargs.get(key, default_value)
        log.info(
            "Connect on SNMP host %s:%d as %s (%s)",
            kwargs["hostname"],
            kwargs["remote_port"],
            kwargs.get("security_username") or "anonymous",
            ", ".join(
                [
                    f"{key}: {value}"
                    for key, value in kwargs.items()
                    if key not in ("hostname", "remote_port", "security_username")
                    and "password" not in key
                ]
            ),
        )
        self.session = Session(**kwargs)
        self.profile_name = profile or DEFAULT_PROFILE
        try:
            self.profile = PROFILES[self.profile_name]
        except KeyError as err:
            raise SNMPClientException(f"Unsupported SNMP profile {self.profile_name}") from err

    def _item_value(self, item):
        if item.snmp_type == "OCTETSTR":
            value = "".join(filter(lambda c: c in string.printable, item.value))
            if value != item.value:
                return item.value.encode("latin-1").hex()
        return item.value

    def _iter_get(self, oids, key_info, oid_suffix=None):
        """Iteractive get all items info"""
        key_oid = oids[key_info]

        log.debug("_iter_get(%s, oid_suffix=%s): key OID=%s", key_info, oid_suffix, key_oid)
        result = []
        for item in self.session.walk(key_oid + (oid_suffix if oid_suffix else "")):
            info = {key_info: self._item_value(item)}
            log.debug(
                "_iter_get(%s, oid_suffix=%s): %s=%s (OID=%s)",
                key_info,
                oid_suffix,
                key_info,
                info[key_info],
                item.oid,
            )
            for key_name, oid in oids.items():
                if key_name == key_info or oid is None:
                    continue
                oid = item.oid.replace(key_oid, oid)
                try:
                    key_item = self.session.get(oid)
                    info[key_name] = self._item_value(key_item)
                except EasySNMPNoSuchNameError:
                    pass
                log.debug(
                    "_iter_get(%s, oid_suffix=%s): %s=%s / %s (%s) = %s",
                    key_info,
                    oid_suffix,
                    key_info,
                    info[key_info],
                    key_name,
                    oid,
                    info.get(key_name),
                )

            result.append(info)

        return result

    def _iter_key_oid(self, key_oid):
        """Iteractive get key info"""
        result = {}
        for item in self.session.walk(key_oid):
            result[item.oid.replace(key_oid, "")] = self._item_value(item)
        return result

    def get_aps_status(self):
        """Get all APs status"""
        return [
            ap
            | {
                "mem_usage": int(ap["free_mem"]) * 100 / int(ap["total_mem"])
                if ap.get("free_mem") is not None and ap["total_mem"] is not None
                else 0
            }
            for ap in self._iter_get(self.profile["ap_oids"], "ip")
        ]

    def get_radio_status(self, ip_address=None):
        """Get all radio interfaces status"""
        radio = {} if ip_address else []
        for oid_suffix, ip in self._iter_key_oid(self.profile["ap_oids"]["ip"]).items():
            if ip_address and ip_address != ip:
                continue
            log.debug("get_radio_status(%s): IP %s OID suffix = %s", ip_address, ip, oid_suffix)
            if ip_address:
                radio[ip] = []
            for it in self._iter_get(self.profile["radio_oids"], "mac", oid_suffix=oid_suffix):
                it["mac"] = ":".join([it["mac"][i : i + 2] for i in range(0, len(it["mac"]), 2)])
                if ip_address:
                    radio[ip].append(it)
                else:
                    radio.append(it)

        return radio.get(ip_address, []) if ip_address else radio  # pylint: disable=no-member

    def get_ap_status(self, ip_address=None):
        """Get one AP status"""
        aps = [ap for ap in self.get_aps_status() if ip_address is None or ip_address == ap["ip"]]
        log.debug("get_ap_status(%s): APs found: %s", ip_address, aps)
        assert (
            len(aps) == 1
        ), f"More than one AP IP address retreived via SNMP (OID: {self.profile['ap_oids']['ip']})"
        return aps[0]


# vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
