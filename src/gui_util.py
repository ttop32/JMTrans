import pyperclip
import webbrowser
import re
import requests
import threading
from tqdm import tqdm
import time
import sys
import os
import pickle        
from urllib.parse import urlparse
import shutil
from datetime import datetime 
import urllib

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from manga_translator_gui import MangaTranslatorGUI
from folder_manager import FolderManager
from ini_handler import IniHandler
from text_ocr import TextOcr
import admin



class GuiUtil():
    def __init__(self, browser):
        self.downloadLock = threading.Lock()
        self.browser=browser
        self.textOcr=TextOcr("")
                
        self.detectDict=dict()
        self.detectDict["credFileDetected"]=False
        self.detectDict["credScopeDetected"]=False
        self.detectDict["ehndDetected"]=False
        self.detectDict["windowocr"]=False
     
        self.folder=FolderManager()
        self.folder.removeDir(["tmp","listItem"])
        self.folder.createDir(["tmp","listItem"])
        self.iniHandler=IniHandler()
        
        listItemFolder="./listItem/"
        if os.path.exists(listItemFolder):
            shutil.rmtree(listItemFolder)

        


    def filterText(self, text):
        text = re.sub('[^0-9a-zA-Z]+', '', text)
        return text

    def showJSMessage(self,msg):
        self.browser.ExecuteFunction("showMessage", msg)        



    ##ini setting-------------------------------------------------------------        
    def createSettingBoxHtml(self,optionTitle,optionDict,selectedOption):    
        optionItemHtml=""
        for key in sorted(optionDict.keys()):   
            selected=""
            if key==selectedOption:
                selected=" selected"
            optionItemHtml+="""
            <option value='"""+optionDict[key]+"""'"""+selected+""">"""+key+""" </option>
            """            
        optionBarHtml="""
        <div class="optionBoxContainer">
          <h2 class='"""+optionTitle+"""'>"""+optionTitle+"""</h2>
           <div class="select_wrapper"><select name="" id="" class="form-control" onfocus='this.size=5; ' onblur='this.size=1;' onchange='this.size=1; this.blur();'>
              """+optionItemHtml+"""  
            </select>
          </div>
        </div>
        """
        return optionBarHtml 
    def createSettingBoxListHtml(self,):
        boxListHtml=""
        for key in sorted(self.iniHandler.optionList.keys()):  
           item=self.iniHandler.optionList[key]
           if item["show"]==True:
                boxListHtml+=self.createSettingBoxHtml(key, self.iniHandler.optionList[key]["optionItemDict"],self.iniHandler.currentSettingValDict[key])
        return boxListHtml
        
    def initSetting(self,):
        boxListHtml=self.createSettingBoxListHtml()
        self.browser.ExecuteFunction("createSettingBoxList", boxListHtml)
        if self.iniHandler.currentSettingValDict["detectiondone"]=="done":
            self.browser.ExecuteFunction("showPage", "main_page")
            for key in self.detectDict.keys():
                self.detectDict[key]=True
        else:
            self.browser.ExecuteFunction("showPage", "start_page")
        

    ##start page-------------------------------------------------------------
    def openBrowser(self,url):
        webbrowser.open(url, new=2)

    def validateUrl(self,url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def setClipboard(self,text):
        pyperclip.copy(text)
    def getClipboard(self,):
        return pyperclip.paste()
    def checkClipboardChangedLoop(self,):
        previouseClipboard=self.getClipboard()  
        while True:
            time.sleep(1)
            if self.getClipboard()!=previouseClipboard and self.getClipboard()!="":
                currentClipboard=self.getClipboard()
                previouseClipboard=currentClipboard
                self.processInputUrl(currentClipboard)
                
    def processInputUrl(self, url):
        if self.validateUrl(url) or os.path.isdir(url):
            if self.validateUrl(url) :
                url = urllib.parse.urlparse(url)
                url = url.scheme + "://" + url.netloc + urllib.parse.quote(url.path)
            self.showJSMessage(url)
            self.startDownload(url)
        else:
            self.showJSMessage("not a valid url, use http format")
            
        
    def checkClipboardChanged(self,):   
        t = threading.Thread(target=self.checkClipboardChangedLoop, args=())
        t.daemon = True
        t.start()

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
            
            
            
    ##environment detection-------------------------------------------------------------            
    def checkCredentialsDownloadedLoop(self,):
        while(not os.path.exists(os.path.join(self.get_download_path(),'credentials.json')) and  not os.path.exists('credentials.json')):
            time.sleep(1.)
        if os.path.exists(os.path.join(self.get_download_path(),'credentials.json')):
            shutil.copy(os.path.join(self.get_download_path(),'credentials.json'), "./")      
        self.showJSMessage("credentials.json detected")
        self.detectDict["credFileDetected"]=True
        self.checkDetectionAllDone()
        
    def checkCredScopeLoop(self,):
        while(not os.path.exists("./token.pickle")):
            time.sleep(1.)    
        self.showJSMessage("credential scope detected")
        self.detectDict["credScopeDetected"]=True
        self.checkDetectionAllDone()
        
    def checkEhndLoop(self,):
        while(not os.path.exists("C:\Program Files (x86)\ChangShinSoft\ezTrans XP\J2KEngineH.dll")):
            time.sleep(1.)
        self.showJSMessage("eztrans ehnd detected")
        self.detectDict["ehndDetected"]=True
        self.checkDetectionAllDone()
    def checkWindowOcrLoop(self,):
        while(not self.textOcr.checkWindowOcr()):
            time.sleep(1.)
        self.showJSMessage("window ocr detected")
        self.detectDict["windowocr"]=True
        self.checkDetectionAllDone()
    
    def checkInstall(self,slideNum):
        print(slideNum)
        if slideNum==1:
            checkFunc=self.checkCredentialsDownloadedLoop
        elif slideNum==2:
            checkFunc=self.checkCredScopeLoop
        elif slideNum==3:
            checkFunc=self.checkEhndLoop
        elif slideNum==4:
            checkFunc=self.checkWindowOcrLoop
        
        
        t = threading.Thread(target=checkFunc, args=())
        t.daemon = True
        t.start()
         
    def installWinOcr(self,):
        admin.runAsAdmin(["C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe ","""
        $Capability = Get-WindowsCapability -Online | Where-Object { $_.Name -Like 'Language.OCR*ja-JP*' };
        $Result = $Capability | Add-WindowsCapability -Online;
        if ($Result.RestartNeeded -eq $True) { Restart-Computer -Force };
        """])
     
    def checkDetectionAllDone(self,):
        for key in self.detectDict.keys():
            if self.detectDict[key]==False:
                return    
        self.iniHandler.setINIValue("detectiondone","done")    #if all true check done

    def checkIsRunnableEvn(self,):
        currentSetting=self.iniHandler.getCurrentSetting()
        if currentSetting["Translator"]=="eztrans":
            if self.detectDict["ehndDetected"]==False:
                self.showJSMessage("ehnd setup is required for current setting")
                return False
        if currentSetting["OCR"]=="googleocr":    
            if self.detectDict["credFileDetected"]==False or self.detectDict["credScopeDetected"]==False:
                self.showJSMessage("googleocr setup is required for current setting")
                return False        
        if currentSetting["OCR"]=="windowocr":
            if self.detectDict["windowocr"]==False:
                self.showJSMessage("windowocr setup is required for current setting")
                return False
        return True
        
    
    #download-------------------------------------------------------------
    def startDownloadThreadFunc(self,url):
        itemId=self.filterText(url)
        itemId=datetime.now().strftime("%Y%m%d%H%M%S")
        infoFunc=self.createDownloadListItemHtml
        progressFunc=self.setItemProgressFunc
        self.createListItemLoading(itemId)
        
        self.downloadLock.acquire()
        mangaTrnaslator=MangaTranslatorGUI(url,self.iniHandler.getCurrentSetting(),itemId,infoFunc,progressFunc)
        result=mangaTrnaslator.processTranslation()
        self.downloadLock.release()
        
        if result==-1:
            self.browser.ExecuteFunction("removeListItem", itemId)   
            self.showJSMessage("download failed. may be GoodbyeDPI not on")
        else:
            self.showJSMessage("downloaded to "+self.get_download_path())
        
    def startDownload(self,url):
        if self.checkIsRunnableEvn():            
            t = threading.Thread(target=self.startDownloadThreadFunc, args=(url,))
            t.daemon = True
            t.start()
                
        
    def setItemProgressFunc(self,id,progress,time):
        self.browser.ExecuteFunction("setItemProgress", id,progress,time)   

    def createListItemLoading(self,id):
        itemHtml="""
          <li id="""+id+""">
            <div class="loader_parent">
            <div class="loader"></div>  </div>  
                   
          <div class="progress-container">
            <div class="progress_bar" ></div>
          </div>
          </li>
        """
        self.browser.ExecuteFunction("addListItem", itemHtml)           

    def createDownloadListItemHtml(self,id,title,itemImage,itemPages):
        itemHtml="""
          <div class="li_contents">   
             <img class="li_img" src='"""+itemImage+"""'  id="thumb"/> 
              <div class="li_contents_text">   
              <div class="li_title">"""+title+"""</div>  
              <div class="li_info_box">
                <img src="icon/clock.png"  class="li_info_icon"/> 
                <div class="li_info_time">test</div>
                <img src="icon/photo.png"  class="li_info_icon"/> 
                <div class="li_info_pages">"""+itemPages+"""p</div>
               </div>
            </div>             
          </div> 
          <div class="progress-container"><div class="progress_bar" ></div></div> 
        """
        self.browser.ExecuteFunction("changeListItem", id, itemHtml)   



            

if __name__ == '__main__':
    guiUtil=GuiUtil("")
    
    

    
