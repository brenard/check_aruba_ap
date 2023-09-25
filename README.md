# check_aruba_ap

Check Aruba APs plugin for Icinga (via SNMP).

## Installation

```bash
python3 -m pip install 'check_aruba_ap@git+https://github.com/brenard/check_aruba_ap'
```

## Usage

### check_aruba_aps

```
usage: check_aruba_aps [-h] -H HOSTNAME [-C SNMP_COMMUNITY] [-V SNMP_VERSION] [-cw WARNING_CPU_THRESHOLD] [-cc CRITICAL_CPU_THRESHOLD] [-mc WARNING_MEMORY_THRESHOLD]
                       [-mw CRITICAL_MEMORY_THRESHOLD] [-rc WARNING_RADIO_USAGE_THRESHOLD] [-rw CRITICAL_RADIO_USAGE_THRESHOLD]

Icinga plugin to check all Aruba APs state via SNMP on the controller

options:
  -h, --help            show this help message and exit
  -H HOSTNAME, --hostname HOSTNAME
                        Aruba SNMP hostname (IP address required for the current elected virtual controller)
  -C SNMP_COMMUNITY, --snmp-community SNMP_COMMUNITY
                        SNMP community (default: public)
  -V SNMP_VERSION, --snmp-version SNMP_VERSION
                        SNMP version (default: 1)
  -t SNMP_TIMEOUT, --snmp-timeout SNMP_TIMEOUT
                        SNMP timeout (default: 5)
  -cw WARNING_CPU_THRESHOLD, --warning-cpu-threshold WARNING_CPU_THRESHOLD
                        Warning AP CPU usage threshold (default: 80%)
  -cc CRITICAL_CPU_THRESHOLD, --critical-cpu-threshold CRITICAL_CPU_THRESHOLD
                        Critical AP CPU usage threshold (default: 95%)
  -mc WARNING_MEMORY_THRESHOLD, --warning-memory-threshold WARNING_MEMORY_THRESHOLD
                        Warning AP memory threshold (default: 80%)
  -mw CRITICAL_MEMORY_THRESHOLD, --critical-memory-threshold CRITICAL_MEMORY_THRESHOLD
                        Critical AP memory threshold (default: 95%)
```

### check_aruba_ap
```
usage: check_aruba_ap [-h] -H HOSTNAME [-C SNMP_COMMUNITY] [-V SNMP_VERSION] [-cw WARNING_CPU_THRESHOLD] [-cc CRITICAL_CPU_THRESHOLD] [-mc WARNING_MEMORY_THRESHOLD]
                      [-mw CRITICAL_MEMORY_THRESHOLD] [-rc WARNING_RADIO_USAGE_THRESHOLD] [-rw CRITICAL_RADIO_USAGE_THRESHOLD]

Icinga plugin to check one Aruba AP state via SNMP

options:
  -h, --help            show this help message and exit
  -H HOSTNAME, --hostname HOSTNAME
                        Aruba SNMP hostname (IP address required for the current elected virtual controller)
  -C SNMP_COMMUNITY, --snmp-community SNMP_COMMUNITY
                        SNMP community (default: public)
  -V SNMP_VERSION, --snmp-version SNMP_VERSION
                        SNMP version (default: 1)
  -t SNMP_TIMEOUT, --snmp-timeout SNMP_TIMEOUT
                        SNMP timeout (default: 5)
  -cw WARNING_CPU_THRESHOLD, --warning-cpu-threshold WARNING_CPU_THRESHOLD
                        Warning AP CPU usage threshold (default: 80%)
  -cc CRITICAL_CPU_THRESHOLD, --critical-cpu-threshold CRITICAL_CPU_THRESHOLD
                        Critical AP CPU usage threshold (default: 95%)
  -mc WARNING_MEMORY_THRESHOLD, --warning-memory-threshold WARNING_MEMORY_THRESHOLD
                        Warning AP memory threshold (default: 80%)
  -mw CRITICAL_MEMORY_THRESHOLD, --critical-memory-threshold CRITICAL_MEMORY_THRESHOLD
                        Critical AP memory threshold (default: 95%)
  -rc WARNING_RADIO_USAGE_THRESHOLD, --warning-radio-usage-threshold WARNING_RADIO_USAGE_THRESHOLD
                        Warning AP radio interface usage threshold (default: 80%)
  -rw CRITICAL_RADIO_USAGE_THRESHOLD, --critical-radio-usage-threshold CRITICAL_RADIO_USAGE_THRESHOLD
                        Critical AP radio interface usage threshold (default: 95%)
```

## Icinga2 configuration

### Check commands declarations

```
object CheckCommand "check_aruba_aps" {
    command = [ "/usr/local/bin/check_aruba_aps" ]
    arguments += {
        "--hostname" = {
            description = "Aruba controller hostname or IP address"
            required = true
            value = "$address$"
        }
        "--snmp-community" = {
            description = "SNMP community"
            required = false
            value = "$snmp_community$"
        }
        "--snmp-version" = {
            description = "SNMP version"
            required = false
            value = "$snmp_version$"
        }
        "--snmp-timeout" = {
            description = "SNMP timeout"
            required = false
            value = "$snmp_timeout$"
        }
        "--warning-cpu-threshold" = {
            description = "Warning CPU threshold"
            required = false
            value = "$aruba_ap_warning_cpu_threshold$"
        }
        "--critical-cpu-threshold" = {
            description = "Critical CPU threshold"
            required = false
            value = "$aruba_ap_critical_cpu_threshold$"
        }
        "--warning-memory-threshold" = {
            description = "Warning memory threshold"
            required = false
            value = "$aruba_ap_warning_memory_threshold$"
        }
        "--critical-memory-threshold" = {
            description = "Critical memory threshold"
            required = false
            value = "$aruba_ap_critical_memory_threshold$"
        }
    }
}

object CheckCommand "check_aruba_ap" {
    command = [ "/usr/local/bin/check_aruba_ap" ]
    arguments += {
        "--hostname" = {
            description = "Aruba AP hostname or IP address (IP address required for the current elected virtual controller)"
            required = true
            value = "$address$"
        }
        "--snmp-community" = {
            description = "SNMP community"
            required = false
            value = "$snmp_community$"
        }
        "--snmp-version" = {
            description = "SNMP version"
            required = false
            value = "$snmp_version$"
        }
        "--snmp-timeout" = {
            description = "SNMP timeout"
            required = false
            value = "$snmp_timeout$"
        }
        "--warning-cpu-threshold" = {
            description = "Warning CPU threshold"
            required = false
            value = "$aruba_ap_warning_cpu_threshold$"
        }
        "--critical-cpu-threshold" = {
            description = "Critical CPU threshold"
            required = false
            value = "$aruba_ap_critical_cpu_threshold$"
        }
        "--warning-memory-threshold" = {
            description = "Warning memory threshold"
            required = false
            value = "$aruba_ap_warning_memory_threshold$"
        }
        "--critical-memory-threshold" = {
            description = "Critical memory threshold"
            required = false
            value = "$aruba_ap_critical_memory_threshold$"
        }
        "--warning-radio-usage-threshold" = {
            description = "Warning radio usage threshold"
            required = false
            value = "$aruba_ap_warning_radio_usage_threshold$"
        }
        "--critical-radio-usage-threshold" = {
            description = "Critical radio usage threshold"
            required = false
            value = "$aruba_ap_critical_radio_usage_threshold$"
        }
    }
}
```

## Copyright

Copyright (c) 2023 Benjamin Renard

## License

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License version 3
as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
