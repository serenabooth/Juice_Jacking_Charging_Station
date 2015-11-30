from sets import Set
import pymtp

def get_dcim_folder_id(device):
  for folder in device.get_parent_folders():
    if folder.name == "DCIM":
      return folder.folder_id

def get_child_folders(device, parent_folder_id):
  folder_ids = Set([parent_folder_id])

  all_folders = device.get_folder_list()

  current_length = len(folder_ids)
  new_length = None
  while current_length != new_length:
    current_length = len(folder_ids)

    for key in all_folders:
      f = all_folders[key]
      if f.parent_id in folder_ids:
        folder_ids.add(f.folder_id)

    new_length = len(folder_ids)

  return folder_ids

def get_picture_file_list(device, folder_ids):
  picture_files = []
  for f in device.get_filelisting():
    if f.parent_id in folder_ids:
      picture_files.append(f)

  return picture_files

# Connect to device
device = pymtp.MTP()
device.connect()

print "\nConnected to device: %s" % device.get_devicename()

dcim_folder_id = get_dcim_folder_id(device)
print "DCIM folder id: %s" % dcim_folder_id

folder_ids = get_child_folders(device, dcim_folder_id)
print "Folder Ids: %s" % folder_ids

picture_files = get_picture_file_list(device, folder_ids)
for f in picture_files:
  print "Picture: %s - %s" % (f.filename, f.filesize)

device.disconnect()