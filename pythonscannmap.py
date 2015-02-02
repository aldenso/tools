#!/usr/bin/env python2
import nmap, os

if os.geteuid() != 0:
    exit("For a good scan you need root privileges")

hosts = ['127.0.0.1', '192.168.0.107', '192.168.1.113']
ports = '22, 53, 68, 80, 111, 443'


def main(hosts, ports, arguments='-sS -sU'):
    for host in hosts:
        nm = nmap.PortScanner()
        try:
            nm.scan(host, str(ports), arguments)
            print("\n"+"#"*40+"\nHost scanned: {0}".format(host)+
                " State: {0}\n".format(nm[host].state())+"#"*40)
            for proto in nm[host].all_protocols():
                if proto == 'tcp' or proto == 'udp':  
                    scannedport = nm[host][proto].keys()
                    scannedport.sort()
                    print("#### Protocol: {0} ####".format(proto))
                    for sp in scannedport:
                        print("Port: {0}  State: {1}".format(int(sp),
                         nm[host][proto][sp]['state']) )
        except Exception as e:
            print("\n"+"#"*40 + "\nNot possible to scan: {0}\n".format(e)+ "#"*40)          
         

if __name__ == '__main__':
    main(hosts, ports)