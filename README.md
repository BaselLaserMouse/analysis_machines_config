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


# Machines administration script

This repository also provides a Fabric `fabfile` to execute repetitive tasks to
administrate the machines.

It relies on [Fabric](http://www.fabfile.org/) and [Patchwork](https://fabric-patchwork.readthedocs.io/en/latest/).
You can install them with `pip` as a normal user as follows:
```
pip3 install --user fabric patchwork
```

Then, invoke the tasks listed in the `fabfile` using:
```
fab --prompt-for-sudo-password --prompt-for-login-password <task>
```
which will ask you your sudo and ssh passwords before executing the task on all
machines.

You can restrict the target machine(s) using `-H <hostname>[,<hostname>]`
option.

Use `fab --list` to display a list of available tasks.
