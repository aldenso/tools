#/usr/bin/python

# Author: aldenso@gmail.com
# Description: small tool to make backups based on age in days

import datetime, os, zipfile, zlib

# Timestamp to compare age of files
a = datetime.datetime.now()
# Timestamp for names in zipfiles
backupts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

# Set the age in days for files you wish to backup and then remove from the original
# directory, change it to the desired age.
fileage = 90
# Set tuples for origin and destiny dir to backup 
dirs2backup = [("/tmp/prueba1_origin", "/tmp/prueba1_destiny"),
               ("/tmp/prueba2_origin", "/tmp/prueba2_destiny")]

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
    if len(files2backup) == 0:
        print("Nothing to do for {}".format(dir2backup))
    else:
        archivefile = dir2copybackup+"/"+"backup_"+backupts+".zip"
        print("#### Creating Archive: {} ####".format(archivefile))
        zf = zipfile.ZipFile(archivefile, mode="w")
        try:
            for file in files2backup:
                print("---> adding {}".format(file))
                zf.write(dir2backup+"/"+file, compress_type=zipfile.ZIP_DEFLATED)
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            print("#### Report of files in archive ####")
            for file in zf.infolist():
                print("File Name:\t{}".format(file.filename))
                print("Created:\t{}".format(datetime.datetime(*file.date_time)))
                print("Compressed size:\t{}".format(file.compress_size))
                print("Uncompressed size:\t{}".format(file.file_size))
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
