#!/bin/bash - 
#=============================================================================
#          FILE: createlocalrepo.sh
#         USAGE: ./createlocalrepo.sh 
#   DESCRIPTION: 
#        AUTHOR: aldenso, aldenso@gmail.com
#      REVISION:  ---
#=============================================================================

#####################################
# Description: Set all configuration values with permitted values like those on
# the examples, of course it will take a lot time to finish, but it will create
# all needed directories and will download the packages, have in mind that it 
# needs some GB's available in FS for every distro you set.
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
urlremoterepo="" 				#ex: "mirrors.kernel.org/centos"
localrepodir=""					#ex: "/share"
outputfile="/tmp/localrepo.$(date +%F-%T)"
dirdistros=""					#ex: centos7 or "centos5 centos6 centos7"  
dirdistrossubset=""				#ex: "os" or "os addons extras updates"
dirdistrossubsetplatf=""		#ex: "i386" or "i386 x86_64"
#####################################
# Configuration -end
#####################################

#####################################
# Test Config
#####################################
touch "$outputfile"
echo "Program started on $(date +%F/%T)" > $outputfile

if [ ! -f $(which rsync > /dev/null 2>&1) ]
then
	echo "You don't have installed rsync, please install it."
	exit
fi

if [ -z "$urlremoterepo" ]
then 
	urlremoterepo=$(curl http://www.centos.org/download/full-mirrorlist.csv \
	> mirrorlist.csv 2>&1) >> $outputfile
	echo "You didn't set a remote repo, the mirror list have been"
	echo "downloaded for you, please check csv file on current directory"
	echo "and select an rsync one to set on \$localrepodir variable."
	exit
	cat $outputfile
else
	echo "Using Remote Repo: $urlremoterepo" >> $outputfile
fi

if [ -z "$localrepodir" ]
then 
	echo -e "Please set a localrepo directory (\$localrepodir)" >> $outputfile
	exit
else
	if [ ! -d "$localrepodir" ]
	then
		$(mkdir $localrepodir)
		for x in $dirdistros
			do	$(mkdir $localrepodir/$x)
			for i in $dirdistrossubset
				do mkdir $localrepodir/$x/$i
					for j in $dirdistrossubsetplatf; do mkdir $localrepodir/$x/$i/$j;done
				done
			done
		echo -e "localrepo directory set:\n$(tree $localrepodir)" >> $outputfile
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
					PKGORI="$urlremoterepo/$(echo $distro|sed s/'[a-z A-Z]'//g)/$subset/$platf"
					#PKGDST="$localrepodir/$distro/$subset/$platf"
					PKGDST="$localrepodir/$distro/$subset"
					echo "$(date +%F/%T): rsyncing $PKGORI $PKGDST " >> $outputfile
					rsync -a --delete --delete-excluded --exclude "local*" --exclude "isos" \
					rsync://$PKGORI $PKGDST >> $outputfile 2>&1
					echo "$(date +%F/%T): Previous rsyncing done." >> $outputfile
					done
			done
	done

echo "Script Finished. Please check outputfile: $outputfile"