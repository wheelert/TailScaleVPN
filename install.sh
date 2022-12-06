#!/bin/bash

APPDIR=/usr/share/TailScaleVPN

echo -e "\e[33m [ Checking for previous versions]\e[0m"
if [ -d "$APPDIR" ]; then
    rm -rf $APPDIR
    rm -rf /usr/share/applications/TailScaleVPN.desktop
    rm -rf /usr/share/polkit-1/actions/TailScaleVPN.policy
fi

#
# Check for dependencies
#
echo -e "\e[33m [ Checking for PyGObject]\e[0m"

if python3 -c 'import gi'; then
        echo -e "\e[32m         PyGObject Found\e[0m"
else
        echo -e "\e[31m         PyGObject Not Found trying install\e[0m"
        pip3 install PyGObject
fi

echo -e "\e[33m [ Checking for Handy]\e[0m"


if python3 -c 'import gi; gi.require_version("Handy","1");'; then
        echo -e "\e[32m         Handy Found\e[0m"
else
        echo -e "\e[31m         libHandy Not Found\e[0m"
	echo -e "\e[31m		please install libHandy > 1.0 \e[0m"
	echo -e "\e[31m [ exiting install ]\e[0m"
	exit
fi






echo -e "\e[32m [ Installing TailScaleVPN ]\e[0m"
mkdir $APPDIR
cp TailScaleVPN.py $APPDIR
cp tailscaleDB.py $APPDIR
cp TailScaleVPN.css $APPDIR
cp TailScaleVPN.png $APPDIR
cp TailScaleVPN $APPDIR
cp TailScaleVPN.desktop /usr/share/applications/
cp TailScaleVPN.policy /usr/share/polkit-1/actions/
