senderPyPath = r'C:\zabbix-agent\scripts\sender_wrapper.py'

agentConf = r'C:\zabbix_agentd.conf'

senderPath = r'C:\zabbix-agent\bin\win32\zabbix_sender.exe'

timeout = '80'

unknownCPUshift = 1000

keysandRegexp = (
	('hw.cpu.AddressWidth',                 r'^AddressWidth\=(.+)'),
	('hw.cpu.Architecture',                 r'^Architecture\=(.+)'),
    ('hw.cpu.Availability',                 r'^Availability\=(.+)'),
	('hw.cpu.CpuStatus',                    r'^CpuStatus\=(.+)'),
    ('hw.cpu.CurrentClockSpeed',            r'^CurrentClockSpeed\=(.+)'),
    ('hw.cpu.CurrentVoltage',               r'^CurrentVoltage\=(.+)'),
	('hw.cpu.DataWidth',                    r'^DataWidth\=(.+)'),
	('hw.cpu.DeviceID',                     r'^DeviceID\=(.+)'),
	('hw.cpu.Family',                       r'^Family\=(.+)'),
	('hw.cpu.L2CacheSize',                  r'^L2CacheSize\=(\d+)'),
	('hw.cpu.L2CacheSpeed',                 r'^L2CacheSpeed\=(\d+)'),
	('hw.cpu.Level',                        r'^Level\=(.+)'),
    ('hw.cpu.LoadPercentage',               r'^LoadPercentage\=(.+)'),
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
    ('hw.cpu.VoltageCaps',                  r'^VoltageCaps\=(.+)'),
)
 
#Info from https://docs.microsoft.com/en-us/windows/desktop/cimwin32prov/win32-processor
architectureType = (
	('0', 'x86'),
	('1', 'MIPS'),
	('2', 'Alpha'),
	('3', 'PowerPC'),
	('5', 'ARM'),
	('6', 'ia64'),
	('9', 'x64'),
)

cpuAvailability = (
    ('1', 'Other'), 
    ('2', 'Unknown'), 
    ('3', 'Running/Full Power'),
    ('4', 'Warning'),
    ('5', 'In Test'),
    ('6', 'Not Applicable'), 
    ('7', 'Power Off'),
    ('8', 'Off Line'),
    ('9', 'Off Duty'),
    ('10', 'Degraded'),
    ('11', 'Not Installed'),
    ('12', 'Install Error'),
    ('13', 'Power Save - Unknown'),
    ('14', 'Power Save - Low Power Mode'),
    ('15', 'Power Save - Standby'),
    ('16', 'Power Cycle'),
    ('17', 'Power Save - Warning'),
    ('18', 'Paused'),
    ('19', 'Not Ready'),
    ('20', 'Not Configured'),
    ('21', 'Quiesced'),
)

cpuStatus = (
    ('0', 'Unknown'),
    ('1', 'CPU Enabled'),
    ('2', 'CPU Disabled by User via BIOS Setup'),
    ('3', 'CPU Disabled By BIOS (POST Error)'),
    ('4', 'CPU is Idle'),
    ('5', 'Reserved'),
    ('6', 'Reserved'),
    ('7', 'Other'),
)

powerManagementCapabilities = (
    ('0', 'Unknown'),
    ('1', 'Not Supported'),
    ('2', 'Disabled'),
    ('3', 'Enabled'),
    ('4', 'Power Saving Modes Entered Automatically'),
    ('5', 'Power State Settable'),
    ('6', 'Power Cycling Supported'),
    ('7', 'Timed Power On Supported'),
)

processorType = (
    ('1', 'Other'),
    ('2', 'Unknown'),
    ('3', 'Central Processor'),
    ('4', 'Math Processor'),
    ('5', 'DSP Processor'),
    ('6', 'Video Processor'),
)

processorFamily = (
    ('1', 'Other'),
    ('2', 'Unknown'),
    ('3', '8086'),
    ('4', '80286'),
    ('5', '80386'),
    ('6', '80486'),
    ('7', '8087'),
    ('8', '80287'),
    ('9', '80387'),
    ('10', '80487'),
    ('11', 'Pentium(R) brand'),
    ('12', 'Pentium(R) Pro'),
    ('13', 'Pentium(R) II'),
    ('14', 'Pentium(R) processor with MMX(TM) technology'),
    ('15', 'Celeron(TM)'),
    ('16', 'Pentium(R) II Xeon(TM)'),
    ('17', 'Pentium(R) III'),
    ('18', 'M1 Family'),
    ('19', 'M2 Family'),
    ('24', 'K5 Family'),
    ('25', 'K6 Family'),
    ('26', 'K6-2'),
    ('27', 'K6-3'),
    ('28', 'AMD Athlon(TM) Processor Family'),
    ('29', 'AMD(R) Duron(TM) Processor'),
    ('30', 'AMD29000 Family'),
    ('31', 'K6-2+'),
    ('32', 'Power PC Family'),
    ('33', 'Power PC 601'),
    ('34', 'Power PC 603'),
    ('35', 'Power PC 603+'),
    ('36', 'Power PC 604'),
    ('37', 'Power PC 620'),
    ('38', 'Power PC X704'),
    ('39', 'Power PC 750'),
    ('48', 'Alpha Family'),
    ('49', 'Alpha 21064'),
    ('50', 'Alpha 21066'),
    ('51', 'Alpha 21164'),
    ('52', 'Alpha 21164PC'),
    ('53', 'Alpha 21164a'),
    ('54', 'Alpha 21264'),
    ('55', 'Alpha 21364'),
    ('64', 'MIPS Family'),
    ('65', 'MIPS R4000'),
    ('66', 'MIPS R4200'),
    ('67', 'MIPS R4400'),
    ('68', 'MIPS R4600'),
    ('69', 'MIPS R10000'),
    ('80', 'SPARC Family'),
    ('81', 'SuperSPARC'),
    ('82', 'microSPARC II'),
    ('83', 'microSPARC IIep'),
    ('84', 'UltraSPARC'),
    ('85', 'UltraSPARC II'),
    ('86', 'UltraSPARC IIi'),
    ('87', 'UltraSPARC III'),
    ('88', 'UltraSPARC IIIi'),
    ('96', '68040'),
    ('97', '68xxx Family'),
    ('98', '68000'),
    ('99', '68010'),
    ('100', '68020'),
    ('101', '68030'),
    ('112', 'Hobbit Family'),
    ('120', 'Crusoe(TM) TM5000 Family'),
    ('121', 'Crusoe(TM) TM3000 Family'),
    ('122', 'Efficeon(TM) TM8000 Family'),
    ('128', 'Weitek'),
    ('130', 'Itanium(TM) Processor'),
    ('131', 'AMD Athlon(TM) 64 Processor Family'),
    ('132', 'AMD Opteron(TM) Family'),
    ('144', 'PA-RISC Family'),
    ('145', 'PA-RISC 8500'),
    ('146', 'PA-RISC 8000'),
    ('147', 'PA-RISC 7300LC'),
    ('148', 'PA-RISC 7200'),
    ('149', 'PA-RISC 7100LC'),
    ('150', 'PA-RISC 7100'),
    ('160', 'V30 Family'),
    ('176', 'Pentium(R) III Xeon(TM)'),
    ('177', 'Pentium(R) III Processor with Intel(R) SpeedStep(TM) Technology'),
    ('178', 'Pentium(R) 4'),
    ('179', 'Intel(R) Xeon(TM)'),
    ('180', 'AS400 Family'),
    ('181', 'Intel(R) Xeon(TM) processor MP'),
    ('182', 'AMD AthlonXP(TM) Family'),
    ('183', 'AMD AthlonMP(TM) Family'),
    ('184', 'Intel(R) Itanium(R) 2'),
    ('185', 'Intel Pentium M Processor'),
    ('190', 'K7'),
    ('200', 'IBM390 Family'),
    ('201', 'G4'),
    ('202', 'G5'),
    ('203', 'G6'),
    ('204', 'z/Architecture base'),
    ('250', 'i860'),
    ('251', 'i960'),
    ('260', 'SH-3'),
    ('261', 'SH-4'),
    ('280', 'ARM'),
    ('281', 'StrongARM'),
    ('300', '6x86'),
    ('301', 'MediaGX'),
    ('302', 'MII'),
    ('320', 'WinChip'),
    ('350', 'DSP'),
    ('500', 'Video Processor'),
)

statusInfo = (
    ('1', 'Other'),
    ('2', 'Unknown'),
    ('3', 'Enabled'),
    ('4', 'Disabled'),
    ('5', 'Not Applicable'),
)

upgradeMethod = (
    ('1', 'Other'),
    ('2', 'Unknown'),
    ('3', 'Daughter Board'),
    ('4', 'ZIF Socket'),
    ('5', 'Replacement/Piggy Back'),
    ('6', 'None'),
    ('7', 'LIF Socket'),
    ('8', 'Slot 1'),
    ('9', 'Slot 2'),
    ('10', '370 Pin Socket'),
    ('11', 'Slot A'),
    ('12', 'Slot M'),
    ('13', 'Socket 423'),
    ('14', 'Socket A (Socket 462)'),
    ('15', 'Socket 478'),
    ('16', 'Socket 754'),
    ('17', 'Socket 940'),
    ('18', 'Socket 939'),
)

voltageCaps = (
    ('1', '5'),
    ('2', '3.3'),
    ('4', '2.9'),
)

keysandParameters = (
    ('hw.cpu.Architecture',                 architectureType),
    ('hw.cpu.Availability',                 cpuAvailability),
    ('hw.cpu.CpuStatus',                    cpuStatus),
    ('hw.cpu.PowerManagementCapabilities',  powerManagementCapabilities),
    ('hw.cpu.ProcessorType',                processorType),
    ('hw.cpu.Family',                       processorFamily),
    ('hw.cpu.StatusInfo',                   statusInfo),
    ('hw.cpu.UpgradeMethod',                upgradeMethod),
    ('hw.cpu.VoltageCaps',                  voltageCaps),
)

import sys
import re
import subprocess
from sender_wrapper import (processData)


def findValues(cpuNum, cpu_out):
    sender = []
    
    for key, regexp in keysandRegexp:
        reVal = re.search(regexp, cpu_out, re.I | re.M)
        
        if reVal:
        
            val = reVal.group(1).strip()
            val = removeQuotes(val)

            for p_key, parameter in keysandParameters:
                if key == p_key:
                    for i in parameter:
                        if i[0] == val:
                            val = i[1]

            sender.append('"%s" %s[cpu%s] "%s"' %(host, key, cpuNum, val))

    return sender
    

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
