#!/usr/bin/env python3
import sys
import os
import time
import yaml
import base64
import paramiko
import datetime

    # ssh credentials
    # base64 encoded username and password - https://www.base64encode.org/
    username = 'USERNAME'
    password = 'PASSWORD'

if __name__ == '__main__':
    # current date/time
    now = datetime.datetime.now()
    date = '%.2i%.2i%.2i' % (now.year, now.month, now.day)
    if not os.path.exists('config/'+date):
        os.mkdir('config/'+date)

    # load config file
    try:
        with open('devices.yml') as f:
            config = yaml.safe_load(f)
    except:
        print("devices.yml file not found")
        sys.exit(1)

    for host in config['ssh']:
        try:
            hostname = host['name']
            host_ip = host['ip_address']

            #session start
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host_ip, username=str(base64.b64decode(username),'utf-8'), password=str(base64.b64decode(password),'utf-8'))
            
            #ssh shell
            shell = client.invoke_shell()
            time.sleep(2)
            
            #enter enable mode
            shell.send('enable\n')
            shell.send('\n')
            time.sleep(5)

            #terminal length for no paging 
            shell.send('terminal length 0\n')
            shell.send('terminal pager 0\n')
            shell.send('screen-length 0\n')
            time.sleep(2)
            
            #show running config and write output
            shell.recv(99999)
            shell.send('\nshow running-config\n')
            time.sleep(5)
            output = shell.recv(99999).decode('utf-8')

            # write to file
            f = open('config/'+date+'/'+hostname+'.cfg', 'w')
            f.write(output)
            f.close()
            
            #close ssh session
            client.close() 
            print("Successfully backed up config for "+hostname)
        except:
            print("\tError backing up config for "+hostname)
            continue