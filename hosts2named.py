#!/usr/bin/python3
import re
import datetime
#Files Involved
hosts_file="/etc/hosts"
data_directories="/var/named/chroot/var/named/data"
nameserver="ns"
nameserverip="192.168.1.60"
domainname="adm"
zoneserial=datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')

# Variables
ipaddresses=dict()
zones=dict()
reverse_zones=dict()

def createZonesHeader():
#     $TTL 86400
#     @ IN SOA ns.adm. root.adm. (
#     2014101901; Serial
#     43200; Refresh
#     3600; Retry
#     3600000; Expire
#     2592000); Minimum
    print ("\t$TTL 86400")
    print ("\t@ IN SOA "+nameserver+"."+domainname+". root."+domainname+". (")
    print ("\t"+zoneserial+"; Serial")
    print ("\t43200; Refresh")
    print ("\t3600; Retry")
    print ("\t3600000; Expire")
    print ("\t2592000); Minimum")
    print ()
    
                
#Creates Zone Definitions for named.conf file 
def createNamedConfZone(zone):
    print ("zone \""+reverse_zones[zone]+".in-addr.arpa\" IN {")
    print ("\ttype master;")
    print ("\tfile \""+zone+".zone\";")
    print ("}")


def createReverseZonefile(zone):
    #with open('file_to_write', 'w') as f:
    #f.write('file contents')
    print ("Create Reverse Zone File "+data_directories+"/"+zone+".zone")
    createZonesHeader()
    print ("\t@ IN NS "+nameserver+"."+domainname+".")
    for myip in list(zones[zone]):
        #61 IN PTR uno.adm.
        ipbits=myip.split('.')
        print ("\t"+ipbits[3]+ " IN PTR " + ipaddresses[myip]+"."+domainname+".")


def createForwardZonefile(zones):
    print ("Create Forward Zone File "+data_directories+"/"+domainname+".zone")
    createZonesHeader()
    print ("\t@ IN NS "+nameserver+"."+domainname+".")
    print ("\t@ IN A "+nameserverip)
    print ("\tNS IN A "+nameserverip)
# @ IN NS ns.adm.
# @ IN A 192.168.1.60
# NS IN A 192.168.1.60
# 
# vmdnsserver IN A 192.168.1.60
# uno IN A 192.168.0.61

    for myzone in zones.keys():
        for myip in list(zones[myzone]):
            print ("\t"+ipaddresses[myip]+" IN A "+myip)        


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
    #print (">"+ip)
    tmpzone=ip.split('.')
    zone=tmpzone[0]+"."+tmpzone[1]+"."+tmpzone[2]
    reverse_zone=tmpzone[2]+"."+tmpzone[1]+"."+tmpzone[0]
    #print ("--->"+zone)
    try:
        if zones[zone]:
          zones[zone].append(ip)
           
            
    except:
        zones[zone]=list()
        zones[zone].append(ip)
        
    reverse_zones[zone]=reverse_zone     
    #ipaddresses.append(ipaddress)
    #print (ipaddress)

print ("\n\n---------------------------------------\n") 

    
for myzone in zones.keys():
    createNamedConfZone(myzone)
    
    print ("\n\n---------------------------------------\n")    
    
    createReverseZonefile(zone)
    
    print ("\n\n---------------------------------------\n")   
    
    print ("ZONE: ["+myzone+"] REVERSE_ZONE: ["+reverse_zones[myzone]+"]")
    #print (str(zones[myzone]))
    
    for myip in list(zones[myzone]):
        print ("\t -- "+myip+ " " + ipaddresses[myip])
    
    print ("\n\n---------------------------------------\n")

createForwardZonefile(zones)
        