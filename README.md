# Images-Downloader
This is a script used to download docker images quickly
</br>
</br>

### **examples**
---
`python3 ./images.py -r -p ./images -i python:3.5 nginx:latest`
</br>

`python3 ./images.py -f images.txt`
</br>
</br>

### **Settings**
---

## Only one of these settings (required):
#### The images to download provided as command line arguments
    -i image1:tag1 image2:tag2 ... imageN:tagN
    
### The images to download provided as a txt file with full path 
    -f ./images.txt   |   -f ~/images.txt
</br>
</br>

## Either one of these settings (notrequired):
### The path of the directory used to save the images, creates it if it doesn't already exist (default is current directory)
    -p .    |   -p ~/images
### The extension to use when saving the downloaded images (default is docker)
    -e docker    |   -e tar.gz
### A boolean that checks whether to redownload an image if it was previously downloaded (default is false)
    -r


