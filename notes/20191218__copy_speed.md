Also here are some old notes from September that could be helpful to others.I made some speed benchmarks, copying a 1GB file from `gluegun` (my machine) to winstor.\
The aim was to test different file browsers and command line tools to see if some were faster than others.Numbers are in MBit/s (divide by 8 to get MBytes/s) to be easy to compare with the maximum I should be\
able to get, which is \~500MBit/s.Ubuntu 16.04 or 18.04 (with kernel \< 5.0)\
- Thunar 50 Mbit/s\
- PCManFM 50 Mbit/s\
- SpaceFM 50 MBit/s\
- cp 440 MBit/s\
- Nautilus 60 MBit/s\
- PCManFM-qt 60 MBit/s\
- (g)rsync 440 MBit/s\
- ranger 100 MBit/s\
- gvfs-copy 50 MBit/s\
- Xfe 150 MBit/s\
- gnome-commander 170 MBit/sUbuntu 18.04 with kernel 5.0\
- gio copy 650 MBit/s\
- Thunar 650 MBit/s\
- Thunar via `smb://` 250 MBit/s\
- gio copy via `smb://` 260 MBit/sCommand line is always pretty fast (results not reported for xubuntu 18.04 with kernel 5.0 but it was the case), but most interestingly Thunar (the default file browser on xubuntu) is much much faster with 18.04 and recent kernel. There is a nasty glitch in Thunar (and all gnome related file browser) that make it hangs forever if you copy a tiny file (\<1KB I think, but not empty) from Winstor \[1\]. It\'s fixed but not (yet) available on Ubuntu 18.04\... I am testing this from times to times, so I\'ll let you know if eventually it\'s corrected. Meanwhile, you\'ll have to do a bit of `cp` or `rsync` just for these ones. \[1\]: https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=886049
