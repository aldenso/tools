#!/bin/bash
# @Author: Aldo Sotolongo
# @Date:   2016-05-25T13:52:59-04:30
# @Email:  aldenso@gmail.com
# @Last modified by:   Aldo Sotolongo
# @Last modified time: 2016-06-24T00:54:29-04:30
#####################################
# Description: creates an initial localrepo for centos, of course it will take
# a lot time to finish, but it will create all needed directories and will
# download the packages, have in mind that it needs some GB's available in FS
# for every distro you set.
# Todo: Add update only for previous repos.
#####################################


#####################################
# Check Privileges
#####################################
if [ $(id -u) -ne 0 ] && [ !$( env | grep "SUDO_UID") ]
	then
	echo "You need root privileges"
	exit
fi

#####################################
# Configuration
#####################################
urlremoterepo="" 				#ex: "//mirror.cisp.com/CentOS"
localrepodir=""					#ex: "/share"
outputfile="/tmp/localrepo.$(date +%F-%T)"
dirdistros=""					#ex: 7.2.1511 or "7.2.1511 6.8"
dirdistrossubset=""				#ex: "os" or "os addons extras updates"
dirdistrossubsetplatf=""		#ex: "i386" or "i386 x86_64"
#####################################
# Configuration -end
#####################################

#####################################
# Test Config
#####################################
touch "$outputfile"
echo "Program started on $(date +%F/%T)" | tee $outputfile

if [ ! -f $(which rsync > /dev/null 2>&1) ]
then
	echo "You don't have rsync installed, please install it."
	exit
fi

if [ -z "$urlremoterepo" ]
then
	urlremoterepo=$(curl https://www.centos.org/download/full-mirrorlist.csv \
	-o mirrorlist.csv 2>&1) | tee -a $outputfile
	sed -i '1d' mirrorlist.csv
	sed -i '$ d' mirrorlist.csv
	echo "You didn't set a remote repo, the mirror list have been"
	echo "downloaded for you, please check csv file on current directory"
	echo "and select an rsync one to set on \$localrepodir variable."
	exit
	cat $outputfile
else
	echo "Using Remote Repo: $urlremoterepo" | tee -a $outputfile
fi

if [ -z "$localrepodir" ]
then
	echo -e "Please set a localrepo directory (\$localrepodir)" | tee -a $outputfile
	exit
else
	if [ ! -d "$localrepodir" ]
	then
		mkdir "$localrepodir"
		for x in $dirdistros
			do	mkdir "$localrepodir"/"$x"
			for i in $dirdistrossubset
				do mkdir "$localrepodir"/"$x"/"$i"
					for j in $dirdistrossubsetplatf;
						do mkdir "$localrepodir"/"$x"/"$i"/"$j";done
				done
			done
		echo -e "localrepo directory set:\n$(tree $localrepodir)" | tee -a $outputfile
	fi
fi
#####################################
# Test Config - end
#####################################

#####################################
# starting download of repos
#####################################

for distro in $(ls $localrepodir)
	do
		for subset in $(ls $localrepodir/$distro)
			do
				for platf in $(ls $localrepodir/$distro/$subset)
					do
					PKGORI="$urlremoterepo/$distro/$subset/$platf"
					#PKGDST="$localrepodir/$distro/$subset/$platf"
					PKGDST="$localrepodir/$distro/$subset"
					echo "$(date +%F/%T): rsyncing $PKGORI $PKGDST " | tee -a $outputfile
					echo "$(date +%F/%T): rsyncing running in background." | tee -a $outputfile
					nohup rsync -a --delete --delete-excluded --exclude "local*" --exclude "isos" \
					rsync:$PKGORI $PKGDST & >> $outputfile 2>&1
					if [ "$?" -ne 0 ]
					then
						echo "Rsync connection refused." | tee -a $outputfile
					fi
					done
			done
	done

echo "Script Finished. Please check outputfile: $outputfile"
