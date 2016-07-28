#!/bin/bash

# This files configure cgroups to enable limitation of user processes, in terms
# of memory and cpu consumption.

# robust options
set -u # crash on undefined variables
set -e # crash on error commands

# get script directory
ETC_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/../etc"

# install cgroups related package
CGPKG="cgroup-bin"
if [ -z "$(dpkg -l | grep "ii  $CGPKG" || true)" ]; then
    sudo apt-get install "$CGPKG"
fi

# create cgroups config file and rules
CGCONF="/etc/cgconfig.conf"
if [ ! -e "$CGCONF" ]; then
    sudo cp "$ETC_DIR/$(basename "$CGCONF")" "$CGCONF"
fi

CGRULES="/etc/cgrules.conf"
if [ ! -e "$CGRULES" ]; then
    sudo cp "$ETC_DIR/$(basename "$CGRULES")" "$CGRULES"
fi

# create limited user group
LGROUP="limited_guest"
if [ -z "$(grep "$LGROUP" /etc/group)" ]; then
    sudo addgroup "$LGROUP"
fi

# create a service file for cgred and add it to startup
CGINIT="/etc/init.d/cgred"
if [ ! -e "$CGINIT" ]; then
    sudo cp "$ETC_DIR/$(basename "$CGINIT")" "$CGINIT"
    sudo chmod +x "$CGINIT"
    sudo update-rc.d cgred defaults
fi

# start cgred service
sudo $CGINIT restart

# hints
echo "HINT: add users to $LGROUP with 'sudo adduser user $LGROUP' to limit their processes"
echo "HINT: look at $CGCONF and adapt values to your needs and your computer"
