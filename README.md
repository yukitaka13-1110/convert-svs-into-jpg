# convert-svs-into-jpg

## About

Simply, convert svs format images into jpg format images. 
  
   

## Usage

    $ python convert.py

Command line options shown in the following

    $ python convert.py -i /path/to/input -o /path/to/output -m CPUCORE_NUM

-i: path to the input images  
-o: path to the output images  
-m: Number of CPU cores to use for conversion  

You need for more informatin, see some help.  

    $ python convert.py -h

## Requirement

For Ubuntu

    $ sudo apt-get install python-openslide
    $ sudo pip install openslide-python
    $ sudo pip install pillow

  
## Installation

    $ git clone https://github.com/yukitaka13-1110/convert-svs-into-jpg.git
