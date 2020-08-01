import sys
import re
import subprocess

p = subprocess.check_output(['wmic', 'MEMPHYSICAL', 'list', 'full'], universal_newlines=True)

memoryDevicesRe = re.search(r'^MemoryDevices\=(\d+)', p, re.M)
if memoryDevicesRe:
    print(memoryDevicesRe.group(1))
else:
    print('NO MATCH!')
    print(p)
