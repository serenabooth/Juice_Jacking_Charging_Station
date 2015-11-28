#!/usr/bin/env/ python
import datetime
import re
import subprocess
# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

def getCurrentDevices(): 
    devices = []
    device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
    df = subprocess.check_output("lsusb", shell=True)
    for i in df.split('\n'):
        if i:
            info = device_re.match(i)
            if info:
                dinfo = info.groupdict()
                dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                devices.append(dinfo)
    return devices 

BASELINE_DEVICES = getCurrentDevices()
NUM_DEVICES = len(BASELINE_DEVICES)

print "Startup successful!"
#print BASELINE_DEVICES
#print len(BASELINE_DEVICES)


def loop(): 
    global BASELINE_DEVICES, NUM_DEVICES

    devices = getCurrentDevices()

    if (len(devices) > NUM_DEVICES):
        NUM_DEVICES = len(devices)
        server = smtplib.SMTP('smtp.gmail.com',587) #port 465 or 587
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login('jimwaldoisthebestest@gmail.com','JimWaldo!!!')
        #server.sendmail('jimwaldoisthebestest@gmail.com','jimwaldoisthebestest@gmail.com',str(devices))
        

        dev_out = [] 
        for dev in devices: 
            if not dev in BASELINE_DEVICES: 
                dev_out.append(dev)

        #print dev_out
        #print len(devices)

        msg = MIMEText(str(datetime.datetime.now()) + ' ' + str(dev_out))
        msg['Subject'] = 'New USB device connected'
        msg['From'] = 'jimwaldoisthebestest@gmail.com'
        msg['To'] = 'jimwaldoisthebestest@gmail.com'
        server.sendmail('jimwaldoisthebestest@gmail.com', 'jimwaldoisthebestest@gmail.com', msg.as_string())
        server.close()

        f = open('log_charging_usage.txt', 'a')
        f.write(str(datetime.datetime.now()) + ' ' + str(dev_out) + '\n\n')
        f.close()


    elif (len(devices) < NUM_DEVICES):
        NUM_DEVICES = len(devices)

if __name__ == "__main__":
    while 1:
        loop()