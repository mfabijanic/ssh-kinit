#!/usr/bin/env python3
#
# SSH kinit (Tier 1 and Tier 2)
#
# Author: Matej Fabijanic <root4unix@gmail.com>
#

import json
from getpass import getpass, getuser
from pykeepass import PyKeePass
from pykeepass.exceptions import CredentialsError
import os
import paramiko
import sys
import time


# TODO
# Change this `echo password | kinit`
def ssh_kinit(kp, keepass_entry, realm, host, ssh_port, ssh_timeout):
    # Tier 1
    if keepass_entry is not None and keepass_entry != "":
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            username = kp.find_entries(title=keepass_entry, first=True).username
            principal = ('%s@%s' % (username, realm))
            password = kp.find_entries(title=keepass_entry, first=True).password

            print('-' * 60)
            ssh.connect(host, port=ssh_port, username=username, password=password, timeout=ssh_timeout)
            print('SSH %s@%s: Connected' % (principal, host))

            stdin, stdout, stderr = ssh.exec_command("klist -s && echo '  Kerberos credentials cache is OK' || { echo '%s' | kinit %s &>/dev/null && echo 'KINIT OK'; }" %
                (password, principal))

            #time.sleep(0.1)
            print(stdout.read().decode())
            stdin.close()
            stdout.close()
            stderr.close()
            ssh.close()
        except AttributeError:
            print('ERROR: check if keepass_entry exist in database: "%s"' % keepass_entry)


def main():
    # Config
    with open('config.json', 'r') as f:
        config = json.load(f)

    keepass_filename = config['keepass']['filename']
    keepass_keyfile = config['keepass']['keyfile']
    ssh_port = config['ssh']['DEFAULT']['port']
    ssh_timeout = float(config['ssh']['DEFAULT']['timeout'])

    if ssh_timeout == '':
        ssh_timeout = float(3)
    if ssh_port == '':
        ssh_port = 22

    print('KeePass DB Filename: %s' % keepass_filename)

    # KeePass Master Password
    while True:
        try:
            kp = PyKeePass(keepass_filename, password=getpass(prompt='KeePass Master Password: ', stream=None), keyfile=keepass_keyfile)
            break
        except CredentialsError:
            print('The password you entered is incorrect.')

    print('SSH timeout: %s' % ssh_timeout)
    print()
    for host in config['hosts']:
        if 'disabled' not in config['hosts'][host]:
            keepass_entry = config['hosts'][host]['keepass_entry']
            realm = config['hosts'][host]['realm']
            # SSH kinit
            ssh_kinit(kp, keepass_entry, realm, host, ssh_port, ssh_timeout)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrupted')
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
