#!/usr/bin/python3
import argparse
import datetime
from easysnmp import Session

parser = argparse.ArgumentParser()

parser.add_argument('-H', '--hostname', type=str, help="Aruba controller hostname", default="localhost")
parser.add_argument('-C', '--snmp-community', type=str, help="SNMP community", default="public")
parser.add_argument('-V', '--snmp-version', type=int, help="SNMP version", default=1)
parser.add_argument('-cw', '--warning-cpu-threshold', type=int, help="Warning AP CPU usage threshold (default: 80%%)", default=80)
parser.add_argument('-cc', '--critical-cpu-threshold', type=int, help="Critical AP CPU usage threshold (default: 95%%)", default=95)
parser.add_argument('-mc', '--warning-memory-threshold', type=int, help="Warning AP memory threshold (default: 80%%)", default=80)
parser.add_argument('-mw', '--critical-memory-threshold', type=int, help="Critical AP memory threshold (default: 95%%)", default=95)

args = parser.parse_args()

session = Session(hostname=args.hostname, community=args.snmp_community, version=args.snmp_version)

def get_aps_status():
    ap_oids = {
        'ip': 'iso.3.6.1.4.1.14823.2.3.3.1.2.1.1.3',
        'name': 'iso.3.6.1.4.1.14823.2.3.3.1.2.1.1.2',
        'serial': 'iso.3.6.1.4.1.14823.2.3.3.1.2.1.1.4',
        'uptime': 'iso.3.6.1.4.1.14823.2.3.3.1.2.1.1.9',
        'status': 'iso.3.6.1.4.1.14823.2.3.3.1.2.1.1.11',
        'cpu_usage': 'iso.3.6.1.4.1.14823.2.3.3.1.2.1.1.7',
        'free_mem': 'iso.3.6.1.4.1.14823.2.3.3.1.2.1.1.8',
        'total_mem': 'iso.3.6.1.4.1.14823.2.3.3.1.2.1.1.10',
    }
    
    key_info = next(iter(ap_oids))
    key_oid = ap_oids[key_info]
    aps = []
    for item in session.walk(key_oid):
        ap = {key_info: item.value}
        for key_name, oid in ap_oids.items():
            oid = item.oid.replace(key_oid, oid)
            key_item = session.get(oid)
            ap[key_name] = key_item.value

        ap['mem_usage'] = int(ap['free_mem']) * 100 / int(ap['total_mem'])
    
        aps.append(ap)
    
    return aps

def format_ap_status(ap):
    return "{name} (IP: {ip}, Serial ID: {serial}, CPU: {cpu_usage}%, Mem: {mem_usage}% ({free_mem}/{total_mem}), Uptime: {uptime})".format(
            **dict(
                (k, format_field(k, v))
                for k, v in ap.items()
            )
    )
    return ", ".join([
        f"{k}: {format_field(k, v)}"
        for k, v in ap.items()
        if k != 'status'
    ])

def format_size(num, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

def format_field(field, value):
    if field == 'uptime':
        return str(datetime.timedelta(seconds=int(value)/100))
    if field in ['free_mem', 'total_mem']:
        return format_size(int(value))
    if field == 'mem_usage':
        return f"{round(value, 1)}"
    return str(value)

aps = get_aps_status()
aps = sorted(aps, key=lambda ap: ap['name'])
offline_aps = [ap for ap in aps if ap['status'] != '1']
critical_cpu_aps = [
    ap for ap in aps
    if int(ap['cpu_usage']) >= args.critical_cpu_threshold
]
warning_cpu_aps = [
    ap for ap in aps
    if int(ap['cpu_usage']) >= args.warning_cpu_threshold and ap not in critical_cpu_aps
]
critical_memory_aps = [
    ap for ap in aps
    if int(ap['mem_usage']) >= args.critical_memory_threshold
]
warning_memory_aps = [
    ap for ap in aps
    if int(ap['mem_usage']) >= args.warning_memory_threshold and ap not in critical_memory_aps
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
    errors.append(f"{len(critical_cpu_aps)} APs with critical CPU usage (>={args.critical_cpu_threshold}%)")
    extra_lines.append(f"APs with critical CPU usage: {', '.join([ap['name'] for ap in critical_cpu_aps])}")
if warning_cpu_aps:
    status = status if status > 1 else 1
    errors.append(f"{len(warning_cpu_aps)} APs with warning CPU usage (>={args.warning_cpu_threshold}%)")
    extra_lines.append(f"APs with warning CPU usage: {', '.join([ap['name'] for ap in warning_cpu_aps])}")
if critical_memory_aps:
    status = 2
    errors.append(f"{len(critical_memory_aps)} APs with critical memory usage (>={args.critical_memory_threshold}%)")
    extra_lines.append(f"APs with critical memory usage: {', '.join([ap['name'] for ap in critical_memory_aps])}")
if warning_memory_aps:
    status = status if status > 1 else 1
    errors.append(f"{len(warning_memory_aps)} APs with warning memory usage (>={args.warning_memory_threshold}%)")
    extra_lines.append(f"APs with warning memory usage: {', '.join([ap['name'] for ap in warning_memory_aps])}")

if not errors:
    messages.append(f"All {len(aps)} APs are online and in optimal state")

if offline_aps:
    extra_lines.append("Online APs:")
extra_lines.append("\n".join([f"- {format_ap_status(ap)}" for ap in aps if ap not in offline_aps]))

status_labels = {0: 'OK', 1: 'WARNING', 2: 'CRITICAL', 3: 'UNKNOWN'}
print(f"{status_labels[status]} - {', '.join(errors + messages)}")
print("\n".join(extra_lines))

# vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
