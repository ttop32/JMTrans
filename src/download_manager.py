import subprocess    
import glob 
import os
import requests
from bs4 import BeautifulSoup
import wget
import subprocess




class DownloaderManager():
    def __init__(self, ):
        self.updateDownloader()
    
    def downloadUrl(self, url):
        self.checkExCred(url)
        p = subprocess.Popen(('./lib_/gallery-dl.exe', url))
        p.wait()  
        print("download done")
        downloadFileList,mangaName=self.getDownloadedFilePathList()
        return  downloadFileList,mangaName
    def getDownloadedFilePathList(self,):
        downloadFileList=glob.glob("gallery-dl/*/*/*.*")
        downloadFileList.sort()
        mangaName=os.path.basename(glob.glob("gallery-dl/*/*")[0]) if len(downloadFileList)!=0 else ""
        return downloadFileList,mangaName
    
    def getLocalDirFileList(self,path):
        mangaName = os.path.basename(path) 
        downloadFileList=glob.glob(os.path.join(path,"*"))
        downloadFileList.sort()
        return downloadFileList,mangaName
        
    def checkExCred(self,url):
        if "exhentai" in url:
            p = subprocess.Popen(("lib_/gallery-dl-cookie/cookie_handler.exe"))
            p.wait()       
        
    def updateDownloader(self,):
        versionPath='./lib_/gallery-dl.txt'
        exePath='./lib_/gallery-dl.exe'


        #check latest version 
        webpage=requests.get("https://github.com/mikf/gallery-dl/releases/")
        soup=BeautifulSoup(webpage.content,"html.parser")
        mydivs = soup.findAll("div", {"class": "Box Box--condensed mt-3"})[0] #first continaer
        for a in mydivs.find_all('a', href=True):                            #list all link
          if a['href'][-4:]==".exe":                                       #LINK TO download exe
            downloadLink="https://github.com"+a['href']


        #check current holded version
        currentVersion=""
        if os.path.exists(versionPath):
            with open(versionPath, "r") as file:
                currentVersion = file.readline()
            
        #download if new version available
        if currentVersion!=downloadLink or not os.path.exists(exePath):
            print("updateDownloader")
            with open(versionPath, "w") as file:
                file.write(downloadLink)

            if os.path.exists(exePath):
                os.remove(exePath)
            wget.download(downloadLink, exePath)
