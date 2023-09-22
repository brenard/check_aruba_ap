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

    def get_aps_status(self):
        """Get all APs status"""
        key_info = "ip"
        key_oid = self.ap_oids[key_info]
        aps = []
        for item in self.session.walk(key_oid):
            ap = {key_info: item.value}
            for key_name, oid in self.ap_oids.items():
                if key_name == key_info:
                    continue
                oid = item.oid.replace(key_oid, oid)
                key_item = self.session.get(oid)
                ap[key_name] = key_item.value  # pylint: disable=no-member

            # Compute memory usage (based on free & total)
            ap["mem_usage"] = int(ap["free_mem"]) * 100 / int(ap["total_mem"])

            aps.append(ap)

        return aps

    def get_ap_status(self, ip_address=None):
        """Get one AP status"""
        aps = [ap for ap in self.get_aps_status() if ip_address is None or ip_address == ap["ip"]]
        assert (
            len(aps) == 1
        ), f"More than one AP IP address retreived via SNMP (OID: {self.ap_oids['ip']})"
        return aps[0]


# vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
