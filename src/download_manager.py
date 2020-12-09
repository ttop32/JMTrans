import subprocess    
import glob 
import os
import requests
from bs4 import BeautifulSoup
import wget
import os



class DownloaderManager():
    def __init__(self, ):
        self.updateDownloader()
    
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
    
    def getLocalDirFileList(self,path):
        mangaName = os.path.basename(path) 
        downloadFileList=glob.glob(os.path.join(path,"*"))
        downloadFileList.sort()
        return downloadFileList,mangaName
        
        
    
    def updateDownloader(self,):
        #get download link
        webpage=requests.get("https://github.com/mikf/gallery-dl/releases/")
        soup=BeautifulSoup(webpage.content,"html.parser")
        mydivs = soup.findAll("div", {"class": "Box Box--condensed mt-3"})[0] #first continaer
        for a in mydivs.find_all('a', href=True):                            #list all link
          if a['href'][-4:]==".exe":                                       #LINK TO download exe
            downloadLink="https://github.com"+a['href']


        #check current version
        if os.path.exists('./lib_/gallery-dl.txt'):
            with open('./lib_/gallery-dl.txt', "r") as file:
                currentVersion = file.readline()

            #download if new version available
            if currentVersion!=downloadLink:
                if os.path.exists(downloadLink):
                    os.remove(downloadLink)
                wget.download(downloadLink, './lib_/gallery-dl.exe')

                with open('./lib_/gallery-dl.txt', "w") as file:
                    file.write(downloadLink)


