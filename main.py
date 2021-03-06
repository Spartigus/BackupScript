# Python imports
import shutil
from datetime import date
import os
import sys
from os import path
from os import walk
import logging

# Local imports
from dotenv import load_dotenv


# Return the values of the source and backup directories from the environment variable folder
load_dotenv()
source_dir = str(os.getenv("SRC_DIR"))
backup_dir = str(os.getenv("BASE_BACKUP_DIR"))


# Return todays date to name the backup folder
today = date.today()
date_format = today.strftime("%d_%b_%Y")
dest_dir = backup_dir + "/" + str(today)


# Backup files to a folder named todays date with CLI output
def perform_backup():
    total_size, files_backup = get_backup_size()
    print(
        "Backup Starting \nTotal files for backup: %s \nTotal size to backup: %s MB"
        % (files_backup, str("{0:.2f}".format(total_size)))
    )
    shutil.copytree(source_dir, dest_dir, ignore=log_path)
    print("Backup completed")


# Returns the folders in the directory and deletes the oldest one if there is more than 5 backups
def get_folders():
    # Returns a list of directories in the backup directory
    dir_raw_list = os.listdir(backup_dir)
    dir_list = []

    # Exclude the hidden files and creates a processed list of the the contents of the backup directory
    for dir in dir_raw_list:
        if "." not in dir:
            dir_list.append(dir)

    # Determines if there is more than 5 backups and deletes the oldest one with CLI output
    if len(dir_list) > 5:
        dir_list.sort()
        print("Deleting oldest backup dated: ", dir_list[0])
        oldest_backup = backup_dir + "/" + (dir_list[0])
        shutil.rmtree(oldest_backup)


# Returns the size of the backup source in megabytes, this includes hidden folders
def get_backup_size():
    total_size = 0
    files_backup = 0

    # Itterates through the entire directory to add the size of each file up
    for path, dirs, files in os.walk(source_dir):
        for f in files:
            fp = os.path.join(path, f)
            total_size += os.path.getsize(fp)
            files_backup += 1

    return total_size / 1024**2, files_backup


# Returns the size of the backup output in megabytes, this includes hidden folders
def output_size():
    backup_size = 0
    file_count = 0

    # Itterates through the entire directory to add the size of each file up
    for path, dirs, files in os.walk(dest_dir):
        for f in files:
            fp = os.path.join(path, f)
            backup_size += os.path.getsize(fp)
            file_count += 1

    return backup_size / 1024**2, file_count


# Logging function in shutil to display information at each operation
def log_path(path, names):
    # Getting variables used to generate CLI output informaton
    cur_dir = str(path)
    backup_size, backup_files = output_size()
    source_size, source_files = get_backup_size()

    # Handling a path longer than 50 chars for displaying correctly
    if len(cur_dir) > 50:
        dis_dir = (
            "Current: "
            + cur_dir[0:20]
            + "..."
            + cur_dir[len(cur_dir) - 30 : len(cur_dir)]
            + " |----| Progress: "
            + str("{0:.2f}".format(backup_size))
            + "/"
            + str("{0:.2f}".format(source_size))
            + " MB"
            + " | "
            + str("{0:.4f}".format(backup_size / source_size * 100))
            + "%"
        )

    else:
        dis_dir = (
            "Current: "
            + cur_dir
            + " |----| Progress: "
            + str("{0:.2f}".format(backup_size))
            + "/"
            + str("{0:.2f}".format(source_size))
            + " MB"
            + " | "
            + str("{0:.4f}".format(backup_size / source_size * 100))
            + "%"
        )

    # This variable is the result of the above to generate the CLI output info
    out_string = dis_dir

    # Displaying the CLI output to the user and refreshing the same line
    print(out_string, end="\r")
    sys.stdout.flush()

    # nothing will be ignored
    return []


# Logic to run the program and ensures a backup wasn't done already today
if path.exists(dest_dir):
    print("A backup has been completed today already.")

else:
    # Runs the backup process if the directories exist
    if path.exists(source_dir) and path.exists(backup_dir):
        get_folders()
        perform_backup()
    else:
        print("Backup source or destination do not exist.")
