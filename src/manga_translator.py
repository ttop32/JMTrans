from folder_manager import FolderManager
from download_manager import DownloaderManager
from text_segmentation import TextSegmenation
from text_detection import TextDetection
from text_ocr import TextOcr
from text_translate import TextTranslator
from text_draw import TextDraw

import os
import pickle
from tqdm import tqdm
import time
import threading

class MangaTranslator():
    def __init__(self, url,settingValueDict):
        self.url=url
        
        self.translatorType=settingValueDict["translator"]
        self.language=settingValueDict["language"]
        self.font=settingValueDict["fontstyle"]
        self.fontsize=settingValueDict["fontsize"]
        
        
           
        self.textSegmentation=TextSegmenation()
        self.textDetection=TextDetection()
        self.textOcr=TextOcr()
        self.textTranslator=TextTranslator(self.translatorType,self.language)
        self.textDraw=TextDraw(self.font,self.fontsize)
        self.folder=FolderManager()
        
        
        
        self.customTqdm=tqdm
        
    def processTranslation(self,):
        ###folder init
        self.folder.removeDir([self.folder.downloadPath])


        ####download
        downloader=DownloaderManager()
        downloadFileList,mangaName=downloader.downloadUrl(self.url)
        #downloadFileList,mangaName=downloader.getDownloadedFilePathList()
        
        if mangaName=="":
            print("download fail")
            return -1
        
        
        oriFileList=self.folder.intitFolderEnv(downloadFileList,mangaName)
        self.sendInfo(mangaName,oriFileList[0],len(oriFileList))
        print(mangaName)
        
        
        self.threadCounter=0
        self.lock = threading.Lock()
        self.lock1 = threading.Lock()
        self.lock2 = threading.Lock()
        self.lock3 = threading.Lock()
        self.lock4 = threading.Lock()
        self.lock5 = threading.Lock()
        #forloop
        #for fileName in tqdm(oriFileList): 
        #    self.processTranslationTask(fileName)
        
        
        #thread start
        tList=[]
        for fileName in oriFileList:
          t = threading.Thread(target=self.processTranslationTask, args=(fileName,))
          t.daemon = True
          t.start()
          tList+=[t]
        print("progess")
        #thread progress
        for i in self.customTqdm(range(len(oriFileList))):
          while self.threadCounter<=i:
            time.sleep(0.5)
        
        
        ###save_file
        self.folder.saveFileAndRemove(mangaName)
        
        return 1
        
        
        
    def processTranslationTask(self,fileName):
                
        self.lock1.acquire()
        ###segmentation
        self.textSegmentation.segmentPage(fileName,self.folder.inpaintedFolder,self.folder.textOnlyFolder)
        self.lock1.release()
        self.lock2.acquire()
        
        ###text_detection
        textBoxList=self.textDetection.textDetect(fileName,self.folder.textOnlyFolder)
        self.lock2.release()
        self.lock3.acquire()
        
        ###text_ocr
        textList=self.textOcr.getTextFromImg(fileName,textBoxList,self.folder.textOnlyFolder)
        self.lock3.release()
        self.lock4.acquire()
        

        ###text_translation
        textList_trans=self.textTranslator.translate(textList)
        self.lock4.release()
        self.lock5.acquire()
        
        
        ###text_draw
        self.textDraw.drawTextToImage(fileName,textBoxList,textList_trans,self.folder.inpaintedFolder,self.folder.transalatedFolder)
        self.lock5.release()
        
        
        #count finish
        self.lock.acquire()
        self.threadCounter+=1
        self.lock.release()

        
        
    
        
    def sendInfo(self,title,image,pages):
        pass
        


if __name__ == "__main__":
    settingDict=dict({'translator': "eztrans",
                    'language': "ko",
                     'fontstyle': "./font/NotoSansKR-Regular.otf",
                     'fontsize':23})
    mangaTranslator=MangaTranslator("",settingDict)
    mangaTranslator.processTranslation()
                     
    pass


