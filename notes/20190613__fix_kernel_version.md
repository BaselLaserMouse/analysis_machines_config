Recent kernels (4.4.0-143+) are not playing well with Nvidia driver so I changed the default booted kernel to 4.4.0-142 (known to work with nvidia driver) following https://askubuntu.com/questions/216398/set-older-kernel-as-default-grub-entry

- `sudo cp /etc/default/grub /etc/default/grub.bak`
- set `GRUB_DEFAULT="Advanced options for Ubuntu>Ubuntu, with Linux 4.4.0-142-generic"` in `/etc/default/grub`
- `sudo update-grub`
- reboot the machine