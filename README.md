# MappingTheInternet
A repository where tools can be downloaded to create an image based on pinging hosts

# Dependencies
- Python 3
- np (numpy)
- Image (PIL)
- ThreadPoolExecutor, as_completed (concurrent.futures)
- Linux (and possibly any other UNIX system) for the use of iputils
Maybe pip (pip3) is required to install the missing python package in a conda environment.

# How to use it ?
1. Enter the first IP to scan
2. Enter the last IP to scan
(Wait until all IP are scaned)
3. Enter the name of the image to be saved
4. Enter the folderpath used to save the image
The image is now saved

# Output example from 1.1.1.0 to 1.2.1.1

![plot](./1_1_1_0_-1_2_1_1.png)

#
This repository (and the code under it) is under the Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) licence
