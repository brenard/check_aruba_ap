""" Icinga plugin to check one Aruba AP state via SNMP """

from easysnmp.exceptions import EasySNMPTimeoutError

from check_aruba_ap import format_ap_info, format_radio_info
from check_aruba_ap.scripts import fatal_error, get_parser, get_snmp_client, parse_args


def main(argv=None):
    """Script main"""
    parser = get_parser(description=__doc__)

    parser.add_argument(
        "-A",
        "--ap-address",
        help=(
            "If the SNMP host is a controler, the AP IP address have to be provided using this "
            "parameter"
        ),
    )
    parser.add_argument(
        "-rc",
        "--warning-radio-usage-threshold",
        type=int,
        help="Warning AP radio interface usage threshold (default: 80%%)",
        default=80,
    )
    parser.add_argument(
        "-rw",
        "--critical-radio-usage-threshold",
        type=int,
        help="Critical AP radio interface usage threshold (default: 95%%)",
        default=95,
    )

    args = parse_args(parser, argv)
    snmp_client = get_snmp_client(args)

    try:
        ap = snmp_client.get_ap_status(ip_address=args.ap_address or args.hostname)
    except EasySNMPTimeoutError:
        fatal_error("Aruba AP not reachable via SNMP")
    status = 0
    errors = []
    messages = []
    extra_lines = [f"{k}: {v}" for k, v in format_ap_info(ap).items()]

    perf_data = {}

    if ap["status"] != "1":
        status = 2
        errors.append(f"AP {ap['name']} is offline")

    if "cpu_usage" in ap:
        perf_data["cpu"] = ";".join(
            [
                f"{ap['cpu_usage']}%",
                str(args.warning_cpu_threshold),
                str(args.critical_cpu_threshold),
                "0",
                "100",
            ]
        )
        if int(ap["cpu_usage"]) >= args.critical_cpu_threshold:
            status = 2
            errors.append(f"CPU usage >= {args.critical_cpu_threshold}%)")
        elif int(ap["cpu_usage"]) >= args.warning_cpu_threshold:
            status = status if status > 1 else 1
            errors.append(f"CPU usage >= {args.warning_cpu_threshold}%)")

    if "mem_usage" in ap:
        perf_data["mem"] = ";".join(
            [
                f"{round(ap['mem_usage'], 1)}%",
                str(args.warning_memory_threshold),
                str(args.critical_memory_threshold),
                "0",
                "100",
            ]
        )
        if int(ap["mem_usage"]) >= args.critical_memory_threshold:
            status = 2
            errors.append(f"Memory usage >= {args.critical_memory_threshold}%)")
        elif int(ap["mem_usage"]) >= args.warning_memory_threshold:
            status = status if status > 1 else 1
            errors.append(f"Memory usage >= {args.warning_memory_threshold}%)")

    try:
        radio = snmp_client.get_radio_status(ip_address=args.ap_address)
    except EasySNMPTimeoutError:
        fatal_error("Fail to retreived radio status via SNMP")

    for it in radio:
        if "usage" in it:
            if int(it["usage"]) >= args.critical_radio_usage_threshold:
                status = 2
                errors.append(
                    f"Interface {it['mac']} radio usage >= {args.critical_radio_usage_threshold}%)"
                )
            elif int(it["usage"]) >= args.warning_radio_usage_threshold:
                status = status if status > 1 else 1
                errors.append(
                    f"Interface {it['mac']} radio usage >= {args.warning_radio_usage_threshold}%)"
                )
            perf_data[f"Interface {it['mac']} - Usage"] = ";".join(
                [
                    f"{it['usage']}%",
                    str(args.warning_radio_usage_threshold),
                    str(args.critical_radio_usage_threshold),
                    "0",
                    "100",
                ]
            )
        if "noise" in it:
            perf_data[f"Interface {it['mac']} - Noise"] = f"{it['noise']}dBm;;;;"
        if "tx_total_frames" in it:
            perf_data[f"Interface {it['mac']} - TX total frames"] = f"{it['tx_total_frames']};;;;"
        if "tx_total_bytes" in it:
            perf_data[f"Interface {it['mac']} - TX total bytes"] = f"{it['tx_total_bytes']};;;;"
        if "tx_dropped_frames" in it:
            perf_data[
                f"Interface {it['mac']} - TX dropped frames"
            ] = f"{it['tx_dropped_frames']};;;;"
        if "rx_total_frames" in it:
            perf_data[f"Interface {it['mac']} - RX total frames"] = f"{it['rx_total_frames']};;;;"
        if "rx_total_bytes" in it:
            perf_data[f"Interface {it['mac']} - RX total bytes"] = f"{it['rx_total_bytes']};;;;"
        if "rx_bad_frames" in it:
            perf_data[f"Interface {it['mac']} - RX bad frames"] = f"{it['rx_bad_frames']};;;;"
        if "phy_events" in it:
            perf_data[f"Interface {it['mac']} - Physical events"] = f"{it['phy_events']};;;;"
        if "clients_count" in it:
            perf_data[f"Interface {it['mac']} - Clients"] = f"{it['clients_count']};;;;"

        extra_lines.append(f"Interface {it['mac']}:")
        extra_lines += [f"  {k}: {v}" for k, v in format_radio_info(it).items()]

    if not errors:
        messages.append(f"AP {ap['name']} is online and in optimal state")

    # Add quotes on perf_data labels (can't be done using f-string)
    perf_data = {f"'{label}'": value for label, value in perf_data.items()}

    status_labels = {0: "OK", 1: "WARNING", 2: "CRITICAL", 3: "UNKNOWN"}
    print(
        f"{status_labels[status]} - {', '.join(errors + messages)}"
        f" | {' '.join([f'{k}={v}' for k, v in perf_data.items()])}"
    )
    print("\n".join(extra_lines))

    return status


# vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
