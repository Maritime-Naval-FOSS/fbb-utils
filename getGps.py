#!/usr/bin/python 
import sys 
import getopt 
import os.path 

import time 
import datetime 

import re 
from urllib import urlopen 
from xml.dom.minidom import parseString 
import urllib2 

if __name__ == '__main__': 
    # Analyzing  [http://10.10....] ...
    html = urllib2.urlopen(urllib2.Request("http://203.0.113.245/")).read() 
    text = re.sub(r'&.*?;', ' ', re.sub(r'<[^>]*?>', '', html) ) 
    rexpr = re.compile('.*GPS position(.+)Standard voice outbound') 
    found = rexpr.search(text) 
    if (not found): 
        print "Unable to spot LAT and LNG in this file" 
        exit() 
    # Processing [" + found.group(1) + "] ...
    array = re.sub(' +', ' ', re.sub("[,']", '', found.group(1)) ).split() 
#    print array 
    if (array[0]=='Acquiring'):
        print "Unable to spot LAT and LNG in this file"
        exit()
    lat = ( float(array[1]) + float(array[2])/60 ) 
    if (array[0]=='S'): lat *= -1 
    lng = ( float(array[4]) + float(array[5])/60 ) 
    if (array[3]=='W'): lng *= -1 
    os.spawnv( os.P_WAIT,"/bin/date", ("/bin/date", "-u", "+%Y-%m-%d %H:%M:%S" ) ) 
    print lat 
    print lng 
