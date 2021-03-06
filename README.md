# Backup Script

This script is designed to backup a specific folder onto a specific removable USB drive or location, each backup is saved by the date the script was run on. When the script is run, it searches the folder to see if a backup has been made that day already, as well as if the source and destination folders exist.

The script then scans the folder to see how far back the history goes, if there is more than 5 backups present, the script deletes the oldest backup. The script then commences backing up your files and displaying the relevant information.

To alter the location of the backup and the source folders, edit the .env file located in the repo.

Below is a screenshot of an example of the CLI display:

![Screenshot from 2022-04-15 17-17-52](https://user-images.githubusercontent.com/99443437/163538246-3be59ad7-9b29-4046-b6ce-3a1f5d241d67.png)
