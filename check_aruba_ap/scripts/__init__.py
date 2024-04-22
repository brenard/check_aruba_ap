""" Common script stuff """

import argparse
import sys

from check_aruba_ap.snmp_client import SNMPClient


def get_parser(*args, **kwargs):
    """Get script arguments parser"""
    parser = argparse.ArgumentParser(*args, **kwargs)

    parser.add_argument(
        "-H",
        "--hostname",
        type=str,
        help="Aruba SNMP hostname (IP address required for the current elected virtual controller)",
        required=True,
    )
    parser.add_argument(
        "-C",
        "--snmp-community",
        type=str,
        help="SNMP community (default: public)",
        default="public",
    )
    parser.add_argument(
        "-V", "--snmp-version", type=int, help="SNMP version (default: 1)", default=1
    )
    parser.add_argument(
        "-p", "--snmp-remote-port", type=int, help="SNMP remote port (default: 161)", default=161
    )
    parser.add_argument("--snmp-local-port", type=int, help="SNMP local port")
    parser.add_argument(
        "--snmp-security-level",
        choices=("no_auth_or_privacy", "auth_without_privacy", "auth_with_privacy"),
        help="SNMP v3 security level (default: 'no_auth_or_privacy')",
        default="no_auth_or_privacy",
    )
    parser.add_argument("-U", "--snmp-auth-username", help="SNMP v3 authentication username")
    parser.add_argument("-P", "--snmp-auth-password", help="SNMP v3 authentication password")
    parser.add_argument(
        "--snmp-auth-protocol",
        choices=("DEFAULT", "MD5", "SHA"),
        help="SNMP v3 authentication protocol (default: 'DEFAULT')",
        default="DEFAULT",
    )
    parser.add_argument(
        "--snmp-priv-protocol",
        choices=("DEFAULT", "DES", "AES"),
        help="SNMP v3 privacy protocol (default: 'DEFAULT')",
        default="DEFAULT",
    )
    parser.add_argument("--snmp-priv-password", help="SNMP v3 privacy password")
    parser.add_argument(
        "-t", "--snmp-timeout", type=int, help="SNMP timeout (default: 5)", default=5
    )

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
    return parser


def fatal_error(error):
    """Handle fatal error"""
    print(f"UNKNOWN - {error}")
    sys.exit(3)


def get_snmp_client(args):
    """Get a configured SNMPClient instance from command arguments"""
    return SNMPClient(
        hostname=args.hostname,
        community=args.snmp_community,
        version=args.snmp_version,
        remote_port=args.snmp_remote_port,
        local_port=args.snmp_local_port or 0,  # An int is required and zero is the default value
        security_level=args.snmp_security_level,
        security_username=args.snmp_auth_username,
        auth_password=args.snmp_auth_password,
        auth_protocol=args.snmp_auth_protocol,
        privacy_protocol=args.snmp_priv_protocol,
        privacy_password=args.snmp_priv_password,
    )


# vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
