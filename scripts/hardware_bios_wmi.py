## Installation instructions: https://github.com/nobodysu/zabbix-hardware ##

senderPyPath = r'C:\zabbix-agent\scripts\sender_wrapper.py'

agentConf = r'C:\zabbix_agentd.conf'

senderPath = r'C:\zabbix-agent\bin\win32\zabbix_sender.exe'

## Advanced configuration ##

cmd = ['wmic','BIOS','list','full']

globalTimeout = 25

keysandRegexp = (
    ('hw.bios.BiosCharacteristics',     r'^BiosCharacteristics\=(.+)'),
    ('hw.bios.BuildNumber',             r'^BuildNumber\=(.+)'),
    ('hw.bios.CodeSet',                 r'^CodeSet\=(.+)'),
    ('hw.bios.CurrentLanguage',         r'^CurrentLanguage\=(.+)'),
    ('hw.bios.Description',             r'^Description\=(.+)'),
    ('hw.bios.IdentificationCode',      r'^IdentificationCode\=(.+)'),
    ('hw.bios.InstallableLanguages',    r'^InstallableLanguages\=(.+)'),
    ('hw.bios.InstallDate',             r'^InstallDate\=(.+)'),
    ('hw.bios.LanguageEdition',         r'^LanguageEdition\=(.+)'),
    ('hw.bios.ListOfLanguages',         r'^ListOfLanguages\=(.+)'),
    ('hw.bios.Manufacturer',            r'^Manufacturer\=(.+)'),
    ('hw.bios.Name',                    r'^Name\=(.+)'),
    ('hw.bios.OtherTargetOS',           r'^OtherTargetOS\=(.+)'),
    ('hw.bios.PrimaryBIOS',             r'^PrimaryBIOS\=(.+)'),
    ('hw.bios.ReleaseDate',             r'^ReleaseDate\=(.+)'),
    ('hw.bios.SerialNumber',            r'^SerialNumber\=(.+)'),
    ('hw.bios.SMBIOSBIOSVersion',       r'^SMBIOSBIOSVersion\=(.+)'),
    ('hw.bios.SMBIOSMajorVersion',      r'^SMBIOSMajorVersion\=(.+)'),
    ('hw.bios.SMBIOSMinorVersion',      r'^SMBIOSMinorVersion\=(.+)'),
    ('hw.bios.SMBIOSPresent',           r'^SMBIOSPresent\=(.+)'),
    ('hw.bios.SoftwareElementID',       r'^SoftwareElementID\=(.+)'),
    ('hw.bios.SoftwareElementState',    r'^SoftwareElementState\=(.+)'),
    ('hw.bios.Status',                  r'^Status\=(.+)'),
    ('hw.bios.TargetOperatingSystem',   r'^TargetOperatingSystem\=(.+)'), 
    ('hw.bios.Version',                 r'^Version\=(.+)'),
)

#Info from https://docs.microsoft.com/en-us/windows/desktop/cimwin32prov/win32-bios
biosCharacteristics = (
    ('0', '0 Reserved'),
    ('1', '1 Reserved'),
    ('2', '2 Unknown'),
    ('3', '3 BIOS Characteristics Not Supported'),
    ('4', '4 ISA is supported'),
    ('5', '5 MCA is supported'),
    ('6', '6 EISA is supported'),
    ('7', '7 PCI is supported'),
    ('8', '8 PC Card (PCMCIA) is supported'),
    ('9', '9 Plug and Play is supported'),
    ('10', '10 APM is supported'),
    ('11', '11 BIOS is Upgradable (Flash)'),
    ('12', '12 BIOS shadowing is allowed'),
    ('13', '13 VL-VESA is supported'),
    ('14', '14 ESCD support is available'),
    ('15', '15 Boot from CD is supported'),
    ('16', '16 Selectable Boot is supported'),
    ('17', '17 BIOS ROM is socketed'),
    ('18', '18 Boot From PC Card (PCMCIA) is supported'),
    ('19', '19 EDD (Enhanced Disk Drive) Specification is supported'),
    ('20', '20 Int 13h - Japanese Floppy for NEC 9800 1.2mb (3.5, 1k Bytes/Sector, 360 RPM) is supported'),
    ('21', '21 Int 13h - Japanese Floppy for Toshiba 1.2mb (3.5, 360 RPM) is supported'),
    ('22', '22 Int 13h - 5.25 / 360 KB Floppy Services are supported'),
    ('23', '23 Int 13h - 5.25 /1.2MB Floppy Services are supported'),
    ('24', '24 Int 13h - 3.5 / 720 KB Floppy Services are supported'),
    ('25', '25 Int 13h - 3.5 / 2.88 MB Floppy Services are supported'),
    ('26', '26 Int 5h, Print Screen Service is supported'),
    ('27', '27 Int 9h, 8042 Keyboard services are supported'),
    ('28', '28 Int 14h, Serial Services are supported'),
    ('29', '29 Int 17h, printer services are supported'),
    ('30', '30 Int 10h, CGA/Mono Video Services are supported'),
    ('31', '31 NEC PC-98'),
    ('32', '32 ACPI supported'),
    ('33', '33 USB Legacy is supported'),
    ('34', '34 AGP is supported'),
    ('35', '35 I2O boot is supported'),
    ('36', '36 LS-120 boot is supported'),
    ('37', '37 ATAPI ZIP Drive boot is supported'),
    ('38', '38 1394 boot is supported'),
    ('39', '39 Smart Battery supported'),
)

softwareElementState = (
    ('0', 'Deployable'),
    ('1', 'Installable'),
    ('2', 'Executable'),
    ('3', 'Running'),
)

targetOS = (
    ('0', 'Unknown'),
    ('1', 'Other'),
    ('2', 'MACOS'),
    ('3', 'ATTUNIX'),
    ('4', 'DGUX'),
    ('5', 'DECNT'),
    ('6', 'Digital Unix'),
    ('7', 'OpenVMS'),
    ('8', 'HPUX'),
    ('9', 'AIX'),
    ('10', 'MVS'),
    ('11', 'OS400'),
    ('12', 'OS/2'),
    ('13', 'JavaVM'),
    ('14', 'MSDOS'),
    ('15', 'WIN3x'),
    ('16', 'WIN95'),
    ('17', 'WIN98'),
    ('18', 'WINNT'),
    ('19', 'WINCE'),
    ('20', 'NCR3000'),
    ('21', 'NetWare'),
    ('22', 'OSF'),
    ('23', 'DC/OS'),
    ('24', 'Reliant UNIX'),
    ('25' 'SCO UnixWare'),
    ('26', 'SCO OpenServer'),
    ('27', 'Sequent'),
    ('28', 'IRIX'),
    ('29', 'Solaris'),
    ('30', 'SunOS'),
    ('31', 'U6000'),
    ('32', 'ASERIES'),
    ('33', 'TandemNSK'),
    ('34', 'TandemNT'),
    ('35', 'BS2000'),
    ('36', 'LINUX'),
    ('37', 'Lynx'),
    ('38', 'XENIX'),
    ('39', 'VM/ESA'),
    ('40', 'Interactive UNIX'),
    ('41', 'BSDUNIX'),
    ('42', 'FreeBSD'),
    ('43', 'NetBSD'),
    ('44', 'GNU Hurd'),
    ('45', 'OS9'),
    ('46', 'MACH Kernel'),
    ('47', 'Inferno'),
    ('48', 'QNX'),
    ('49', 'EPOC'),
    ('50', 'IxWorks'),
    ('51', 'VxWorks'),
    ('52', 'MiNT'),
    ('53', 'BeOS'),
    ('54', 'HP MPE'),
    ('55', 'NextStep'),
    ('56', 'PalmPilot'),
    ('57', 'Rhapsody'),
    ('58', 'Windows 2000'),
    ('59', 'Dedicated'),
    ('60', 'VSE'),
    ('61', 'TPF'),
)

## End of configuration ##

import sys
import re
import subprocess
from sender_wrapper import (fail_ifNot_Py3, processData, removeQuotes)

def get_output(cmd_):

    err = None

    try:
        if      (sys.version_info.major == 3 and
                 sys.version_info.minor <= 2):

            p = subprocess.check_output(cmd_, universal_newlines=True)

            err = 'OLD_PYTHON32_OR_LESS'
        else:
            p = subprocess.check_output(cmd_, universal_newlines=True, timeout=globalTimeout)

    except subprocess.TimeoutExpired:
        err = 'TIMEOUT'

    except:
        p = ''

    return (p, err)

    
def findValues(p):
    sender = []
    
    for key, regexp in keysandRegexp:
        reVal = re.search(regexp, p, re.I | re.M)
        
        if reVal:
            val = reVal.group(1).strip()
            val = removeQuotes(val)
            
            if key == 'hw.bios.BiosCharacteristics':
                val = val.replace('{', '').replace('}', '')
                valTemp = ''
                
                charList = val.split(',')
                for i in charList:
                    for j in biosCharacteristics:
                        if i == j[0]:
                            valTemp = '%s %s%s' % (valTemp, j[1], r'\n')
                
                val = valTemp
            
            if key == 'hw.bios.SoftwareElementState':
                for i in softwareElementState:
                    if i[0] == val:
                        val = i[1]
                        
            if key == 'hw.bios.TargetOperatingSystem':
                for i in targetOS:
                    if i[0] == val:
                        val = i[1]

            sender.append('"%s" %s "%s"' % (host, key, val))

    return sender


if __name__ == '__main__':

    fail_ifNot_Py3()

    host = str(sys.argv[2])

    p_out_once = get_output(cmd)
    p_out = p_out_once[0]
    senderData = findValues(p_out)
    
    timeout = '0'

    link = 'https://github.com/nobodysu/zabbix-hardware'
    sendStatusKey = 'hw.bios.info[SendStatus]'
    processData(senderData, '', agentConf, senderPyPath, senderPath, timeout, host, link, sendStatusKey)
