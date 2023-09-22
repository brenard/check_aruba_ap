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


def format_size(num, suffix="B"):
    """Format file size"""
    num = float(num) if not isinstance(num, (int, float)) else num
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


# vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
