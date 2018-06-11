#!/usr/bin/python
import urllib
import unicodedata
import re
import os
import time
from xml.dom import minidom

def getLatLon(node, tag):
    node_data = node.getElementsByTagName(tag)[0].childNodes[0].data
    array = re.sub("[^0-9NSEW]", " ", node_data).encode('ascii','ignore').split()
    retval = ( float(array[0]) + float(array[1])/60 + float(array[2])/3600 )
    if (array[3]=='S' or array[3]=='W'): retval *= -1
    return retval

if __name__ == '__main__':
    xml = minidom.parse( urllib.urlopen('http://203.0.113.254/xml/modem_status.xml') )

    signal ="0.0"
    rssi = xml.getElementsByTagName("Rssi")
    if len(rssi)==1:
        signal = rssi[0].childNodes[0].data

    igps = xml.getElementsByTagName("_IGPS")
    if len(igps)!=1:
        """Unable to spot LAT and LNG in this file"""
        exit()

    """Processing <_IGPS> ..."""
    if len(igps[0].getElementsByTagName("Lat"))==1 and len(igps[0].getElementsByTagName("Lon"))==1:
        lat = getLatLon(igps[0], "Lat")
        lng = getLatLon(igps[0], "Lon")
        os.spawnv( os.P_WAIT,"/bin/date", ("/bin/date", "-u", "+%Y-%m-%d %H:%M:%S" ) )
        print lat
        print lng
        print signal
    else:
        """GPS lat/lng not found. Returning Nothing"""

    xml.unlink()
