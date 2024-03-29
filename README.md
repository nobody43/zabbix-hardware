# zabbix-hardware
Current features:
- RAM hardware info for Windows through WMI
- CPU hardware info with multiprocessor support for Windows through WMI
- Network interfaces info for Windows through WMI
- BIOS hardware info for Windows through WMI

Requires [Python 3.1+](https://www.python.org/downloads/windows/). It must be mentioned [in PATH](https://github.com/nobody43/zabbix-hardware/blob/master/screenshots/python-installation1.png) and installed for [all users](https://github.com/nobody43/zabbix-hardware/blob/master/screenshots/python-installation2.png).

## Screenshots
[RAM Latest data](https://raw.githubusercontent.com/nobody43/zabbix-hardware/master/screenshots/hardware-ram-items.png)

[CPU Latest data](https://raw.githubusercontent.com/nobody43/zabbix-hardware/master/screenshots/hardware-cpu-items.png)

[NET Latest data](https://raw.githubusercontent.com/nobody43/zabbix-hardware/master/screenshots/hardware-net-items.png)

[BIOS Latest data](https://raw.githubusercontent.com/nobody43/zabbix-hardware/master/screenshots/hardware-bios-items.png)

## Testing
```bash
server$ zabbix_get -s 192.0.2.1 -k hw.ram.discovery[get,"Example host"]
server$ zabbix_get -s 192.0.2.1 -k hw.cpu.discovery[get,"Example host"]
server$ zabbix_get -s 192.0.2.1 -k hw.net.discovery[get,"Example host"]
server$ zabbix_get -s 192.0.2.1 -k hw.bios[get,"Example host"]
```
Default operation mode. Displays json that server should get, detaches, then waits and sends data with zabbix-sender. `Example host` is your `Host name` field in zabbix. You might want to use nonexistent name for testing to avoid unnecessary database pollution (client introduces itself with this name and false names will be ignored).
<br /><br />

```bash
server$ zabbix_get -s 192.0.2.1 -k hw.ram.discovery[getverb,"Example host"]
server$ zabbix_get -s 192.0.2.1 -k hw.cpu.discovery[getverb,"Example host"]
server$ zabbix_get -s 192.0.2.1 -k hw.net.discovery[getverb,"Example host"]
server$ zabbix_get -s 192.0.2.1 -k hw.bios[getverb,"Example host"]
```
or locally:
```cmd
client> python "C:\Program Files\Zabbix Agent\scripts\hardware_net_wmi.py" getverb "Example host"
```
Verbose mode. Does not detaches or prints LLD. Lists all items sent to zabbix-sender, also it is possible to see sender output in this mode.

These scripts were tested to work with following configurations:

- Windows 10 / Server 6.0 / Agent 4.0 / Python (3.1-3.11)
- Windows Server 2012 / Server 6.0 / Agent 4.0 / Python 3.11
- Windows 7 / Server (5.0, 6.0) / Agent (4.0, 5.0) / Python (3.1-3.8)
