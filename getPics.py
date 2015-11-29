from sets import Set
import pymtp

def get_dcim_folder_id(device):
  for folder in device.get_parent_folders():
    if folder.name == "DCIM":
      return folder.folder_id

# Connect to device
device = pymtp.MTP()
device.connect()

print "\nConnected to device: %s" % device.get_devicename()

dcim_folder_id = get_dcim_folder_id(device)
print "DCIM folder id: %s" % dcim_folder_id

device.disconnect()