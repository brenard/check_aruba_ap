""" Icinga plugin to check all Aruba APs state via SNMP on the controller """

import sys

from check_aruba_ap import format_ap_status
from check_aruba_ap.scripts import get_parser
from check_aruba_ap.snmp_client import SNMPClient


def main(argv=None):
    """Script main"""
    parser = get_parser(description=__doc__)
    args = parser.parse_args(argv if argv else sys.argv[1:])

    snmp_client = SNMPClient(
        hostname=args.hostname, community=args.snmp_community, version=args.snmp_version
    )

    aps = snmp_client.get_aps_status()
    aps = sorted(aps, key=lambda ap: ap["name"])
    offline_aps = [ap for ap in aps if ap["status"] != "1"]
    critical_cpu_aps = [ap for ap in aps if int(ap["cpu_usage"]) >= args.critical_cpu_threshold]
    warning_cpu_aps = [
        ap
        for ap in aps
        if int(ap["cpu_usage"]) >= args.warning_cpu_threshold and ap not in critical_cpu_aps
    ]
    critical_memory_aps = [
        ap for ap in aps if int(ap["mem_usage"]) >= args.critical_memory_threshold
    ]
    warning_memory_aps = [
        ap
        for ap in aps
        if int(ap["mem_usage"]) >= args.warning_memory_threshold and ap not in critical_memory_aps
    ]
    status = 0
    errors = []
    messages = []
    extra_lines = []
    if offline_aps:
        status = 2
        errors.append(f"{len(offline_aps)} offline APs detected on {len(aps)} APs")
        extra_lines.append("Offline APs:")
        extra_lines.append("\n".join([f"- {format_ap_status(ap)}" for ap in offline_aps]))

    if critical_cpu_aps:
        status = 2
        errors.append(
            f"{len(critical_cpu_aps)} APs with critical CPU usage "
            f"(>={args.critical_cpu_threshold}%)"
        )
        extra_lines.append(
            f"APs with critical CPU usage: {', '.join([ap['name'] for ap in critical_cpu_aps])}"
        )
    if warning_cpu_aps:
        status = status if status > 1 else 1
        errors.append(
            f"{len(warning_cpu_aps)} APs with warning CPU usage (>={args.warning_cpu_threshold}%)"
        )
        extra_lines.append(
            f"APs with warning CPU usage: {', '.join([ap['name'] for ap in warning_cpu_aps])}"
        )
    if critical_memory_aps:
        status = 2
        errors.append(
            f"{len(critical_memory_aps)} APs with critical memory usage "
            f"(>={args.critical_memory_threshold}%)"
        )
        extra_lines.append(
            "APs with critical memory usage: "
            f"{', '.join([ap['name'] for ap in critical_memory_aps])}"
        )
    if warning_memory_aps:
        status = status if status > 1 else 1
        errors.append(
            f"{len(warning_memory_aps)} APs with warning memory usage "
            f"(>={args.warning_memory_threshold}%)"
        )
        extra_lines.append(
            "APs with warning memory usage: "
            f"{', '.join([ap['name'] for ap in warning_memory_aps])}"
        )

    if not errors:
        messages.append(f"All {len(aps)} APs are online and in optimal state")

    if offline_aps:
        extra_lines.append("Online APs:")
    extra_lines.append(
        "\n".join([f"- {format_ap_status(ap)}" for ap in aps if ap not in offline_aps])
    )

    status_labels = {0: "OK", 1: "WARNING", 2: "CRITICAL", 3: "UNKNOWN"}
    print(f"{status_labels[status]} - {', '.join(errors + messages)}")
    print("\n".join(extra_lines))


# vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
