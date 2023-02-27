## Installation instructions: https://github.com/nobodysu/zabbix-hardware ##

senderPyPath = r'C:\Program Files\Zabbix Agent\scripts\sender_wrapper.py'

agentConf    = r'C:\Program Files\Zabbix Agent\zabbix_agentd.conf'

senderPath   = r'C:\Program Files\Zabbix Agent\zabbix_sender.exe'


## Advanced configuration ##

delay          = '50'   # Between LLD and data sending
heavyDebug     = False

cmd = 'wmic path Win32_NetworkAdapter where PhysicalAdapter=TRUE get /value'

keysAndRegexps = (
    ('hw.net.wmi.Speed',        r'^Speed=(\d+)'),
    ('hw.net.wmi.MACAddress',   r'^MACAddress=(.+)'),
    ('hw.net.wmi.ProductName',  r'^ProductName=(.+)'),
    ('hw.net.wmi.AdapterType',  r'^AdapterType=(.+)'),
)

ignoredServiceNames = (
    'msloop',
    'VBoxNetAdp',
)

# re.I | re.M
speedFormat = (
    ('^10(?:\s+)?Mb',        10000000),
    ('^100(?:\s+)?Mb',       100000000),
    ('^1(?:\.0)?(?:\s+)?Gb', 1000000000),
    ('^10(?:\s+)?Gb',        10000000000),
    ('^25(?:\s+)?Gb',        25000000000),
    ('^40(?:\s+)?Gb',        40000000000),
    ('^50(?:\s+)?Gb',        50000000000),
    ('^100(?:\s+)?Gb',       100000000000),
)

manualMaxSpeed = (
    (r'NVIDIA nForce 10/100/1000 Mbps Ethernet', 1000000000),
)


## End of configuration ##

import sys
import re
import subprocess
import winreg
from sender_wrapper import (processData, fail_ifNot_Py3, removeQuotes)


def wmiNetRun(cmd_):

    err = None

    try:
        p = subprocess.check_output(cmd_, universal_newlines=True)

    except subprocess.TimeoutExpired:
        err = 'TIMEOUT'

    except:
        p = ''

    p = p.replace('\n\n', '\n')

    return (p, err)

def findValuesInWMI(ID_, block_):
    sender = []
    
    if isIgnoredService(block_):
        return sender

    for key, regexp in keysAndRegexps:

        reVal = re.search(regexp, block_, re.I | re.M)
        
        
        if reVal:
            
            val = reVal.group(1).strip()
            val = removeQuotes(val)

            sender.append('"%s" %s[%s] "%s"' % (host, key, ID_, val))

    return sender
    
def isIgnoredService(block_):
    serviceName = re.search(r'^ServiceName=(.+)', block_, re.I | re.M)
    if serviceName:
        if serviceName.group(1) in ignoredServiceNames:
            return True
    else:
        return False
    

def splitBlocks(p):

    split = p.split('\n\n\n')

    strip = [x for x in split if x.strip()]

    return strip
    
def findRaw_ifID(block):
    ID = re.search(r'DeviceID=(\d+)', block, re.M | re.I)
    if ID:
        return ID.group(1)
    else:
        return ('Error: No ID found')
        sys.exit(1)
        
def rawToFull_ifID(rawID):
    rawID = str(rawID)

    if len(rawID) == 1:
        result = "000" + rawID
    elif len(rawID) == 2:
        result = "00" + rawID
    elif len(rawID) == 3:
        result = "0" + rawID
    else:
        print('Unexpected Device ID. Terminating.')
        sys.exit(1)

    return result
    
def findValuesInRegistry(ID):

    path = r'SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}\%s\Ndi\params\*SpeedDuplex\enum' % ID
    isValid = False
    try:
        hKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
        isValid = True
    except:
        pass

    modes = []        
    if isValid:
        for n in range(20):
            enum = []
            
            try:
                result = winreg.QueryValueEx(hKey, str(n))
                enum.append(result[0])
                enum.append(n)
                modes.append(enum)
            except:
                pass

    return (modes, isValid)

    
def findModeValues_Eng(modes_, ifID):

    actualModes = []
    sender = []
    
    speed = ''
    for str, id in modes_:
        for regex, speed in speedFormat:
            reSpeed = re.search(regex, str, re.M | re.I)
            if reSpeed:
                actualModes.append([id, 'ENG', speed])
                senderValue = '"%s" hw.net.driver.Speed[%s,%s] "%s"' % (host, ifID, id, speed)
                sender.append(senderValue)

    return (sender, actualModes)

    
def findModeValues_Any(modes_, ifID):
    intermediateModes = []
    actualModes = []
    sender = []
    
    for i in modes_:
        reVal = re.search(r'^(\d+)', i[0], re.M | re.I)
        if reVal:
            intermediateModes.append([reVal.group(1), i[1]])
    
    lastValue = None
    for rSpeed, id in intermediateModes:
        if      rSpeed == '10':
            speed = 10000000
        elif    rSpeed == '100':
            speed = 100000000
        elif  ( lastValue == '100'  and
               (rSpeed   == '1'     or
                rSpeed   == '1.0')):
            speed = 1000000000
        elif  ((lastValue == '1'    or
                lastValue == '1.0') and
                rSpeed    == '10'):
            speed = 10000000000
        elif    rSpeed    == '25':
            speed = 25000000000
        elif    rSpeed    == '40':
            speed = 40000000000
        elif    rSpeed    == '50':
            speed = 50000000000
        elif  ((lastValue == '40'   or
                lastValue == '50')  and
                rSpeed    == '100'):
            speed = 100000000000

        actualModes.append([id, rSpeed, speed])
        senderValue = '"%s" hw.net.driver.Speed[%s,%s] "%s"' % (host, ifID, id, speed)
        sender.append(senderValue)
        
        lastValue = rSpeed
        
    return (sender, actualModes)


def parseModes(modes_, ID):
    json = []
    sender = []

    for i in modes_:

        senderValue = '"%s" hw.net.driver.Mode[%s,%s] "%s"' % ( host, ID, i[1], i[0] )
        sender.append(senderValue)
        json.append({'{#IFID}':ID, '{#MODEID}':str(i[1])})
        
    return(json, sender)


def findMaxSpeed(modes_, block_):

    isManualProduct = findManualMaxSpeed(block_)
    if isManualProduct:
        maxSpeed = isManualProduct
    elif modes_:
        speeds = []
        for i in modes_:
            speeds.append(i[2])
        speeds.sort()
        
        maxSpeed = max(speeds)
    else:
        maxSpeed = None
        
    return maxSpeed
        

def findManualMaxSpeed(block_):
    reProductName = re.search(r'^ProductName=(.+)', block_, re.I | re.M)

    if reProductName:
        for i in manualMaxSpeed:
            if reProductName.group(1).strip() == i[0]:
                return i[1]
    else:
        return None
        
        
def findState(modes_, block, allBlocks_):

    sender = []

    ifID = rawToFull_ifID(findRaw_ifID(block))
    currentSpeed = findSpeed(block)
    if currentSpeed:
        currentSpeed = int(currentSpeed)
        
    maxSpeed_out = findMaxSpeed(modes_, block)

    if isBridge(block):
        state = 'BRIDGE'
    elif not currentSpeed:
        hypervMac = findHypervMAC(allBlocks_)
        if hypervMac:
            raw_ifID = findVirtual_ifID(allBlocks_, hypervMac)
            physical_ifID = rawToFull_ifID(raw_ifID)
            
            state = 'HYPERV_PHYSICAL_POINTS_TO_%s' % physical_ifID
            
            speed = findSpeedByID(allBlocks_, raw_ifID)

            sender.append('"%s" hw.net.wmi.Speed[%s] "%s"' % (host, ifID, speed))
        else:
            state = 'NO_SPEED'
    elif isHyperV(block):
            virtualMac = findMac(block)
            raw_ifID = findPhysical_ifID(allBlocks_, virtualMac)
            virtual_ifID = rawToFull_ifID(raw_ifID)
            
            state = 'HYPERV_VIRTUAL_POINTS_TO_%s' % virtual_ifID

    elif not modes_:
        state = 'NO_MODES'
    elif currentSpeed == 9223372036854775807:
        state = 'INVALID_SPEED_OVERFLOW'
    elif maxSpeed_out < currentSpeed:
        state = 'SPEED_HIGHER_THAN_MODE'
    elif not maxSpeed_out == currentSpeed:
        state = 'DEGRADED'
    else:
        state = 'PROCESSED'

    sender.append('"%s" hw.net.Status[%s] "%s"' % (host, ifID, state))

    return sender

    
def isBridge(block_):
    reService = re.search(r'^ServiceName=NdisImPlatformMp$', block_, re.I | re.M)
    if reService:
        return True
    else:
        return False
    
    
def isHyperV(block_):
    reService = re.search(r'^ServiceName=VMSMP$', block_, re.I | re.M)
    if reService:
        return True
    else:
        return False
    
    
def findHypervMAC(allBlocks_):

    for b in allBlocks_: 
        if isHyperV(b):
            return findMac(b)

    return None
    
    
def findMac(block_):
    reMac = re.search(r'^MACAddress=(.+)'   , block_, re.I | re.M)
    if reMac:
        return reMac.group(1)
    else:
        return None
    
    
def findPhysical_ifID(allBlocks_, mac):
    matchMac = r'^MACAddress=%s$' % mac

    for b in allBlocks_:
        reService = re.search(r'^ServiceName=VMSMP$', b, re.I | re.M)
        reMac = re.search(matchMac, b, re.I | re.M)
        if  (    reMac and
             not reService):
            
            return findRaw_ifID(b)
            
    return None
        

def findVirtual_ifID(allBlocks_, mac):
    matchMac = r'^MACAddress=%s$' % mac

    for b in allBlocks_:
        reService = re.search(r'^ServiceName=VMSMP$', b, re.I | re.M)
        reMac = re.search(matchMac, b, re.I | re.M)
        if  (reMac and
             reService):
            
            return findRaw_ifID(b)
            
    return None
        
        
def findSpeed(block_):
    reSpeed = re.search(r'^Speed=(\d+)', block_, re.I | re.M)
    if reSpeed:
        return reSpeed.group(1)
    else:
        return None
        
        
def findSpeedByID(allBlocks_, raw_ifID_):
    ifMatch = '^DeviceID=%s$' % raw_ifID_

    for b in allBlocks_:
        reID = re.search(ifMatch, b, re.M | re.I)
        if  reID:
            return findSpeed(b)
            
    return None


if __name__ == '__main__':
    fail_ifNot_Py3()

    host = str(sys.argv[2])

    jsonData = []
    senderData = []
    
    p_out = wmiNetRun(cmd.split())
    allBlocks = splitBlocks(p_out[0])
    for b in allBlocks:
        ifID = rawToFull_ifID(findRaw_ifID(b))
        
        findValuesInWMI_out = findValuesInWMI(ifID, b)
        if not findValuesInWMI_out:
            continue

        jsonData.append({'{#ID}':ifID})
        
        values_out = findValuesInRegistry(ifID)
        validity = values_out[1]
        modes = values_out[0]

        senderModes = findModeValues_Eng(modes, ifID)
        if not senderModes[0]:
            senderModes = findModeValues_Any(modes, ifID)
        
        senderData.extend(senderModes[0])
        parsed_modes_out = parseModes(modes, ifID)
        jsonData.extend(parsed_modes_out[0])
        if parsed_modes_out[1]:
            senderData.extend(parsed_modes_out[1])
            
        if findValuesInWMI_out:
            senderData.extend(findValuesInWMI_out)
            currentSpeed = findSpeed(b)
            connState = findState(senderModes[1], b, allBlocks)
            senderData.extend(connState)

    link = 'https://github.com/nobodysu/zabbix-hardware'
    sendStatusKey = 'hw.net.info[SendStatus]'
    processData(senderData, jsonData, agentConf, senderPyPath, senderPath, delay, host, link, sendStatusKey)
