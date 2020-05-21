**Note for myself, likely useful to others**\
When installing cuda using the local debian method, for cuda 10.0, install the metapackage `cuda-toolkit-10.0` instead of the recommended `cuda` metapackage\... otherwise it may complain/refuse to install if your nvidia-driver is too recent (say 430) compared to what it expects\... even if it runs perfectly fine with more recent drivers.
