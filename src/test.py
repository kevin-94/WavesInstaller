from os.path import basename
import os, sys
from urlparse import urlsplit
import urllib2

def chunk_report(bytes_so_far, chunk_size, total_size):
   percent = float(bytes_so_far) / total_size
   percent = round(percent*100, 2)
   sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%)\r" % 
       (bytes_so_far, total_size, percent))

   if bytes_so_far >= total_size:
      sys.stdout.write('\n')
      
def chunk_read(response, chunk_size=8192, report_hook=None):
   total_size = response.info().getheader('Content-Length').strip()
   total_size = int(total_size)
   bytes_so_far = 0
   data = []

   while 1:
      chunk = response.read(chunk_size)
      bytes_so_far += len(chunk)

      if not chunk:
         break

      data += chunk
      if report_hook:
         report_hook(bytes_so_far, chunk_size, total_size)

   return "".join(data)      

def url2name(url):
    return basename(urlsplit(url)[2])

def download(url, destination,localFileName = None):
    localName = url2name(url)
    req = urllib2.Request(url)
    r = urllib2.urlopen(req)
    if r.info().has_key('Content-Disposition'):
        # If the response has Content-Disposition, we take file name from it
        localName = r.info()['Content-Disposition'].split('filename=')[1]
        if localName[0] == '"' or localName[0] == "'":
            localName = localName[1:-1]
    elif r.url != url: 
        # if we were redirected, the real file name we take from the final URL
        localName = url2name(r.url)
    if localFileName: 
        # we can force to save the file as specified name
        localName = localFileName
    f = open(localName, 'wb')
    f.write(chunk_read(r, report_hook=chunk_report))
    f.close()
    filedest=destination+"/"+localName
    os.rename(localName, filedest)
    
#http://apache.trisect.eu/tomcat/tomcat-9/v9.0.0.M8/bin/apache-tomcat-9.0.0.M8.zip
if __name__ == "__main__":
    myrul="http://apache.trisect.eu/tomcat/tomcat-9/v9.0.0.M8/bin/apache-tomcat-9.0.0.M8.zip";
    myurl2="https://dl.influxdata.com/influxdb/releases/influxdb-0.13.0_linux_amd64.tar.gz";
    download(myurl2,"D:/tests")
    print "finished"
    
    
    