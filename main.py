# Python imports
import shutil
from datetime import date
import os
from os import path
from os import walk
from distutils.dir_util import copy_tree


# Setup the constant variables for the locations of files and backups
SRC_DIR = "/home/spartigus/Documents/Coding/Projects"
BASE_BACKUP_DIR = "/media/spartigus/Files"


# Get todays date to name the backup and location of the backup
today = date.today()
date_format = today.strftime("%d_%b_%Y")
dest_dir = BASE_BACKUP_DIR + "/" + str(today)


# Backup files function
def perform_backup():
    size = get_backup_size()
    print("Backup starting, total size is %s MB" % size)
    copy_tree(SRC_DIR, dest_dir)
    print("Backup completed")


# Gets the folders in the directory and deletes the oldest one if more than 5 backups
def get_folders():
    # Get list of files in the directory
    dir_raw_list = os.listdir("/media/spartigus/Files")
    dir_list = []

    # Exclude the hidden files and creates a processed list
    for dir in dir_raw_list:
        if "." not in dir:
            dir_list.append(dir)

    # Determines if there is more than 5 backups and deletes the oldest one
    if len(dir_list) > 5:
        dir_list.sort()
        print("Deleting oldest backup dated: ", dir_list[0])
        oldest_backup = base_dir + "/" + (dir_list[0])
        shutil.rmtree(oldest_backup)


# Get the size of the backup and returning this in megabytes. This includes hidden folders
def get_backup_size():
    total_size = 0

    # Itterates through the entire directory to add the size of each file up
    for path, dirs, files in os.walk(SRC_DIR):
        for f in files:
            fp = os.path.join(path, f)
            total_size += os.path.getsize(fp)

    return total_size / 1024**2


# Logic to run the program and ensures a backup wasn't done already today
if path.exists(dest_dir):
    print("Backup completed today already.")

else:
    # Runs the backup process
    get_folders()
    perform_backup()
