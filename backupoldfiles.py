#!/usr/bin/python
# @Author: Aldo Sotolongo
# @Date:   2016-05-25T14:22:58-04:00
# @Email:  aldenso@gmail.com
# @Last modified by:   Aldo Sotolongo
# @Last modified time: 2016-08-21T22:11:05-04:00
# Description: small tool to make backups based on age in days

import datetime
import os
import zipfile
import zlib
from subprocess import Popen, PIPE

# Timestamp to compare age of files
a = datetime.datetime.now()
# Timestamp for names in zipfiles
backupts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

# Set the age in days for files you wish to backup and then remove from the
# original directory, change it to the desired age.
fileage = 90
# Set tuples for origin and destiny dir to backup
dirs2backup = [("/backups/prueba1_origin", "/backups/prueba1_destiny"),
               ("/backups/prueba2_origin", "/backups/prueba2_destiny")]


def checkdirs(dirs2backup):
    for dirs in dirs2backup:
        for dir in dirs:
            if os.path.exists(dir):
                continue
            else:
                print("Directory {} doesn't exists".format(dir))
                exit("Please create it")


def checkperm(dirs2backup):
    count = 0
    for dir in dirs2backup:
        dir2backup = dir[0]
        print("Checking permissions in: {}".format(dir2backup))
        files = os.listdir(dir2backup)
        files2backup = checkage(files, dir2backup)
        for file in files2backup:
            if not os.access(dir2backup + "/" + file, os.W_OK) or not \
             os.access(dir2backup + "/" + file, os.R_OK):
                count += 1
                print("You don't have the proper permissions on file: {}"
                      .format(file))
    if count != 0:
        exit("Check your permissions: {} permissions wrong".format(count))
    else:
        print("Permissions OK")


def checkage(files, dir2backup):
    list2backup = []
    for file in files:
        timestamp = os.lstat(dir2backup + "/" + file).st_mtime
        b = datetime.datetime.fromtimestamp(timestamp)
        age = (a - b).days
        if age >= fileage:
            list2backup.append(file)
    return list2backup


def createarchive(dir2copybackup, dir2backup, files2backup):
    if len(files2backup) == 0:
        print("Nothing to do for {}".format(dir2backup))
    else:
        archivefile = dir2copybackup + "/" + "backup_" + backupts + ".zip"
        print("#### Creating Archive: {} ####".format(archivefile))
        zf = zipfile.ZipFile(archivefile, mode="w")
        try:
            for file in files2backup:
                print("++++ adding {}".format(file))
                zf.write(dir2backup + "/" + file,
                         arcname=file,
                         compress_type=zipfile.ZIP_DEFLATED)
                cmd = "rm -f {0}/{1}".format(dir2backup, file)
                p = Popen(cmd, stdout=PIPE, shell=True)
                output, error = p.communicate()
                if not error:
                    print("---- {} archived and original deleted".format(file))
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            print("#### Report of files in archive ####")
            for file in zf.infolist():
                print("File Name:\t{}".format(file.filename))
                print("Created:\t{}"
                      .format(datetime.datetime(*file.date_time)))
                print("Compressed size:\t{}".format(file.compress_size))
                print("Uncompressed size:\t{}".format(file.file_size))
            print("#### Closing archive ####")
            zf.close()


def main(dirs2backup):
    checkdirs(dirs2backup)
    checkperm(dirs2backup)
    for dir in dirs2backup:
        dir2backup = dir[0]
        dir2copybackup = dir[1]
        files = os.listdir(dir2backup)
        files2backup = checkage(files, dir2backup)
        print("#" * 50)
        print("Dir_Origin: {0}\nDir_Destiny: {1}".format(dir[0], dir[1]))
        print("Files_to_backup:\n" + str(files2backup))
        createarchive(dir2copybackup, dir2backup, files2backup)
        archivefile = dir2copybackup + "/" + "backup_" + backupts + ".zip"
        if os.path.exists(archivefile):
            with open(dir2copybackup+"/backup_{}.log"
                      .format(backupts), "wb") as f:
                f.write("#"*50+"\n")
                f.write("Dir_Origin: {0}\nDir_Destiny: {1}\n"
                        .format(dir[0], dir[1]))
                f.write("Files_in_backup:\n")
                zf = zipfile.ZipFile(archivefile, mode="r")
                f.write("Filename\tCreated\tCompSize\tUncompSize\n")
                for file in zf.infolist():
                    filename = file.filename
                    createdtime = datetime.datetime(*file.date_time)
                    compressedsize = file.compress_size
                    uncompressedsize = file.file_size
                    f.write("{0}\t{1}\t{2}\t{3}\n"
                            .format(filename,
                                    createdtime,
                                    compressedsize,
                                    uncompressedsize))
                zf.close()
        else:
            print("No log file generated")

if __name__ == "__main__":
    main(dirs2backup)
