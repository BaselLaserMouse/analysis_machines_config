# Analysis machines configuration

## Configuration scripts

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


## Administration script

This repository also provides a Fabric `fabfile` to execute repetitive tasks to
administrate the machines.

It relies on [Fabric](http://www.fabfile.org/) and [Patchwork](https://fabric-patchwork.readthedocs.io/en/latest/).
You can install them with `pip` as a normal user as follows:
```
pip3 install --user fabric patchwork
```

Then, invoke the tasks listed in the `fabfile` using `fab <task>`.

Use `fab --list` to display a list of available tasks.

Some tasks need `sudo` rights: add the `--prompt-for-sudo-password` option to
enter it before commands execution.

You can restrict the target machine(s) using `-H <hostname>[,<hostname>]`
option.

To authentificate yourself using ssh, you can either:

- use `--prompt-for-login-password` option, to enter your password once
  everytime your run a task,
- or use key-based ssh authentification
    - create an ssh key using `ssh-keygen`
    - copy it to the machines with `ssh-copy-id -f <key_file.pub> <remote-machine>`
    - add a section in your `.ssh/config` file to force usage of this key for
      analysis machines
    ```
    Host *.mrsic-flogel.swc.ucl.ac.uk
      IdentityFile <key_file>
      User <username>
    ```
    - use `ssh-add <key_file>` to unlock it


## Installation checklist for a new machine

Here is a quick checklist to install a new analysis machine:

- install xubuntu 18.04 (xfce desktop is choosen for x2go compatibility)
- install `openssh-server` with `apt`, to access the machine remotely
- upgrade the system using `apt upgrade`
- install additional useful softwares using `apt`, see list below
- configure the `/mnt/data` partition using a btrfs RAID1 configuration
- configure the `/mnt/microscopy` mount point
- install `monitorix` package, following its installation instructions
- (optional) install proprietary drivers and related libraries (e.g. nvidia
  drivers and cuda)
- (optional) install other analysis softwares such as `matlab` and `pycharm`
- add user(s) (+ a private folder in `/mnt/data` and their mount point for
  `winstor`)
- provide the MAC address and the computer name to the IT, to get name
  resolution

Installation of additional softwares:
```
# development packages
sudo apt install build-essential gfortran bison flex cmake python3-pip python3-dev
# GIT related packages
sudo apt install git meld tig gitg
# filesystem packages
sudo apt install btrfs-tools cifs-utils nfs-common gparted
# monitoring and diagnostic packages
sudo apt install iotop htop nload lnav dfc ncdu smartmontools
# remote session packages
sudo apt install x2goserver x2goclient
# other CLI softwares packages
sudo apt install screen tmux emacs vim-gtk tree ranger curl
# other GUI softwares packages
sudo apt install synaptic gimp inkscape
```

Configuration of the `/mnt/data` mount point:
```
sudo mkfs.btrfs -L data -d raid1 /dev/<drive1> /dev/<drive2> ...
sudo mkdir /mnt/data
sudo sh -c 'echo "\n# raid volume\nLABEL=data /mnt/data btrfs defaults 0 0" >> /etc/fstab'
```

Configuration of the `/mnt/microscopy` mount point:
```
sudo mkdir /mnt/microscopy
sudo sh -c 'echo "\n# team storage\n//172.24.170.8/public /mnt/microscopy cifs username=datatran,noauto,users,noperm 0 0" >> /etc/fstab'
```

Install monitorix (following its [documentation](https://www.monitorix.org/doc-debian.html)
and using [IzzySoft](https://apt.izzysoft.de/ubuntu/dists/generic/) APT
repository, checked on 2019/02/11):
```
sudo sh -c 'echo "deb https://apt.izzysoft.de/ubuntu generic universe" > /etc/apt/sources.list.d/monitorix.list'
curl https://apt.izzysoft.de/izzysoft.asc | sudo apt-key add -
sudo apt update
sudo apt install monitorix
```
