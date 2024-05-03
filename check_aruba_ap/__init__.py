""" Common formating helpers """

import datetime


def format_ap_info(ap):
    """Format AP info"""
    info = {}
    if "ip" in ap:
        info["IP"] = ap["ip"]
    if "model" in ap:
        info["Model"] = ap["model"]
    if "serial" in ap:
        info["Serial ID"] = ap["serial"]
    if "cpu_usage" in ap:
        info["CPU"] = f"{ap['cpu_usage']}%"
    if "mem_usage" in ap or ("free_mem" in ap and "total_mem" in ap):
        info["Mem"] = (
            f"{round(ap['mem_usage'], 1)}%"
            if "mem_usage" in ap
            else f"{round(ap['free_mem'] * 100 / ap['total_mem'], 1)}%"
        )
        if "free_mem" in ap and "total_mem" in ap:
            info["Mem"] += f" ({format_size(ap['free_mem'])}/{format_size(ap['total_mem'])})"
    if "uptime" in ap:
        info["Uptime"] = str(datetime.timedelta(seconds=int(ap["uptime"]) / 100))
    return info


def format_ap_status(ap):
    """Format AP status"""
    return f"{ap['name']} ({', '.join([f'{k}: {v}' for k, v in format_ap_info(ap).items()])})"


def format_radio_info(it):
    """Format radio interface info"""
    info = {}
    if "ssid" in it:
        info["SSID"] = it["ssid"]
    if "usage" in it:
        info["Usage"] = f"{it['usage']}%"
    if "status" in it:
        info["Status"] = it["status"]
    if "noise" in it:
        info["Noise"] = f"{it['noise']}dBm"
    if "tx_total_frames" in it:
        info["TX"] = f"{it['tx_total_frames']} frames"
        extra = []
        if "tx_total_bytes" in it:
            extra.append(format_size(it["tx_total_bytes"], input_unit="KiB"))
        if "tx_dropped_frames" in it:
            extra.append(f"drops: {it['tx_dropped_frames']} frames")
        if extra:
            info["TX"] += f" ({' '.join(extra)})"
    if "rx_total_frames" in it:
        info["RX"] = f"{it['rx_total_frames']} frames"
        extra = []
        if "rx_total_bytes" in it:
            extra.append(format_size(it["rx_total_bytes"], input_unit="KiB"))
        if "rx_bad_frames" in it:
            extra.append(f"bad: {it['rx_bad_frames']} frames")
        if extra:
            info["RX"] += f" ({' '.join(extra)})"
    if "phy_events" in it:
        info["Physical events"] = it["phy_events"]
    if "clients_count" in it:
        info["Clients"] = it["clients_count"]
    return info


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
