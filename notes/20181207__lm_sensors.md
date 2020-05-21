Maxime Rio  7 Dec 2018 at 13:22\
Changes to chainsaw to report temperature in monitorix:\
- install `lm-sensors` and run `sudo sensors-detect` (use default answers) and let it add required modules to `/etc/modules.conf`\
- install `extra` package for current kernel, to be sure to have the required module (wasn\'t the case for 4.13, I had to install `linux-image-extra-4.13.0-45-generic`)\
- in `/etc/monitorix/monitorix.conf` turn `lmsens` line (in `graph_enable` section) to `y`\
- make sure `lm-sensors` service is running, restart monitorix service (`service lm-sensors restart` and `service monitorix restart`)\
- check http://chainsaw.mrsic-flogel.swc.ucl.ac.uk:8080/monitorix to see if new temperature graphs are available (edited) 
