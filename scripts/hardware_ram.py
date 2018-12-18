## Installation instructions: https://github.com/nobodysu/noneyet ##

senderPyPath = r'C:\zabbix-agent\scripts\sender_wrapper.py'

agentConf = r'C:\zabbix_agentd.conf'

senderPath = r'C:\zabbix-agent\bin\win32\zabbix_sender.exe'

timeout = '80'


## Advanced configuration ##

unknownSlotShift = 1000
heavyDebug = False

# re.M | re.I
keysAndRegexps = (
                  ('hw.ram.BankName',      r'^BankLabel\=(.+)'),
                  ('hw.ram.Capacity',      r'^Capacity\=(\d+)'),
                  ('hw.ram.DeviceLocator', r'^DeviceLocator\=(.+)'),
                  ('hw.ram.FormFactor',    r'^FormFactor\=(\d+)'),
                  ('hw.ram.Manufacturer',  r'^Manufacturer\=(.+)'),
                  ('hw.ram.MemoryType',    r'^MemoryType\=(\d+)'),
                  ('hw.ram.PartNumber',    r'^PartNumber\=(.+)'),
                  ('hw.ram.SerialNumber',  r'^SerialNumber\=(.+)'),
                  ('hw.ram.Speed',         r'^Speed\=(\d+)'),
                  ('hw.ram.TotalWidth',    r'^TotalWidth\=(\d+)'),
                  ('hw.ram.TypeDetail',    r'^TypeDetail\=(\d+)'),
                 )

'''
TypeDetail
1 = Reserved
2 = Other
4 = Unknown
8 = Fast-paged
16 = Static column
32 = Pseudo-static
64 = RAMBUS
128 = Synchronous
256 = CMOS
512 = EDO
1024 = Window DRAM
2048 = Cache DRAM
4096 = Non-volatile
'''

'''
MemoryType
0 = Unknown
1 = Other
2 = DRAM
3 = Synchronous DRAM
4 = Cache DRAM
5 = EDO
6 = EDRAM
7 = VRAM
8 = SRAM
9 = RAM
10 = ROM
11 = Flash
12 = EEPROM
13 = FEPROM
14 = EPROM
15 = CDRAM
16 = 3DRAM
17 = SDRAM
18 = SGRAM
19 = RDRAM
20 = DDR
21 = DDR2
22 = DDR2 FB-DIMM
24 = DDR3
25 = FBD2
'''

'''
FormFactor
(0)    Unknown
(1)    Other
(2)    SIP
(3)    DIP
(4)    ZIP
(5)    SOJ
(6)    Proprietary
(7)    SIMM
(8)    DIMM
(9)    TSOP
(10)    PGA
(11)    RIMM
(12)    SODIMM
(13)    SRIMM
(14)    SMD
(15)    SSMP
(16)    QFP
(17)    TQFP
(18)    SOIC
(19)    LCC
(20)    PLCC
(21)    BGA
(22)    FPBGA
(23)    LGA
'''   

## End of configuration ##

import sys
import re
import subprocess
from sender_wrapper import (fail_ifNot_Py3, processData)


def removeQuotes(s):
    quotes = ["'", '"']

    for i in quotes:
        s = s.replace(i, '')

    return s


def wmiMemChipRun():
    sender = []

    try:
        p = subprocess.check_output(['wmic', 'path', 'cim_chip', 'get', '/value'], universal_newlines=True)
        #print(p)
    except:
        p = None

    p = p.replace('\n\n', '\n')

    if heavyDebug:
        sender.append('"%s" hw.ram.MEMORYCHIP_Output "%s"' % (host, p))   # broken newlines

    return (p, sender)


def splitBanks(p):
    split = p.split('\n\n\n')

    strip = [x for x in split if x.strip()]

    return strip


def findSlotNum(bank):
    bankLabelRe = re.search(r'^BankLabel\=(.+)', bank, re.M | re.I)
    if bankLabelRe:
        bankLabel = bankLabelRe.group(1)
        bankLabel = bankLabel.strip()
    else:
        bankLabel = False

    result = False
    if bankLabel:
        slotRe = re.search(r'(?:[\w-]+|\s+)(\d+)$', bankLabel)
        if slotRe:
            result = slotRe.group(1)

    return result


def findValues(slotNum, bank):
    sender = []

    for key, regexp in keysAndRegexps:
        reVal = re.search(regexp, bank, re.M | re.I)

        if reVal:
            val = reVal.group(1).strip()
            val = removeQuotes(val)

            sender.append('"%s" %s[slot%s] "%s"' % (host, key, slotNum, val))

    return sender


if __name__ == '__main__':
    fail_ifNot_Py3()

    host = str(sys.argv[2])

    senderData = []
    jsonData = []

    p_Once = wmiMemChipRun()
    p_Out = p_Once[0]
    p_SenderDebug = p_Once[1]

    if p_SenderDebug:
        senderData.extend(p_SenderDebug)

    bankBlocks = splitBanks(p_Out)

    for n, b in enumerate(bankBlocks):
        isRegularSlot = findSlotNum(b)
        if isRegularSlot:
            slot = isRegularSlot
        else:
            slot = str(n + unknownSlotShift)   # prevent collisions by shifting unknown banks

        bankSender = findValues(slot, b)

        if bankSender:
            senderData.extend(bankSender)
            jsonData.append({'{#BANKNUM}':slot})

    link = 'norepoyet'
    processData(senderData, jsonData, agentConf, senderPyPath, senderPath, timeout, host, link)
