# check_aruba_ap

Check Aruba APs plugin for Icinga (via SNMP).

__Note:__ Test on :
 * Virtual Controler (Instant Mode) version 8.10.0.6 and AP-515 / AP-575 (firmware version 8.10.0.6) (use `--snmp-profile instant_node`, default)
 * A7010 Controler version 8.10.0.6 LSR and APs 535, 515, 375 & 345 (use `--snmp-profile a7010`)

## Installation

### Using pip

```bash
python3 -m pip install 'check_aruba_ap@git+https://github.com/brenard/check_aruba_ap'
```

__Note:__ Since Debian 12 Bookworm, you have to add the `--break-system-packages` parameter.

### Using pip with a virtualenv

```bash
sudo apt install python3-venv
python3 -m venv /usr/local/share/check_aruba_ap
/usr/local/share/check_aruba_ap/bin/python3 -m pip install \
  'check_aruba_ap@git+https://github.com/brenard/check_aruba_ap'
mkdir -p /usr/local/lib/nagios/plugins
ln -s /usr/local/share/check_aruba_ap/bin/check_aruba_ap* /usr/local/lib/nagios/plugins
```

### Using pipx

```bash
sudo \
  PIPX_HOME=/usr/local/share/pipx-nagios-plugins \
  PIPX_BIN_DIR=/usr/local/lib/nagios/plugins \
  python3 -m pipx install \
  'check_aruba_ap@git+https://github.com/brenard/check_aruba_ap'
```

__Note:__ the `pipx` package is available since Debian 11 Bulleyes (via backports) and Debian 12 Bookworm.

## Upgrade

### Using pip

```bash
python3 -m pip uninstall check_aruba_ap
python3 -m pip install -U 'check_aruba_ap@git+https://github.com/brenard/check_aruba_ap'
```

### Using pip with a virtualenv

```bash
/usr/local/share/check_aruba_ap/bin/python3 -m pip uninstall \
  'check_aruba_ap'
/usr/local/share/check_aruba_ap/bin/python3 -m pip install \
  'check_aruba_ap@git+https://github.com/brenard/check_aruba_ap'
```

### Using pipx

```bash
sudo \
  PIPX_HOME=/usr/local/share/pipx-nagios-plugins \
  PIPX_BIN_DIR=/usr/local/lib/nagios/plugins \
  python3 -m pipx uninstall check_aruba_ap
sudo \
  PIPX_HOME=/usr/local/share/pipx-nagios-plugins \
  PIPX_BIN_DIR=/usr/local/lib/nagios/plugins \
  python3 -m pipx install \
  'check_aruba_ap@git+https://github.com/brenard/check_aruba_ap'
```

## Usage

### check_aruba_aps
```
usage: check_aruba_aps [-h] -H HOSTNAME [-cw WARNING_CPU_THRESHOLD]
                       [-cc CRITICAL_CPU_THRESHOLD] [-mc WARNING_MEMORY_THRESHOLD]
                       [-mw CRITICAL_MEMORY_THRESHOLD]
                       [--snmp-profile {instant_node,a7010}] [-C SNMP_COMMUNITY]
                       [-V SNMP_VERSION] [-p SNMP_REMOTE_PORT]
                       [--snmp-local-port SNMP_LOCAL_PORT]
                       [--snmp-security-level {no_auth_or_privacy,auth_without_privacy,auth_with_privacy}]
                       [-U SNMP_AUTH_USERNAME] [-P SNMP_AUTH_PASSWORD]
                       [--snmp-auth-protocol {DEFAULT,MD5,SHA}]
                       [--snmp-priv-protocol {DEFAULT,DES,AES}]
                       [--snmp-priv-password SNMP_PRIV_PASSWORD] [-t SNMP_TIMEOUT]
                       [-v] [-d] [-l LOG_FILE] [-c]

Icinga plugin to check all Aruba APs state via SNMP on the controller

options:
  -h, --help            show this help message and exit
  -H HOSTNAME, --hostname HOSTNAME
                        Aruba SNMP hostname (IP address required for the current
                        elected virtual controller)
  -cw WARNING_CPU_THRESHOLD, --warning-cpu-threshold WARNING_CPU_THRESHOLD
                        Warning AP CPU usage threshold (default: 80%)
  -cc CRITICAL_CPU_THRESHOLD, --critical-cpu-threshold CRITICAL_CPU_THRESHOLD
                        Critical AP CPU usage threshold (default: 95%)
  -mc WARNING_MEMORY_THRESHOLD, --warning-memory-threshold WARNING_MEMORY_THRESHOLD
                        Warning AP memory threshold (default: 80%)
  -mw CRITICAL_MEMORY_THRESHOLD, --critical-memory-threshold CRITICAL_MEMORY_THRESHOLD
                        Critical AP memory threshold (default: 95%)

SNMP options:
  --snmp-profile {instant_node,a7010}
                        SNMP profile (default: instant_node)
  -C SNMP_COMMUNITY, --snmp-community SNMP_COMMUNITY
                        SNMP community (default: public)
  -V SNMP_VERSION, --snmp-version SNMP_VERSION
                        SNMP version (default: 1)
  -p SNMP_REMOTE_PORT, --snmp-remote-port SNMP_REMOTE_PORT
                        SNMP remote port (default: 161)
  --snmp-local-port SNMP_LOCAL_PORT
                        SNMP local port
  --snmp-security-level {no_auth_or_privacy,auth_without_privacy,auth_with_privacy}
                        SNMP v3 security level (default: 'no_auth_or_privacy')
  -U SNMP_AUTH_USERNAME, --snmp-auth-username SNMP_AUTH_USERNAME
                        SNMP v3 authentication username
  -P SNMP_AUTH_PASSWORD, --snmp-auth-password SNMP_AUTH_PASSWORD
                        SNMP v3 authentication password
  --snmp-auth-protocol {DEFAULT,MD5,SHA}
                        SNMP v3 authentication protocol (default: 'DEFAULT')
  --snmp-priv-protocol {DEFAULT,DES,AES}
                        SNMP v3 privacy protocol (default: 'DEFAULT')
  --snmp-priv-password SNMP_PRIV_PASSWORD
                        SNMP v3 privacy password
  -t SNMP_TIMEOUT, --snmp-timeout SNMP_TIMEOUT
                        SNMP timeout (default: 5)

Logging options:
  -v, --verbose         Enable verbose mode
  -d, --debug           Enable debug mode
  -l LOG_FILE, --log-file LOG_FILE
                        Log file path
  -c, --console         Always log on console (even if log file is configured)
```

### check_aruba_ap
```
usage: check_aruba_ap [-h] -H HOSTNAME [-cw WARNING_CPU_THRESHOLD]
                      [-cc CRITICAL_CPU_THRESHOLD] [-mc WARNING_MEMORY_THRESHOLD]
                      [-mw CRITICAL_MEMORY_THRESHOLD]
                      [--snmp-profile {instant_node,a7010}] [-C SNMP_COMMUNITY]
                      [-V SNMP_VERSION] [-p SNMP_REMOTE_PORT]
                      [--snmp-local-port SNMP_LOCAL_PORT]
                      [--snmp-security-level {no_auth_or_privacy,auth_without_privacy,auth_with_privacy}]
                      [-U SNMP_AUTH_USERNAME] [-P SNMP_AUTH_PASSWORD]
                      [--snmp-auth-protocol {DEFAULT,MD5,SHA}]
                      [--snmp-priv-protocol {DEFAULT,DES,AES}]
                      [--snmp-priv-password SNMP_PRIV_PASSWORD] [-t SNMP_TIMEOUT]
                      [-v] [-d] [-l LOG_FILE] [-c] [-A AP_ADDRESS]
                      [-rc WARNING_RADIO_USAGE_THRESHOLD]
                      [-rw CRITICAL_RADIO_USAGE_THRESHOLD]

Icinga plugin to check one Aruba AP state via SNMP

options:
  -h, --help            show this help message and exit
  -H HOSTNAME, --hostname HOSTNAME
                        Aruba SNMP hostname (IP address required for the current
                        elected virtual controller)
  -cw WARNING_CPU_THRESHOLD, --warning-cpu-threshold WARNING_CPU_THRESHOLD
                        Warning AP CPU usage threshold (default: 80%)
  -cc CRITICAL_CPU_THRESHOLD, --critical-cpu-threshold CRITICAL_CPU_THRESHOLD
                        Critical AP CPU usage threshold (default: 95%)
  -mc WARNING_MEMORY_THRESHOLD, --warning-memory-threshold WARNING_MEMORY_THRESHOLD
                        Warning AP memory threshold (default: 80%)
  -mw CRITICAL_MEMORY_THRESHOLD, --critical-memory-threshold CRITICAL_MEMORY_THRESHOLD
                        Critical AP memory threshold (default: 95%)
  -A AP_ADDRESS, --ap-address AP_ADDRESS
                        If the SNMP host is a controler, the AP IP address have to
                        be provided using this parameter
  -rc WARNING_RADIO_USAGE_THRESHOLD, --warning-radio-usage-threshold WARNING_RADIO_USAGE_THRESHOLD
                        Warning AP radio interface usage threshold (default: 80%)
  -rw CRITICAL_RADIO_USAGE_THRESHOLD, --critical-radio-usage-threshold CRITICAL_RADIO_USAGE_THRESHOLD
                        Critical AP radio interface usage threshold (default: 95%)

SNMP options:
  --snmp-profile {instant_node,a7010}
                        SNMP profile (default: instant_node)
  -C SNMP_COMMUNITY, --snmp-community SNMP_COMMUNITY
                        SNMP community (default: public)
  -V SNMP_VERSION, --snmp-version SNMP_VERSION
                        SNMP version (default: 1)
  -p SNMP_REMOTE_PORT, --snmp-remote-port SNMP_REMOTE_PORT
                        SNMP remote port (default: 161)
  --snmp-local-port SNMP_LOCAL_PORT
                        SNMP local port
  --snmp-security-level {no_auth_or_privacy,auth_without_privacy,auth_with_privacy}
                        SNMP v3 security level (default: 'no_auth_or_privacy')
  -U SNMP_AUTH_USERNAME, --snmp-auth-username SNMP_AUTH_USERNAME
                        SNMP v3 authentication username
  -P SNMP_AUTH_PASSWORD, --snmp-auth-password SNMP_AUTH_PASSWORD
                        SNMP v3 authentication password
  --snmp-auth-protocol {DEFAULT,MD5,SHA}
                        SNMP v3 authentication protocol (default: 'DEFAULT')
  --snmp-priv-protocol {DEFAULT,DES,AES}
                        SNMP v3 privacy protocol (default: 'DEFAULT')
  --snmp-priv-password SNMP_PRIV_PASSWORD
                        SNMP v3 privacy password
  -t SNMP_TIMEOUT, --snmp-timeout SNMP_TIMEOUT
                        SNMP timeout (default: 5)

Logging options:
  -v, --verbose         Enable verbose mode
  -d, --debug           Enable debug mode
  -l LOG_FILE, --log-file LOG_FILE
                        Log file path
  -c, --console         Always log on console (even if log file is configured)
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
