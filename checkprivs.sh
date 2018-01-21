#!/bin/bash
#==============================================================================
# Author: Aldo Sotolongo
# Email:  aldenso@gmail.com
# Description: easy way to check root privileges in a script.
#==============================================================================

# Option 1: $EUID var
if [ "$EUID" -ne 0 ]
then
    echo "not root privileges - EUID"
else
    echo "root privileges - EUID"
fi

# Option 2: id command
if [ "$(id -u)" -ne 0 ]
then
    echo "not root privileges - ID"
else
    echo "root privileges - ID"
fi

# output:
# $ ./checkprivs.sh
# not root privileges - EUID
# not root privileges - ID
#
# $ sudo ./checkprivs.sh
# root privileges - EUID
# root privileges - ID
#
# # ./checkprivs.sh
# root privileges - EUID
# root privileges - ID
