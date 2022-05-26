#! /usr/bin/python
import urllib.request


def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)    
    file = open(filename, 'wb')
    file.write(response.read())
    file.close()
