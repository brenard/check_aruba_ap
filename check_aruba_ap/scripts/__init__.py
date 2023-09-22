""" Common script stuff """

import argparse


def get_parser(*args, **kwargs):
    """Get script arguments parser"""
    parser = argparse.ArgumentParser(*args, **kwargs)

    parser.add_argument(
        "-H",
        "--hostname",
        type=str,
        help="Aruba SNMP hostname (IP address required for the current elected virtual controller)",
        default="localhost",
    )
    parser.add_argument("-C", "--snmp-community", type=str, help="SNMP community", default="public")
    parser.add_argument("-V", "--snmp-version", type=int, help="SNMP version", default=1)
    parser.add_argument(
        "-cw",
        "--warning-cpu-threshold",
        type=int,
        help="Warning AP CPU usage threshold (default: 80%%)",
        default=80,
    )
    parser.add_argument(
        "-cc",
        "--critical-cpu-threshold",
        type=int,
        help="Critical AP CPU usage threshold (default: 95%%)",
        default=95,
    )
    parser.add_argument(
        "-mc",
        "--warning-memory-threshold",
        type=int,
        help="Warning AP memory threshold (default: 80%%)",
        default=80,
    )
    parser.add_argument(
        "-mw",
        "--critical-memory-threshold",
        type=int,
        help="Critical AP memory threshold (default: 95%%)",
        default=95,
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
    return parser


# vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
