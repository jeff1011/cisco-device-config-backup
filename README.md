# cisco-device-config-backup
this script uses paramiko to ssh into devices and scrape the running configuration

steps to install:
1. activate virtual environment
      source venv/bin/activate
2. install packages
      pip3 install -r requirements.txt
3. put device friendly name/ip address in 'devices.yml'
      
steps to use:
1. activate virtual environment
      source venv/bin/activate
2. run backup script
      python3 backup.py
