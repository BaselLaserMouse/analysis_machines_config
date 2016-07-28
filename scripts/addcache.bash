#!/bin/bash

# This scripts configures a persistent cache for network filesystems.
#
# /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\
# /!\                                                                         /!\
# /!\ This script will try to make a RAID0 partition for the cache, on        /!\
# /!\ provided disks, e.g. "addcache.bash /dev/sdc /dev/sdd".                 /!\
# /!\ Make sure that provided disks are not used for anything, i.e. mounted,  /!\
# /!\ and no important data is stored on them as they will be blanked.        /!\
# /!\                                                                         /!\
# /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\ /!\

# robust options
set -u # crash on undefined variables
set -e # crash on error commands

# install cachefilesd if not installed
CACHEPKG="cachefilesd"
if [ -z "$(dpkg -l | grep "ii  $CACHEPKG" || true)" ]; then
    sudo apt-get install "$CACHEPKG"
fi

# configure cachefilesd to start
if [ -z "$(grep '^RUN=yes' /etc/default/cachefilesd || true)" ]; then
    sudo sed -i 's/^#RUN=yes/RUN=yes/' /etc/default/cachefilesd
fi

# create cache partition mount point
CACHEDIR="/mnt/fscache"

if [ ! -d "$CACHEDIR" ]; then
    sudo mkdir "$CACHEDIR"
fi

# no RAID0 if only one drive is given
if [ "$#" -eq 1 ]; then
    CACHEDEV="$1"
else
    CACHEDEV="/dev/md0"
fi

# create cache system RAID0 partition
RAIDPKG="mdadm"

if [ ! -b "$CACHEDEV" ]; then

    for disk in $*; do
        if [ ! -b "$disk" ]; then
            echo "Block device ${disk} does not exist!"
            exit 1
        fi
    done

    # create  RAID partitions
    PARTITIONS=''
    for disk in $*; do
        sudo sgdisk -n 1 -t 1:FD "$disk";
        PARTITIONS="$PARTITIONS ${disk}1"
    done

    # install mdadm package if necessary
    if [ -z "$(dpkg -l | grep "ii  $RAIDPKG" || true)" ]; then
        sudo apt-get install  "$RAIDPKG"
    fi

    # create RAID0 array and save its configuration
    sudo mdadm --create --verbose "$CACHEDEV" --level=stripe --raid-devices="$#" $PARTITIONS
    sudo sh -c "mdadm --detail --scan >> /etc/mdadm/mdadm.conf"
    sudo update-initramfs -u

    # format as ext4 partition
    sudo mkfs.ext4 "$CACHEDEV"

fi

# add entry to automount the cache at start
if [ -z "$(grep "$CACHEDIR" /etc/fstab)" ]; then
    sudo sh -c 'echo "# cache for cachefilesd" >> /etc/fstab'
    sudo sh -c "echo \"$CACHEDEV $CACHEDIR ext4 defaults 0 1\" >> /etc/fstab"
fi

# configure cachefilesd to use the new partition
if [ -z "$(grep '^dir $CACHEDIR' /etc/cachefilesd.conf || true)" ]; then
    sudo sed -i "s|^dir .*|dir $CACHEDIR|" /etc/cachefilesd.conf
fi

# mount cache file if necessary
if [ -z "$(mount | grep "$CACHEDIR" || true)" ]; then
    sudo mount "$CACHEDIR"
fi

# start cachefilesd service if necessary
if [ -z "$(pgrep cachefilesd  || true)" ]; then
  sudo /etc/init.d/cachefilesd start
fi

# disable OpLocks in cifs mounts to make cache working with M-drive
MODFILE="/etc/modprobe.d/cifs-oplocks.conf"
if [ ! -e "$MODFILE" ]; then
  sudo sh -c "echo '# disable OpLocks, in order to have working cache with M-drive' > $MODFILE"
  sudo sh -c "echo 'options cifs enable_oplocks=0' >> $MODFILE"
fi

# git hint on how to change fstab entries to use the cache for microscopy
echo "HINT: add 'fsc' option to your cifs mounts in /etc/ftab to enable persistent cache"
echo "HINT: add 'cache=loose' option to your cifs mounts in /etc/ftab to make them work with M-drive"
echo "HINT: umount your cifs mounts and reload cifs module (or -- simpler -- just reboot)"
