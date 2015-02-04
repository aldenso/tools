#!/usr/bin/env python2
import nmap, os, argparse, sys
from datetime import datetime

if os.geteuid() != 0:
    exit("For a good scan you need root privileges")

parser = argparse.ArgumentParser(description="Be aware of quotation marks"+
    " and special characters (\,-) use the examples")
parser.add_argument("--hosts", help="Indicate hosts to scan"+
 " example: '192.168.0.10' or '192.168.1.100 192.168.1.200'")
parser.add_argument("--flags", help="Indicate flags for nmap"+
    " example: '\-sL' or '-sS -sU'")
parser.add_argument("--ports", help="Indicate the ports to scan"+
    " example: '22' or '22-80' or '22, 68, 80'")
args = parser.parse_args()

if args.hosts:
    global hosts
    hosts = [i for i in args.hosts.split()]
else:
    hosts = ['127.0.0.1']

if args.flags:
    global arguments
    arguments = args.flags
else:
    arguments = '-sV'

if args.ports:
    global ports
    ports = args.ports
else:
    ports = None

if len(sys.argv) == 1:
    print("#"*60+"\nUSING DEFAULT VALUES\nhosts:{0}\n".format(hosts)+
        "ports:'Well Known Port list'\n"+
        "flags:'Service Version Detection'\n"+"#"*60)
else:
    if ports == None:
        wns = "Well Known Port list"
        print("#"*60+"\nUSING VALUES\nhosts:{0}\n".format(hosts)+
            "ports: {0}\n".format(wns)+
            "flags: {0}\n".format(arguments)+"#"*60)
    else:
        print("#"*60+"\nUSING VALUES\nhosts:{0}\n".format(hosts)+
            "ports: {0}\n".format(ports)+
            "flags: {0}\n".format(arguments)+"#"*60)

def main(hosts, ports, arguments):
    startdate, starttime = datetime.now().strftime('%Y/%m/%d %H:%M:%S').split()
    print("\n"+"#"*60+"\nScan Report started on {0}".format(
        startdate)+ " at {0}".format(starttime)+ "\n"+"#"*60)
    for host in hosts:
        nm = nmap.PortScanner()
        try:
            nm.scan("'"+host+"'", ports, arguments)
            print("\n"+"#"*60+"\nHost scanned: {0}".format(host)+
                " State: {0}\n".format(nm[host].state())+"#"*60)
            for proto in nm[host].all_protocols():
                if proto == 'tcp' or proto == 'udp':  
                    scannedport = nm[host][proto].keys()
                    scannedport.sort()
                    print("#### Protocol: {0} ####".format(proto))
                    for sp in scannedport:
                        if arguments == '-sV':
                            name = nm[host][proto][sp].get('name')
                            product = nm[host][proto][sp].get('product')
                            version = nm[host][proto][sp].get('version')
                            extrainfo = nm[host][proto][sp].get('extrainfo')
                            print("Port: {0}  State: {1}".format(int(sp),
                            nm[host][proto][sp]['state'])+
                            "\tName/Product: {0}/{1}".format(name, product)+
                            " Version/Extrainfo: {0}/{1}".format(version, extrainfo))
                        else:
                            print("Port: {0}  State: {1} Name: {2}".format(int(sp),
                            nm[host][proto][sp]['state'],
                            nm[host][proto][sp].get('name')))
        except Exception as e:
            print("\n"+"#"*60 + "\nNot possible to scan: {0}\n".format(e)+ "#"*60)
    enddate, endtime = datetime.now().strftime('%Y/%m/%d %H:%M:%S').split()
    print("\n"+"#"*60+"\nScan Report finished on {0}".format(
        enddate)+ " at {0}".format(endtime)+ "\n"+"#"*60)        
         

if __name__ == '__main__':
    main(hosts, ports, arguments)