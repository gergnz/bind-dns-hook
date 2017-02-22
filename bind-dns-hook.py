#!/usr/bin/env python
import sys
import os
import datetime
from shutil import copyfile
from blockstack_zones import parse_zone_file,make_zone_file

format = "%Y%m%d"
serialprefix = datetime.datetime.today().strftime(format)

zonepath='/etc/bind/primary/'

def deploy_challenge(options):
    domain=options[2]
    token=options[4]

    zonefile = domain.split('.',1)[1]

    if os.path.isfile(zonepath+'db.'+zonefile):
        zf = zonepath+'db.'+zonefile
    elif os.path.isfile(zonepath+'db.'+domain):
        zf = zonepath+'db.'+domain
    else:
        print  >> sys.stderr, "no idea what file to use"
        quit(1)

    fd = open(zf, 'r')
    zfdata = parse_zone_file(fd.read())
    fd.close()
    oldserial=str(zfdata['soa'][0]['serial'])
    serialsuffix=str(00)
    if oldserial[:-2] == str(serialprefix):
        serialsuffix=str(int(oldserial[-2:])+1)

    newserial=serialprefix+serialsuffix.zfill(2)

    if not zfdata.has_key('txt'):
        zfdata['txt'] = []

    zfdata['txt'].append({'name': '_acme-challenge.'+domain+'.', 'txt': token})
    zfdata['soa'][0]['serial'] = newserial

    copyfile(zf, zf+'.'+oldserial)
    w = open(zf, 'w')
    w.write(make_zone_file(zfdata))

def clean_challenge(options):
    domain=options[2]
    token=options[4]

    zonefile = domain.split('.',1)[1]

    if os.path.isfile(zonepath+'db.'+zonefile):
        zf = zonepath+'db.'+zonefile
    elif os.path.isfile(zonepath+'db.'+domain):
        zf = zonepath+'db.'+domain
    else:
        print  >> sys.stderr, "no idea what file to use"
        quit(1)

    fd = open(zf, 'r')
    zfdata = parse_zone_file(fd.read())
    fd.close()
    oldserial=str(zfdata['soa'][0]['serial'])
    serialsuffix=str(00)
    if oldserial[:-2] == str(serialprefix):
        serialsuffix=str(int(oldserial[-2:])+1)

    newserial=serialprefix+serialsuffix.zfill(2)

    for i in range(len(zfdata['txt'])):
        if zfdata['txt'][i]['name'] == '_acme-challenge.'+domain+'.':
            zfdata['txt'].pop(i)

    zfdata['soa'][0]['serial'] = newserial

    copyfile(zf, zf+'.'+oldserial)
    w = open(zf, 'w')
    w.write(make_zone_file(zfdata))

def deploy_cert(options):
    quit()

def unchanged_cert(options):
    quit()

def invalid_challenge(options):
    quit()

def request_failure(options):
    quit()

def exit_hook(options):
    quit()

if __name__ == '__main__':
    locals()[sys.argv[1]](sys.argv)
