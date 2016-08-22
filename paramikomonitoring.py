#!/usr/bin/python
# @Author: Aldo Sotolongo
# @Date:   2016-05-25T14:22:59-04:00
# @Email:  aldenso@gmail.com
# @Last modified by:   Aldo Sotolongo
# @Last modified time: 2016-08-22T16:29:31-04:00
# File: paramikomonitoring.py
# Description: This script is useful to create a menu based monitoring for
# servers with properly configured ssh

import os
import paramiko
import ipaddr as ip

commands = ['df -h', 'free -m', 'tail -5 /var/log/messages']
menu = {}
ipaddr = ''
count = 1
for command in commands:
    menu[count] = command
    count = count + 1


def ExecuteCommands(answer, ipaddr):
    ssh = paramiko.SSHClient()
    # Remember sometimes you need to change hostkey in sshd to use rsa or dsa
    # not ecdsa otherwise it will indicate an error "not in known_hosts"
    ssh.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
    # AutoAddPolicy is not the recommended way but is neccesary for some
    # systems that always indicate "not found in known_hosts"
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    private_key = os.path.expanduser('~/.ssh/id_rsa')
    mykey = paramiko.RSAKey.from_private_key_file(private_key)
    # ssh.connect(ipaddr, username='test', password='test1234')
    ssh.connect(ipaddr, username='test', pkey=mykey)
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
    answer = 0
    print("Please indicate the IP to connect:\n")
    while answer == 0:
        try:
            answer = raw_input("Press (0) to exit.\n")
            if answer == '0':
                exit("Bye")
            elif not ip.IPAddress(answer):
                # Generate exception for non ip values
                pass
            else:
                ipaddr = answer
        except Exception as e:
            print("Error ==> {}".format(e))
            main()

    print("#"*60+"\nPlease indicate the commands to execute:\n" +
          "in server: {0}\n".format(ipaddr)+"#"*60)
    answer = 0
    count = 1
    for command in commands:
        print("({0}) ==> {1}".format(count, command))
        count = count + 1
    while answer == 0:
        try:
            answer = input("Press (0) to exit.\n" +
                           "Press number of choice:")
            if answer == 0:
                exit("Bye")
            elif answer not in menu.keys():
                print("#"*30+"\nNot a valid choice\n"+"#"*30)
                print("Please select one option from previous list")
                answer = 0
            else:
                ExecuteCommands(answer, ipaddr)
        except Exception as e:
            print("Error ==> {}".format(e))

if __name__ == '__main__':
    main()
