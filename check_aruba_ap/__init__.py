""" Common formating helpers """

import datetime


def format_ap_info(ap):
    """Format AP info"""
    return {
        "IP": ap["ip"],
        "Serial ID": ap["serial"],
        "CPU": f"{ap['cpu_usage']}%",
        "Mem": (
            f"{round(ap['mem_usage'], 1)}% "
            f"({format_size(ap['free_mem'])}/{format_size(ap['total_mem'])})"
        ),
        "Uptime": str(datetime.timedelta(seconds=int(ap["uptime"]) / 100)),
    }


def format_ap_status(ap):
    """Format AP status"""
    return f"{ap['name']} ({', '.join([f'{k}: {v}' for k, v in format_ap_info(ap).items()])})"


def format_radio_info(it):
    """Format radio interface info"""
    return {
        "Usage": f"{it['usage']}%",
        "Status": it["status"],
        "Noise": f"{it['noise']}dBm",
        "TX": (
            f"{it['tx_total_frames']} frames "
            f"({format_size(it['tx_total_bytes'], input_unit='KiB')}, "
            f"drops: {it['tx_dropped_frames']} frames)"
        ),
        "RX": (
            f"{it['rx_total_frames']} frames "
            f"({format_size(it['rx_total_bytes'], input_unit='KiB')}, "
            f"bad: {it['rx_bad_frames']} frames)"
        ),
        "Physical events": it["phy_events"],
        "Clients": it["clients_count"],
    }


def format_size(num, input_unit=None):
    """Format file size"""
    num = float(num) if not isinstance(num, (int, float)) else num
    units = ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB")
    input_unit_idx = units.index(input_unit) if input_unit else 0
    for idx, unit in enumerate(units):
        if input_unit_idx and input_unit_idx > idx:
            continue
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}"
        num /= 1024.0
    return f"{num:.1f}YiB"


# vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
