# zabbix-hardware
Current features:
- CPU hardware info with multiprocessor support for Windows through WMI
- RAM hardware info for Windows through WMI
- BIOS hardware info for Windows through WMI
- Network interfaces info for Windows through WMI

Requires Python 3.1+. It must be installed for all users and mentioned in PATH.

## Screenshots
[RAM Latest data](https://raw.githubusercontent.com/nobodysu/zabbix-hardware/master/screenshots/hardware-ram-items.png)

[CPU Latest data](https://raw.githubusercontent.com/nobodysu/zabbix-hardware/master/screenshots/hardware-cpu-items.png)

[BIOS Latest data](https://raw.githubusercontent.com/nobodysu/zabbix-hardware/master/screenshots/hardware-bios-items.png)

## Testing
```bash
server$ zabbix_get -s 192.0.2.1 -k hw.ram.discovery[get,"Example host"]
server$ zabbix_get -s 192.0.2.1 -k hw.cpu.discovery[get,"Example host"]
server$ zabbix_get -s 192.0.2.1 -k hw.net.discovery[get,"Example host"]
server$ zabbix_get -s 192.0.2.1 -k hw.bios[get,"Example host"]
```
Default operation mode. Displays json that server should get, detaches, then waits and sends data with zabbix-sender. `Example host` is your `Host name` field in zabbix.
<br /><br />

```bash
server$ zabbix_get -s 192.0.2.1 -k hw.ram.discovery[getverb,"Example host"]
server$ zabbix_get -s 192.0.2.1 -k hw.cpu.discovery[getverb,"Example host"]
server$ zabbix_get -s 192.0.2.1 -k hw.net.discovery[getverb,"Example host"]
server$ zabbix_get -s 192.0.2.1 -k hw.bios[getverb,"Example host"]
```
or locally:
```cmd
client> python "C:\zabbix-agent\scripts\hardware_net.py" getverb "Example host"
```
Verbose mode. Does not detaches or prints LLD. Lists all items sent to zabbix-sender, also it is possible to see sender output in this mode.
