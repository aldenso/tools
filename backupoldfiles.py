#/usr/bin/python

# Author: aldenso@gmail.com
# Description: small tool to make backups based on age in days

import datetime, os, zipfile

# Timestamp to compare age of files
a = datetime.datetime.now()
# Timestamp for names in zipfiles
backupts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

# Set the age in days for files you wish to backup and then remove from the original
# directory, change it to the desired age.
fileage = 90
# Set tuples for origin and destiny dir to backup 
dirs2backup = [("/home/aldo/prueba", "/tmp/prueba"),
               ("/tmp/prueba2_origin", "/tmp/prueba2")]

def checkage(files, dir2backup):
    list2backup = []
    for file in files:
        timestamp = os.lstat(dir2backup+"/"+file).st_mtime
        b = datetime.datetime.fromtimestamp(timestamp)
        age = (a-b).days
        if age >= fileage:
            list2backup.append(file)
    return list2backup

def createarchive(dir2copybackup, dir2backup, files2backup):
    archivefile = dir2copybackup+"/"+"backup_"+backupts+".zip"
    print("#### Creating Archive: {0} ####".format(archivefile))
    zf = zipfile.ZipFile(archivefile, mode="w")
    try:
        for file in files2backup:
            print("---> adding {0}".format(file))
            zf.write(dir2backup+"/"+file)
    except Exception as e:
        print("Error: {0}".format(e))
    finally:
        print("#### Closing archive ####")
        zf.close()


def main(dirs2backup):
    for dir in dirs2backup:
        dir2backup = dir[0]
        dir2copybackup = dir[1]
        files = os.listdir(dir2backup)
        files2backup = checkage(files, dir2backup)
        print("#"*50)
        print("Dir_Origin: {0}\nDir_Destiny: {1}".format(dir[0], dir[1]))
        print("Files_to_backup:\n"+str(files2backup))
        createarchive(dir2copybackup, dir2backup, files2backup)
        

if __name__ == "__main__":
    main(dirs2backup)
