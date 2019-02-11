senderPyPath = r'C:\zabbix-agent\scripts\sender_wrapper.py'

agentConf = r'C:\zabbix_agentd.conf'

senderPath = r'C:\zabbix-agent\bin\win32\zabbix_sender.exe'

timeout = '80'

unknownCPUshift = 1000

keysandRegexp = (
                    ('hw.cpu.AddressWidth',                 r'^AddressWidth\=(.+)'),
                    ('hw.cpu.Architecture',                 r'^Architecture\=(.+)'),
                    ('hw.cpu.CpuStatus',                    r'^CpuStatus\=(.+)'),
                    ('hw.cpu.DataWidth',                    r'^DataWidth\=(.+)'),
                    ('hw.cpu.DeviceID',                     r'^DeviceID\=(.+)'),
                    ('hw.cpu.Family',                       r'^Family\=(.+)'),
                    ('hw.cpu.L2CacheSize',                  r'^L2CacheSize\=(\d+)'),
                    ('hw.cpu.L2CacheSpeed',                 r'^L2CacheSpeed\=(\d+)'),
                    ('hw.cpu.Level',                        r'^Level\=(.+)'),
                    ('hw.cpu.Name',                         r'^Name\=(.+)'),
                    ('hw.cpu.OtherFamilyDescription',       r'^OtherFamilyDescription\=(.+)'),
                    ('hw.cpu.PowerManagementCapabilities',  r'^PowerManagementCapabilities\=(.+)'),
                    ('hw.cpu.PowerManagementSupported',     r'^PowerManagementSupported\=(.+)'),
                    ('hw.cpu.ProcessorId',                  r'^ProcessorId\=(.+)'),
                    ('hw.cpu.ProcessorType',                r'^ProcessorType\=(.+)'),
                    ('hw.cpu.Revision',                     r'^Revision\=(.+)'),
                    ('hw.cpu.SocketDesignation',            r'^SocketDesignation\=(.+)'),
                    ('hw.cpu.StatusInfo',                   r'^StatusInfo\=(.+)'),
                    ('hw.cpu.Status',                       r'^Status\=(.+)'),
                    ('hw.cpu.UniqueId',                     r'^UniqueId\=(.+)'),
                    ('hw.cpu.UpgradeMethod',                r'^UpgradeMethod\=(.+)'),
                )

import sys
import re
import subprocess
from sender_wrapper import (processData)


def removeQuotes(s):
    quotes = ["'", '"']

    for i in quotes:
        s = s.replace(i, '')

    return s


def findOutput():

    try:
        p = subprocess.check_output(['wmic', 'CPU', 'list', 'full'], universal_newlines=True)
    except:
        p = ""
        
        if sys.argv[1] == 'getverb':
            print('Error calling wmic command. Terminating.')
            sys.exit(1)
            
    return p


def splitCPUblocks(p):

    split = p.split('\n\n\n')
    
    strip = [x for x in split if x.strip()]
    
    return strip


def findCPUnum(cpu_out):

    deviceIDRe = re.search(r'^DeviceID\=(.+)', cpu_out, re.I | re.M)
    if deviceIDRe:
        deviceID = deviceIDRe.group(1)
        deviceID = deviceID.strip()
    else:
        deviceID = None

    result = False
    cpuNum = re.search(r'(?:CPU|CPU\s+)(\d+)$', deviceID, re.I | re.M)
    if cpuNum:
        result = cpuNum.group(1).strip()

    return result


def findValues(cpuNum, cpu_out):
    sender = []
    
    for key, regexp in keysandRegexp:
        reVal = re.search(regexp, cpu_out, re.I | re.M)
        
        if reVal:
        
            val = reVal.group(1).strip()
            val = removeQuotes(val)
            sender.append('"%s" %s[cpu%s] "%s"' %(host, key, cpuNum, val))

    return sender


if __name__ == '__main__':
    
    host = str(sys.argv[2])

    jsonData = []
    senderData = []
    
    p_out = findOutput()
    
    for n, i in enumerate(splitCPUblocks(p_out)):
        
        cpuNum = findCPUnum(i)
        if cpuNum:
            cpu = cpuNum
        else:
            cpu = str(n + unknownCPUshift)
        
        cpuValues = findValues(cpu, i)
        
        if cpuValues:
            senderData.extend(cpuValues)
            jsonData.append({'{#CPUNUM}':cpu})

    link = 'norepoyet'
    processData(senderData, jsonData, agentConf, senderPyPath, senderPath, timeout, host, link)
