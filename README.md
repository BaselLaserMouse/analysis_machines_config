# Machines configuration scripts

This repository contains scripts to add some functionalities to Linux
computers:

- `scripts/addcache.bash` adds a persistent cache (using one or several drives)
  usable for network folders, e.g. cifs shares,
- `scripts/addcgroups.bash` adds some rules to limit members of the
  `limited_guest` group (number of CPUs, memory limit) in order to keep machine
  accessible even under heavy load.

These scripts can do very bad things to your machine, so *please* make sure
that you understand what you are doing (and what the scripts are doing) before
using them.
