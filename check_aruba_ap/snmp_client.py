""" SNMP Client """

from easysnmp import Session


class SNMPClient:
    """SNMP client (based on easysnmp session usage)"""

    hostname = "localhost"
    community = "public"
    version = 1
    session = None

    ap_oids = {
        "ip": "iso.3.6.1.4.1.14823.2.3.3.1.2.1.1.3",
        "name": "iso.3.6.1.4.1.14823.2.3.3.1.2.1.1.2",
        "serial": "iso.3.6.1.4.1.14823.2.3.3.1.2.1.1.4",
        "uptime": "iso.3.6.1.4.1.14823.2.3.3.1.2.1.1.9",
        "status": "iso.3.6.1.4.1.14823.2.3.3.1.2.1.1.11",
        "cpu_usage": "iso.3.6.1.4.1.14823.2.3.3.1.2.1.1.7",
        "free_mem": "iso.3.6.1.4.1.14823.2.3.3.1.2.1.1.8",
        "total_mem": "iso.3.6.1.4.1.14823.2.3.3.1.2.1.1.10",
    }

    radio_oids = {
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
    }

    def __init__(self, hostname=None, community=None, version=None):
        if hostname is not None:
            self.hostname = hostname
        if community is not None:
            self.community = community
        if version is not None:
            self.version = version
        self.session = Session(
            hostname=self.hostname, community=self.community, version=self.version
        )

    @staticmethod
    def _item_value(item):
        return item.value.encode("latin-1").hex() if item.snmp_type == "OCTETSTR" else item.value

    def _iter_get(self, oids, key_info):
        """Iteractive get all items info"""
        key_oid = oids[key_info]
        result = []
        for item in self.session.walk(key_oid):
            info = {key_info: self._item_value(item)}
            for key_name, oid in oids.items():
                if key_name == key_info:
                    continue
                oid = item.oid.replace(key_oid, oid)
                key_item = self.session.get(oid)
                info[key_name] = self._item_value(key_item)

            result.append(info)

        return result

    def get_aps_status(self):
        """Get all APs status"""
        return [
            ap | {"mem_usage": int(ap["free_mem"]) * 100 / int(ap["total_mem"])}
            for ap in self._iter_get(self.ap_oids, "ip")
        ]

    def get_radio_status(self):
        """Get all radio interfaces status"""
        radio = []
        for it in self._iter_get(self.radio_oids, "mac"):
            it["mac"] = ":".join([it["mac"][i : i + 2] for i in range(0, len(it["mac"]), 2)])
            radio.append(it)
        return radio

    def get_ap_status(self, ip_address=None):
        """Get one AP status"""
        aps = [ap for ap in self.get_aps_status() if ip_address is None or ip_address == ap["ip"]]
        assert (
            len(aps) == 1
        ), f"More than one AP IP address retreived via SNMP (OID: {self.ap_oids['ip']})"
        return aps[0]


# vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
