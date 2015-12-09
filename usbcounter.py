#!/usr/bin/env/ python
import datetime
import re
import subprocess

import smtplib
from email.mime.text import MIMEText

from sets import Set
import pymtp

def get_dcim_folder_id(device):
  for folder in device.get_parent_folders():
    if folder.name == "DCIM":
      print folder.folder_id
      return folder.folder_id

def getCurrentDevices(): 
    devices = []
    device_re = re.compile("""Bus\s+(?P<bus>\d+)\s+Device\s+
        (?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$""", re.I)
    df = subprocess.check_output("lsusb", shell=True)
    for i in df.split('\n'):
        if i:
            info = device_re.match(i)
            if info:
                dinfo = info.groupdict()
                dinfo['device'] = """/dev/bus/usb/%s/%s
                        """ % (dinfo.pop('bus'), dinfo.pop('device'))
                devices.append(dinfo)
    return devices 

BASELINE_DEVICES = getCurrentDevices()
NUM_DEVICES = len(BASELINE_DEVICES)

print "Startup successful!"


def loop(): 
    global BASELINE_DEVICES, NUM_DEVICES

    devices = getCurrentDevices()

    if (len(devices) > NUM_DEVICES):
        NUM_DEVICES = len(devices)
        server = smtplib.SMTP('smtp.gmail.com',587) 
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login('jimwaldoisthebestest@gmail.com','JimWaldo!!!')
        
        dcim_folder_id = 0
        dev_out = [] 
        for dev in devices: 
            if not dev in BASELINE_DEVICES: 
                dev_out.append(dev)
                try: 
                    # Connect to device
                    device = pymtp.MTP()
                    device.connect()

                    dcim_folder_id = get_dcim_folder_id(device)
                    print "DCIM folder id: %s" % dcim_folder_id
                    device.disconnect()
                except: 
                    pass
                    
        if (dcim_folder_id > 0): 
            msg = MIMEText(str(datetime.datetime.now()) + ' ' + 
                       str(dev_out) + "DCIM folder found.")
        else: 
            msg = MIMEText(str(datetime.datetime.now()) + ' ' + 
                       str(dev_out))
        msg['Subject'] = 'New USB device connected'
        msg['From'] = 'jimwaldoisthebestest@gmail.com'
        msg['To'] = 'jimwaldoisthebestest@gmail.com'
        server.sendmail('jimwaldoisthebestest@gmail.com', 
                        'jimwaldoisthebestest@gmail.com', 
                        msg.as_string())
        server.close()

        f = open('log_charging_usage.txt', 'a')
        f.write(str(datetime.datetime.now()) + ' ' + 
                    str(dev_out) + '\n\n')
        f.close()


    elif (len(devices) < NUM_DEVICES):
        NUM_DEVICES = len(devices)

if __name__ == "__main__":
    while 1:
        try:
            loop()
        except: 
            pass