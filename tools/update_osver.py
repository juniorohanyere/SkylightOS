#!/usr/bin/python3

# update_osver.py
# Created on Tue May 23 2023 by Seal Sealy (seal331)
# Codename "Esaul" Operating System
# Copyright (c) 2023 - SkylightOS Project

from os import chdir, popen
from os import path as ospath
from sys import *
import importlib.util as omport
from datetime import datetime
from getpass import getuser

abspath = ospath.abspath(__file__)
dname = ospath.dirname(abspath)
chdir(dname)
user = getuser()

majorminor = "1.0"

if ospath.isfile("SConstruct"):
    print('ERR: you are not running this script from the root SkylightOS directory')
    exit(1)

spec = omport.spec_from_file_location(
  "configo", dname + "/../build/config.py")

configo = omport.module_from_spec(spec)
spec.loader.exec_module(configo)

# if for some reason you need to override the automatic build number bump put it here instead of SPECIAL_NO
build_num_manual_override="SPECIAL_NO"

# there are accounts that would in the future produce automated builds of Skylight, that should exempted from having a username added to the build str
build_user_special_accounts = [
    "skvbl"
]

if len(argv) != 2:
    print(f'Usage: {argv[0]} read|update')
    exit(1)

if argv[1] == "read":
    with open(dname + "/../src/crt/sdk/system/osver.h", "a+") as osver_h:
        osver_h.seek(0)
        lines = osver_h.readlines()
        line = lines[7]
        if "fre" in line:
            print("fre")
            exit(0)
        elif "chk" in line:
            print("chk")
            exit(0)
        else:
            print("ERR: unable to find the build type! Is osver.h corrupt?")
            exit(1)

elif argv[1] == "update":
    if ospath.isfile(dname + '/../src/crt/sdk/system/osver.h'):
        with open(dname + '/../src/crt/sdk/system/osver.h') as f1:
            lines = f1.readlines()
            bnum = lines[-1]
            bnum = bnum.strip()
            bnum = bnum[17:]
            bnum = bnum[:-1]
            bnum = int(float(bnum))
        with open(dname + '/../src/crt/sdk/system/osver.h', 'w') as f2:
            f2.writelines(lines[:-7])
            f2.write(f'#define bld_type "{configo.config}"\n')
            f2.write(f'#define bld_lab "{popen("git symbolic-ref --short HEAD").read().strip()}"\n')
            f2.write(f'#define bld_arch "{configo.arch}"\n')
            stamp = datetime.today().strftime('%Y%m%d-%H%M')
            f2.write(f'#define bld_time "{stamp}"\n')
            f2.write(f'#define bld_majorminor "{str(majorminor)}"\n')
            for lab in build_user_special_accounts:
                if user != lab:
                    f2.write(f'#define bld_user "{str(user)}"\n')
                    break
                else:
                    f2.write(f'#define bld_user "__OFFICIAL__"\n')
                    break
            if build_num_manual_override != "SPECIAL_NO":
                f2.write(f'#define bld_num "{str(build_num_manual_override)}"\n')
            else:
                f2.write(f'#define bld_num "{str(bnum + 1)}.0"\n')
    else:
        with open(dname + '/../src/crt/sdk/system/osver.h', 'w') as f2:
            f2.write('/* osver.h\n')
            f2.write(' * Automatically Generated\n')
            f2.write(' * Codename "Esaul" Operating System\n')
            f2.write(' * Copyright (c) 2023 - SkylightOS Project\n')
            f2.write('*/\n')
            f2.write('\n')
            f2.write('// DO NOT TOUCH LINES BELOW - AUTOMATICALLY GENERATED - DO NOT DELETE, EVER!//\n')
            f2.write(f'#define bld_type "{configo.config}"\n')
            f2.write(f'#define bld_lab "{popen("git symbolic-ref --short HEAD").read().strip()}"\n')
            f2.write(f'#define bld_arch "{configo.arch}"\n')
            stamp = datetime.today().strftime('%Y%m%d-%H%M')
            f2.write(f'#define bld_time "{stamp}"\n')
            f2.write(f'#define bld_majorminor "{str(majorminor)}"\n')
            for lab in build_user_special_accounts:
                if user != lab:
                    f2.write(f'#define bld_user "{str(user)}"\n')
                    break
                else:
                    f2.write(f'#define bld_user "__OFFICIAL__"\n')
                    break
            if build_num_manual_override != "SPECIAL_NO":
                f2.write(f'#define bld_num "{str(build_num_manual_override)}"\n')
            else:
                f2.write(f'#define bld_num "1.0"\n')
exit(0)
