# Analysis machines configuration

This repo contains mainly installation documentation (see below), some [notes](NOTES.md) about bugs and fixes, and a [spreadsheet](MACHINES.tsv) summarizing the fleet.

Check the `#analysis_machines` Slack channel of https://mrsicflogelhofer.slack.com/ for more information, historical details, ask for help, etc.

## Installation checklist for a new machine

Here is a quick checklist to install a new analysis machine:

- install xubuntu 18.04 (xfce desktop is choosen for x2go compatibility)
- install `openssh-server` with `apt`, to access the machine remotely
- upgrade the system using `apt upgrade`
- install additional useful softwares using `apt`, see list below
- configure the `/mnt/data` partition using a btrfs RAID1 configuration
  or configure `/home` as a separate partition using a btrfs RAID1 configuration
- install `monitorix` package, following its installation instructions
- install East quadrant printer drivers and add a printer using xfce GUI
- (optional) install virtualbox, provide a Windows virtual machine and stick a
  Windows license on the computer case
- (optional) install proprietary drivers and related libraries (e.g. nvidia
  drivers and cuda)
- (optional) install third-party softwares such as `matlab`, `pycharm`, `slack`
  and `miniconda`
- add user(s) (+ a private folder in `/mnt/data` and their mount point for
  `winstor`)
- provide the MAC address and the computer name to the IT, to get name
  resolution

Installation of additional softwares:
```
# development packages
sudo apt install build-essential gfortran bison flex cmake python3-pip python3-dev python3-venv
# GIT related packages
sudo apt install git meld tig gitg
# filesystem packages
sudo apt install btrfs-tools cifs-utils nfs-common gparted
# monitoring and diagnostic packages
sudo apt install iotop htop nload lnav dfc ncdu smartmontools
# remote session packages
sudo apt install x2goserver x2goclient
# other CLI softwares packages
sudo apt install screen tmux emacs vim-gtk tree ranger curl atool parallel
# other GUI softwares packages
sudo apt install synaptic gimp inkscape grsync
```

Configuration of the `/mnt/data` mount point:
```
sudo mkfs.btrfs -L data -d raid1 /dev/<drive1> /dev/<drive2> ...
sudo mkdir /mnt/data
sudo sh -c 'echo "\n# raid volume\nLABEL=data /mnt/data btrfs defaults 0 0" >> /etc/fstab'
```

Configuration of `/home` as a separate partition:
```
sudo mkfs.btrfs -L data -d raid1 /dev/<drive1> /dev/<drive2> ...
sudo sh -c 'echo "\n# raid volume\nLABEL=data /home btrfs defaults,nofail 0 0" >> /etc/fstab'
```
Note that main user(s) should be created before this mount point, to be able to
log in graphically in case the RAID array fails (to get a proper `/home` folder
on the original OS drive). The `nofail` option prevents the systems from
blocking if the RAID don't mount, but then errors are quite silent.

Install monitorix (following its [documentation](https://www.monitorix.org/doc-debian.html)
and using [IzzySoft](https://apt.izzysoft.de/ubuntu/dists/generic/) APT
repository, checked on 2019/02/11):
```
sudo sh -c 'echo "deb https://apt.izzysoft.de/ubuntu generic universe" > /etc/apt/sources.list.d/monitorix.list'
curl https://apt.izzysoft.de/izzysoft.asc | sudo apt-key add -
sudo apt update
sudo apt install monitorix
```

For the East quadrant printer (Kyocera M6026cdn), download the "Linux UPD driver
with extended feature support" package from Kyocera's wbesite:
https://www.kyoceradocumentsolutions.co.za/index/service___support/download_center.false.driver.ECOSYSM6026CDN._.EN.html
Then unpack it twice and install the ubuntu package:
```
aunpack KyoceraLinux*.zip
aunpack KyoceraLinuxPackages*.tar.gz
sudo dpkg -i KyoceraLinuxPackages-*/Ubuntu/Global/kyodialog_amd64/kyodialog_7.0-0_amd64.deb
sudo apt -f install  # fix missing dependencies
kyodialog7 --telemetry false  # turn off google analytics
```
For each user, use `Printers` from the xfce menu to add a printer:

- select `Network Printer > Internet Printing Protocol (ipp)`
- enter device URI: `ipp://caxton.swc.ucl.ac.uk:631/printers/swc-L4-E-Quad`
- press forward and leave default parameters.

Create a user and (optional) give administrator rights:
```
sudo adduser <username>  # create the new user
sudo adduser <username> sudo  #  add use to sudo group (aka admin rights)
```

Install virtualbox:
```
sudo apt install virtualbox virtualbox-ext-pack virtualbox-guest-additions-iso
```
Make sure CPU virtualization is enabled in the BIOS/UEFI.
Add user(s) to `vboxusers` to allow usb passthrough:
```
sudo adduser <username> vboxusers
```

Third-party packages:

- `slack` can be installed with `snap` or downloading their `.deb` package,
- `pycharm` can be installed with `snap`, but user needs a license for the
  professional version (as UCL member we get educational access for free)
- `matlab` can be downloaded and installed via the MathWorks website, if you
  have a MathWorks account bound to UCL (use your UCL email address), but note
  that only staff (not students) can activate a campus license,
- `miniconda` can be downloaded from the conda website, just make sure to
  install using `sudo` and the location `/opt/miniconda3`
  + to configure the shell of a user: `/opt/miniconda3/bin/conda init`
  + to disable the default environment: `conda config --set auto_activate_base false`


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
