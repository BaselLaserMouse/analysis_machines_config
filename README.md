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
