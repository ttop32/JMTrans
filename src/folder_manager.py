import os
import shutil
from datetime import datetime 

class FolderManager():
    def __init__(self, ):
        self.mainTempFolder="tmp/"
        self.downloadPath="gallery-dl/"


    def intitFolderEnv(self,downloadFileList,mangaName):
        self.setMainTempFolder(mangaName)
        self.createDir([self.oriFolder,self.textOnlyFolder,self.inpaintedFolder,self.transalatedFolder])
        self.copyFilesToFolder(downloadFileList,self.oriFolder)
        oriFileList=[self.oriFolder+os.path.basename(i) for i in downloadFileList]
        return oriFileList
        
        

    def setMainTempFolder(self,folderName):
        self.mainTempFolder="tmp/"+datetime.now().strftime("%Y%m%d%H%M%S")+"/"
        self.oriFolder=self.mainTempFolder+"ori/"
        self.textOnlyFolder=self.mainTempFolder+"textOnly/"
        self.inpaintedFolder=self.mainTempFolder+"inpainted/"
        self.transalatedFolder=self.mainTempFolder+folderName+"/"
    def createDir(self,listPath):
        for filePath in listPath:
            if not os.path.exists(filePath):
                os.makedirs(filePath)
    def removeDir(self,listPath):
        for filePath in listPath:
            if os.path.exists(filePath):
                shutil.rmtree(filePath)


    def get_download_path(self,):
        """Returns the default downloads path for linux or windows"""
        if os.name == 'nt':
            import winreg
            sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                location = winreg.QueryValueEx(key, downloads_guid)[0]
            return location
        else:
            return os.path.join(os.path.expanduser('~'), 'downloads')

    def copyFilesToFolder(self,fileList,tempFolder):
        for filename in fileList:
            shutil.copy(filename, tempFolder)
            
    
    def saveFileAndRemove(self,mangaName):
        #save as zip file
        shutil.make_archive(mangaName, 'zip', self.transalatedFolder)
        
        namePadding=""
        i=0
        while os.path.exists(os.path.join(self.get_download_path(),mangaName+namePadding+".zip")):
            i+=1
            namePadding="("+str(i)+")"
            
        zipFile=mangaName+namePadding+".zip"    
        os.rename(mangaName+".zip", zipFile) 
        
        shutil.move(zipFile, self.get_download_path())
        self.removeDir([self.mainTempFolder])
        
        return os.path.join(self.get_download_path(),zipFile)
        

    def sendInfo(self,title,image,pages):
        pass

if __name__ == "__main__":
    folderManager=FolderManager()
    print( folderManager.get_download_path())