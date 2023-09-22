""" Icinga plugin to check one Aruba AP state via SNMP """

import sys

from check_aruba_ap import format_ap_info
from check_aruba_ap.scripts import get_parser
from check_aruba_ap.snmp_client import SNMPClient


def main(argv=None):
    """Script main"""
    parser = get_parser(description=__doc__)
    args = parser.parse_args(argv if argv else sys.argv[1:])

    snmp_client = SNMPClient(
        hostname=args.hostname, community=args.snmp_community, version=args.snmp_version
    )

    ap = snmp_client.get_ap_status(ip_address=args.hostname)
    status = 0
    errors = []
    messages = []
    extra_lines = [f"{k}: {v}" for k, v in format_ap_info(ap).items()]
    perf_data = {
        "cpu": ";".join(
            [
                f"{ap['cpu_usage']}%",
                str(args.warning_cpu_threshold),
                str(args.critical_cpu_threshold),
                "0",
                "100",
            ]
        ),
        "mem": ";".join(
            [
                f"{round(ap['mem_usage'], 1)}%",
                str(args.warning_memory_threshold),
                str(args.critical_memory_threshold),
                "0",
                "100",
            ]
        ),
    }

    if int(ap["cpu_usage"]) >= args.critical_cpu_threshold:
        status = 2
        errors.append(f"CPU usage >= {args.critical_cpu_threshold}%)")
    elif int(ap["cpu_usage"]) >= args.warning_cpu_threshold:
        status = status if status > 1 else 1
        errors.append(f"CPU usage >= {args.warning_cpu_threshold}%)")

    if int(ap["mem_usage"]) >= args.critical_memory_threshold:
        status = 2
        errors.append(f"Memory usage >= {args.critical_memory_threshold}%)")
    elif int(ap["mem_usage"]) >= args.warning_memory_threshold:
        status = status if status > 1 else 1
        errors.append(f"Memory usage >= {args.warning_memory_threshold}%)")

    if not errors:
        messages.append(f"AP {ap['name']} is online and in optimal state")

    status_labels = {0: "OK", 1: "WARNING", 2: "CRITICAL", 3: "UNKNOWN"}
    print(
        f"{status_labels[status]} - {', '.join(errors + messages)}"
        f" | {', '.join([f'{k}={v}' for k, v in perf_data.items()])}"
    )
    print("\n".join(extra_lines))


# vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
