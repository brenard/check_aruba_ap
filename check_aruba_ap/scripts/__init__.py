""" Common script stuff """

import argparse
import logging
import os.path
import sys

from check_aruba_ap.snmp_client import DEFAULT_PROFILE, PROFILES, SNMPClient


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

    snmp_opts = parser.add_argument_group("SNMP options")

    snmp_opts.add_argument(
        "--snmp-profile",
        choices=list(PROFILES.keys()),
        help=f"SNMP profile (default: {DEFAULT_PROFILE})",
        default=DEFAULT_PROFILE,
    )
    snmp_opts.add_argument(
        "-C",
        "--snmp-community",
        type=str,
        help="SNMP community (default: public)",
        default="public",
    )
    snmp_opts.add_argument(
        "-V", "--snmp-version", type=int, help="SNMP version (default: 1)", default=1
    )
    snmp_opts.add_argument(
        "-p", "--snmp-remote-port", type=int, help="SNMP remote port (default: 161)", default=161
    )
    snmp_opts.add_argument("--snmp-local-port", type=int, help="SNMP local port")
    snmp_opts.add_argument(
        "--snmp-security-level",
        choices=("no_auth_or_privacy", "auth_without_privacy", "auth_with_privacy"),
        help="SNMP v3 security level (default: 'no_auth_or_privacy')",
        default="no_auth_or_privacy",
    )
    snmp_opts.add_argument("-U", "--snmp-auth-username", help="SNMP v3 authentication username")
    snmp_opts.add_argument("-P", "--snmp-auth-password", help="SNMP v3 authentication password")
    snmp_opts.add_argument(
        "--snmp-auth-protocol",
        choices=("DEFAULT", "MD5", "SHA"),
        help="SNMP v3 authentication protocol (default: 'DEFAULT')",
        default="DEFAULT",
    )
    snmp_opts.add_argument(
        "--snmp-priv-protocol",
        choices=("DEFAULT", "DES", "AES"),
        help="SNMP v3 privacy protocol (default: 'DEFAULT')",
        default="DEFAULT",
    )
    snmp_opts.add_argument("--snmp-priv-password", help="SNMP v3 privacy password")
    snmp_opts.add_argument(
        "-t", "--snmp-timeout", type=int, help="SNMP timeout (default: 5)", default=5
    )

    log_opts = parser.add_argument_group("Logging options")

    log_opts.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    log_opts.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    log_opts.add_argument("-l", "--log-file", help="Log file path")
    log_opts.add_argument(
        "-c",
        "--console",
        action="store_true",
        help="Always log on console (even if log file is configured)",
    )

    return parser


def parse_args(parser, argv=None):
    """Parse and return script arguments"""
    args = parser.parse_args(argv if argv else sys.argv[1:])

    # Init logging
    logformat = f"%(asctime)s - {os.path.basename(sys.argv[0])} - %(levelname)s - %(message)s"
    if args.debug:
        loglevel = logging.DEBUG
    elif args.verbose:
        loglevel = logging.INFO
    else:
        loglevel = logging.WARNING

    handlers = []
    if args.log_file:
        handlers.append(logging.FileHandler(args.log_file))
    if not args.log_file or args.console:
        handlers.append(logging.StreamHandler())
    logging.basicConfig(level=loglevel, format=logformat, handlers=handlers)

    return args


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
        profile=args.snmp_profile,
    )


# vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
