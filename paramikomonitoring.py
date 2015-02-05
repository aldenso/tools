#!/usr/bin/env python2
#
# File: paramikomonitoring.py
# Author: aldenso@gmail.com
# Description: This script is useful to create a menu based monitoring for
# servers with properly configured ssh
import paramiko, os, re

commands = ['df -h', 'free -m', 'tail -5 /var/log/messages']
menu = {}
ipaddr = ''
count=1
for command in commands:
    menu[count]=command
    count=count+1

def ExecuteCommands(answer, ipaddr):
    ssh = paramiko.SSHClient()
    #Remember to change hostkey in sshd to use rsa or dsa not ecdsa
    #otherwise it will indicate an error "not in known_hosts"
    ssh.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
    #It could be improved with authorized_hosts
    ssh.connect(ipaddr, username='test', password='test1234')
    if menu.get(answer):
        stdin, stdout, stderr = ssh.exec_command(menu.get(answer))
        for line in stdout.readlines():
            print(line)
        errors = []
        for line in stderr.readlines():
            errors.append(line)
            if len(errors) != 0:
                print("Error ==> {0}".format(errors))
    ssh.close()

def main():
    global ipaddr
    global answer
    answer=0
    print("Please indicate the IP to connect:\n")
    while answer == 0:
        try:
            answer = raw_input("Press (0) to exit.\n")
            if answer == '0':
                exit("Bye")
            # It can be improved
            elif not re.match(r'\d{1,3}\.\d{1,3}\.+\d{1,3}\.\d{1,3}', answer):
                print("[-] Format Not Accepted.")
                main()
            else:
                ipaddr=answer
        except Exception as e:
            print("Error ==> {}".format(e))

    print("#"*60+"\nPlease indicate the commands to execute:\n"+
        "in server: {0}\n".format(ipaddr)+"#"*60)
    answer=0
    count=1
    for command in commands:
        print("({0}) ==> {1}".format(count, command))
        count=count+1
    while answer == 0:
        try:
            answer = input("Press (0) to exit.\n"+
                "Press number of choice:")
            if answer == 0:
                exit("Bye")
            elif answer not in menu.keys():
                print("#"*30+"\nNot a valid choice\n"+"#"*30)
                print("Please select one option from previous list")
                answer=0
            else:
                ExecuteCommands(answer, ipaddr)
        except Exception as e:
            print("Error ==> {}".format(e))

if __name__ == '__main__':
    main()