#!/bin/bash
#=============================================================================
# @File_name: menu_script_array.sh
# @Author: Aldo Sotolongo
# @Email: aldenso@gmail.com
# @Date:   2017-04-17 13:23:06
# @Last Modified by:   Aldo Sotolongo
# @Last Modified time: 2017-04-17 13:40:18
#=============================================================================

##############################################################################
# Functions
##############################################################################
show_menu() {
    clear
    echo "==================="    
    echo " M A I N - M E N U "
    echo "==================="
    echo "1) Option 1"
    echo "2) Menu 2"
    echo "3) quit"
}

read_options(){
    local choice
    read -p "Enter choice [ 1 - 3] " choice
    case $choice in
        1) 
            echo "Option 1 selected"
            sleep 2 # waiting
            show_menu
            ;;
        2) 
            show_menu2
            ;;
        3) 
            exit
            ;;
        *) 
            echo -e "${RED}Error...Invalid Option${STD}" && sleep 2
    esac
}


show_menu2(){
declare -a opt_IDX=()   # Initialize our arrays, to make sure they're empty.
declare -A opt_VAL=()     # Note that associative arrays require Bash version 4.
echo "line1" > tmp_file.txt
echo "line2" >> tmp_file.txt
echo "line3" >> tmp_file.txt
echo "line4" >> tmp_file.txt
readarray -t options < ./tmp_file.txt
rm tmp_file.txt

for i in "${!options[@]}"; do
    opt_IDX[$i]="${options[$i]%% *}"             # create an array of just names
    opt_VAL[${opt_IDX[$i]}]="${options[$i]#* }"   # map names to IPs
done

PS3='Select an option (any other choice will return to previous menu): '
select IDX in "${opt_IDX[@]}"; do
    case "$IDX" in
        "") 
            break
            ;;
        *)
            echo "Selected option is:"
            echo "${opt_VAL[$IDX]}"
            ;;
    esac
done
}

##############################################################################
# Traps for CTRL+C, CTRL+Z and quit
##############################################################################
# trap '' SIGINT SIGQUIT SIGTSTP

##############################################################################
# Main logic - Loop for the main menu
##############################################################################
while true
do
    show_menu
    read_options
done
