import re
import subprocess
# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

NUM_DEVICES = 12

while (True): 
    device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
    df = subprocess.check_output("lsusb", shell=True)
    devices = []
    for i in df.split('\n'):
        if i:
            info = device_re.match(i)
            if info:
                dinfo = info.groupdict()
                dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                devices.append(dinfo)
    if (len(df.split('\n')) > NUM_DEVICES):
        server = smtplib.SMTP('smtp.gmail.com',587) #port 465 or 587
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login('jimwaldoisthebestest@gmail.com','JimWaldo!!!')
        #server.sendmail('jimwaldoisthebestest@gmail.com','jimwaldoisthebestest@gmail.com',str(devices))
        
        print len(df.split('\n'))
        print devices
        msg = MIMEText(str(devices))
        msg['Subject'] = 'New USB device connected'
        msg['From'] = 'jimwaldoisthebestest@gmail.com'
        msg['To'] = 'jimwaldoisthebestest@gmail.com'
        server.sendmail('jimwaldoisthebestest@gmail.com', 'jimwaldoisthebestest@gmail.com', msg.as_string())
        server.close()