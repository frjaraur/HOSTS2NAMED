#!/usr/bin/python3
import re
hosts_file="/etc/hosts"
data_directories="/var/named/chroot/var/named/data"


def createNamedConfZone(zone):
    print ("zone \"")


ipaddresses=dict()
zones=dict()
reverse_zones=dict()


for line in open(hosts_file,'r'):
    tmp=line.rstrip('|n')
    tmp=re.sub('\s+',' ',tmp)
    tmp=tmp.split(' ')
    ipaddress=tmp[0]
    ipname=tmp[1]
    if not ipaddress: continue
    if ":" in ipaddress: continue
    if "127.0.0.1" in ipaddress: continue
    
    try:
        
        if ipaddresses[ipaddress]:
            if ipaddresses[ipaddress] == ipname:
                print ("Duplicate lines for "+ipaddress+" and "+ipname)
            else:
                print ("Duplicate entry for "+ipaddress+" ("+ipaddresses[ipaddress]+" -- "+ipname+") not updating second value...")
            continue
    except:

        print ("Updating "+ipname+" with "+ipaddress)
        ipaddresses[ipaddress]=ipname
    
    
for ip in ipaddresses.keys():
    print (">"+ip)
    tmpzone=ip.split('.')
    zone=tmpzone[0]+"."+tmpzone[1]+"."+tmpzone[2]
    reverse_zone=tmpzone[2]+"."+tmpzone[1]+"."+tmpzone[0]
    print ("--->"+zone)
    try:
        if zones[zone]:
          zones[zone].append(ip)
           
            
    except:
        zones[zone]=list()
        zones[zone].append(ip)
        
    reverse_zones[zone]=reverse_zone     
    #ipaddresses.append(ipaddress)
    #print (ipaddress)
    
for myzone in zones.keys():
    print ("ZONE: ["+myzone+"] REVERSE_ZONE: ["+reverse_zones[myzone]+"]")
    print (str(zones[myzone]))
    for myip in list(zones[myzone]):
        print ("\t -- "+myip+ " " + ipaddresses[myip])
        