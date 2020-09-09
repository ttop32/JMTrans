import subprocess    
import glob 
import os

class DownloaderManager():
    def __init__(self, ):
        pass
    
    def downloadUrl(self, url):
        p = subprocess.Popen(('./lib_/gallery-dl.exe', url))
        p.wait()   
        downloadFileList,mangaName=self.getDownloadedFilePathList()
        return  downloadFileList,mangaName
    def getDownloadedFilePathList(self,):
    
        downloadFileList=glob.glob("gallery-dl/*/*/*.*")
        downloadFileList.sort()
        mangaName=os.path.basename(glob.glob("gallery-dl/*/*")[0]) if len(downloadFileList)!=0 else ""
        return downloadFileList,mangaName
    
    
    
    
#p = subprocess.Popen(('./lib/gallery-dl.exe', "-d","abc",url))
#p.wait()   