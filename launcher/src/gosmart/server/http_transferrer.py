from __future__ import print_function

from zope.interface import implementer
import paramiko
import urllib.request as urllib2
import os
import requests

from gosmart.server.transferrer import ITransferrer


@implementer(ITransferrer)
class HTTPTransferrer:
    def __init__(self, host, port, key_file):
        self._host = host
        self._port = 22
        self._port = port
        self._key_file = key_file

    def connect(self):
        print("The Host:" + self._host)
        print("The Port:" + str(self._port))

    def disconnect(self):
        print("Disconnecting")        

    
    def pull_files(self, files, root, remote_root):
        for local, remote in files.items():
            remote_url = "http://gosmartfiles.blob.core.windows.net/gosmart/" + remote    
            absolute_path = os.path.join(root, local)
            print("Download File From: " + remote_url)
            print("Download File To:" + absolute_path)
            directory = os.path.dirname(absolute_path)
            print("Directory Created: " + directory)
            os.makedirs(directory)
            self.downloadFile(remote_url, absolute_path)
		

    def push_files(self, files, root, remote_root):
        for local, remote in files.items():
            absolute_path = os.path.join(root, local)
            print("Uploading from: " + absolute_path + " to:" + remote)
            self.uploadFile(absolute_path, remote)	
			
    def downloadFile(self, sourceUrlStr, destinationStr):
        '''Downloads a file from the source URL to the destination (typically a folder)
        
        Keyword arguments:
        sourceUrlStr -- Url of the file which will be downloaded
        destinationStr -- FullPath to the destination     
        '''        
        if not os.path.exists(destinationStr):
            '''Check If we have downloaded the file already'''
            print("Download: "+ sourceUrlStr +" to " + destinationStr)            

            '''download the file'''
            try:
                serverFile = urllib2.urlopen(sourceUrlStr)
            except:
                raise ServerError("download failed",-2)
            localFile = open(destinationStr, "wb")
            localFile.write(serverFile.read())
            serverFile.close()
            localFile.close()
    
    def uploadFile(self, sourcePath,destinationUrl):
        '''Uploads the file located in sourcePath to the destinationUrl
        
        Keyword arguments:
        sourcePath -- fullpath to the file which will be uploaded
        destinationUrl -- Url where the file is send to
        '''
        print("upload "+sourcePath+" to "+destinationUrl)
        try:
            f = {'file': open(sourcePath, 'rb')}
        except:
            print("file "+sourcePath+" does not exist.")
         #   raise LocalError("File does not exist",-3)
        try:
           #auth=("gosmart","password"), 
            r = requests.post(destinationUrl,
                    files=f)
        except:
            print("Server error!")
          #  raise ServerError("Upload failed.",-1)
        if(r.status_code!=200):
            print("Upload Failed")
          #  raise ServerError("Upload failed",-1)		
