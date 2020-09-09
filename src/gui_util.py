import win32clipboard
import webbrowser
import re
import requests
import configparser

import threading
from tqdm import tqdm
import time

import sys
import os
import pickle        
from urllib.parse import urlparse
import shutil

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from manga_translator_gui import MangaTranslatorGUI
from folder_manager import FolderManager


class GuiUtil():
    def __init__(self, browser):
        self.downloadLock = threading.Lock()
        self.configPath="setting.ini"
        self.config = configparser.ConfigParser();
        self.browser=browser
        
        self.credFileDetected=False
        self.credScopeDetected=False
        self.ehndDetected=False

        self.folder=FolderManager()
        self.folder.removeDir(["tmp","listItem"])
        self.folder.createDir(["tmp","listItem"])
        

        self.loadINI()

    def filterText(self, text):
        text = re.sub('[^0-9a-zA-Z]+', '', text)
        return text

    def showJSMessage(self,msg):
        self.browser.ExecuteFunction("showMessage", msg)        


    ##ini setting-------------------------------------------------------------
    def saveINIwithDict(self,settingDict):
        self.config['setting'] = settingDict
        with open(self.configPath, 'w') as configfile:
            self.config.write(configfile)

    def saveINI(self,tranlsator, lang, font, fontSize,detection):
        self.config['setting'] = {'translator': tranlsator,
                    'language': lang,
                     'fontstyle': font,
                     'fontsize':fontSize,
                     "detectiondone":detection}
        with open(self.configPath, 'w') as configfile:
            self.config.write(configfile)
                
    def loadINI(self,):
        self.config = configparser.ConfigParser();    
        self.config.read(self.configPath)
        if "setting" not in self.config.sections():
            self.saveINI("EZTrans XP","korean","NotoSans","auto","notDone")  

        self.iniDict=dict(self.config["setting"])

    def loadTranslateSettingValue(self,):
        self.loadINI()
        settingValueDict=dict({})
        settingValueDict["translator"]=self.getTranslaotrList()[self.iniDict["translator"]]
        settingValueDict["language"]=self.getLanguageList()[self.iniDict["language"]]
        settingValueDict["fontstyle"]=self.getFontStyleList()[self.iniDict["fontstyle"]]
        settingValueDict["fontsize"]=self.iniDict["fontsize"]
        return settingValueDict
        
        
    def getTranslaotrList(self,):
        translatorDict=dict({"EZTrans XP":"eztrans"})#,"Google":"google" })
        return translatorDict
        
    def getLanguageList(self,):
        LANGUAGES = {'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy', 'azerbaijani': 'az', 'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn', 'bosnian': 'bs', 'bulgarian': 'bg', 'catalan': 'ca', 'cebuano': 'ceb', 'chichewa': 'ny', 'chinese (simplified)': 'zh-cn', 'chinese (traditional)': 'zh-tw', 'corsican': 'co', 'croatian': 'hr', 'czech': 'cs', 'danish': 'da', 'dutch': 'nl', 'english': 'en', 'esperanto': 'eo', 'estonian': 'et', 'filipino': 'tl', 'finnish': 'fi', 'french': 'fr', 'frisian': 'fy', 'galician': 'gl', 'georgian': 'ka', 'german': 'de', 'greek': 'el', 'gujarati': 'gu', 'haitian creole': 'ht', 'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'iw', 'hindi': 'hi', 'hmong': 'hmn', 'hungarian': 'hu', 'icelandic': 'is', 'igbo': 'ig', 'indonesian': 'id', 'irish': 'ga', 'italian': 'it', 'japanese': 'ja', 'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km', 'korean': 'ko', 'kurdish (kurmanji)': 'ku', 'kyrgyz': 'ky', 'lao': 'lo', 'latin': 'la', 'latvian': 'lv', 'lithuanian': 'lt', 'luxembourgish': 'lb', 'macedonian': 'mk', 'malagasy': 'mg', 'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt', 'maori': 'mi', 'marathi': 'mr', 'mongolian': 'mn', 'myanmar (burmese)': 'my', 'nepali': 'ne', 'norwegian': 'no', 'pashto': 'ps', 'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa', 'romanian': 'ro', 'russian': 'ru', 'samoan': 'sm', 'scots gaelic': 'gd', 'serbian': 'sr', 'sesotho': 'st', 'shona': 'sn', 'sindhi': 'sd', 'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so', 'spanish': 'es', 'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv', 'tajik': 'tg', 'tamil': 'ta', 'telugu': 'te', 'thai': 'th', 'turkish': 'tr', 'ukrainian': 'uk', 'urdu': 'ur', 'uzbek': 'uz', 'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'}
        return LANGUAGES
     
    def getFontSizeList(self,):
        sizeDict=dict({})
        for i in range(5,100):
            sizeDict[str(i)]=str(i)
        
        sizeDict["auto"]="auto"
        return sizeDict
        
    def getFontStyleList(self,):
        from matplotlib import font_manager
        font_manager._rebuild()

        # 리스트의 원소(폰트파일의 경로)만큼 반복
        fontDict=dict({})
        for v in font_manager.findSystemFonts(fontpaths=None, fontext='ttf'):
            try:
                # 각 폰트파일의 경로를 사용하여 폰트 속성 객체 얻기
                fprop = font_manager.FontProperties(fname=v)
                # 폰트 속성중 이름과 파일 경로를 딕셔러리로 구성하여 리스트에 추가.
                fontDict[fprop.get_name()]=fprop.get_file()
            except:
                continue
        fontDict=dict(sorted(fontDict.items()))    #sort key
        
        newFontDict=dict({})
        for key in fontDict.keys():
            newFontDict["""<span style="font-family:"""+key+""";">"""+key+"</span>"]=fontDict[key]    #apply font style on display
        fontDict=newFontDict
        
        #<span style="font-family:Ami R;">Ami R</span>
        fontDict["NotoSans"]="./font/NotoSansKR-Regular.otf"
        return newFontDict
        
    def createSettingBoxHtml(self,optionTitle,optionKey,optionDict,selectedOption):    
        optionItemHtml=""
        for key in optionDict.keys():
            optionItemHtml+="""
            <div class="option">
                <input type="radio" class="radio" id='"""+optionDict[key]+"""' "name="category" />
                <label for='"""+optionDict[key]+"""'>"""+key+"""</label>
            </div>
            """            
       
        optionBarHtml="""
        <div class="optionBoxContainer">
          <h2 class='"""+optionKey+"""'>"""+optionTitle+"""</h2>
          <div class="select-box">
            <div class="options-container">
              """+optionItemHtml+"""
            </div>
            <div class="selected">
              """+selectedOption+"""
            </div>
          </div>
        </div>
        """
        return optionBarHtml 
    def createSettingBoxListHtml(self,):
        boxListHtml=""
        boxListHtml+=self.createSettingBoxHtml("Translator","translator", self.getTranslaotrList(),self.iniDict["translator"])
        boxListHtml+=self.createSettingBoxHtml("Language", "language",self.getLanguageList(),self.iniDict["language"])
        boxListHtml+=self.createSettingBoxHtml("FontStyle","fontstyle", self.getFontStyleList(),self.iniDict["fontstyle"])
        boxListHtml+=self.createSettingBoxHtml("FontSize", "fontsize",self.getFontSizeList(),self.iniDict["fontsize"])
        return boxListHtml
        
    def initSetting(self,):
        boxListHtml=self.createSettingBoxListHtml()
        self.browser.ExecuteFunction("createSettingBoxList", boxListHtml)
        if self.iniDict["detectiondone"]=="done":
            self.browser.ExecuteFunction("showPage", "main_page")
        else:
            self.browser.ExecuteFunction("showPage", "start_page")
        
    def setINIValue(self,name,value):
        self.iniDict[name]=value
        self.saveINIwithDict(self.iniDict)
        


    ##start page-------------------------------------------------------------
    
    def getGoogleCred(self,):
        SCOPES = ['https://www.googleapis.com/auth/drive']
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        service = build('drive', 'v3', credentials=creds)
        return service


    
    def openBrowser(self,url):
        webbrowser.open(url, new=2)

    def validateUrl(self,url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def getClipboard(self,):
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
        except:
            data=""
        return data
    def checkClipboardChangedLoop(self,):
        previouseClipboard=self.getClipboard()  

        while True:
            time.sleep(1)
            if self.getClipboard()!=previouseClipboard and self.getClipboard()!="":
                currentClipboard=self.getClipboard()
                previouseClipboard=currentClipboard
                self.processInputUrl(currentClipboard)
                
    def processInputUrl(self, url):
        if not self.validateUrl(url):
            self.showJSMessage("not a valid url, use http format")
        else:
            self.showJSMessage(url)
            self.startDownload(url)
        
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
            
    def checkCredentialsDownloadedLoop(self,):
        if self.iniDict["detectiondone"]=="done":
            return
        while(not os.path.exists(os.path.join(self.get_download_path(),'credentials.json')) and  not os.path.exists('credentials.json')):
            time.sleep(1.)
        if os.path.exists(os.path.join(self.get_download_path(),'credentials.json')):
            shutil.copy(os.path.join(self.get_download_path(),'credentials.json'), "./")      
        self.showJSMessage("credentials.json detected")
        self.credFileDetected =True
        self.checkDetectionAllDone()
        
    def checkCredentialsDownloaded(self,):
        t = threading.Thread(target=self.checkCredentialsDownloadedLoop, args=())
        t.daemon = True
        t.start()
    def checkCredScopeLoop(self,):
        while(not os.path.exists("./token.pickle")):
            time.sleep(1.)
            
        self.showJSMessage("credential scope detected")
        self.credScopeDetected =True
        self.checkDetectionAllDone()
        
        
    def checkCredScope(self,):
        t = threading.Thread(target=self.checkCredScopeLoop, args=())
        t.daemon = True
        t.start()
    def checkEhndLoop(self,):
        while(not os.path.exists("C:\Program Files (x86)\ChangShinSoft\ezTrans XP\J2KEngineH.dll")):
            time.sleep(1.)
        self.showJSMessage("eztrans ehnd detected")
        self.ehndDetected =True
        self.checkDetectionAllDone()
        
    def checkEhnd(self,):
        t = threading.Thread(target=self.checkEhndLoop, args=())
        t.daemon = True
        t.start()
     
    def checkDetectionAllDone(self,):
        if self.credFileDetected and self.credScopeDetected and self.ehndDetected:
            self.setINIValue("detectiondone","done")

    
    #download-------------------------------------------------------------
    
    def startDownloadThreadFunc(self,url):
        itemId=self.filterText(url)
        infoFunc=self.createDownloadListItemHtml
        progressFunc=self.setItemProgressFunc
        self.createListItemLoading(itemId)
        
        self.downloadLock.acquire()
        mangaTrnaslator=MangaTranslatorGUI(url,self.loadTranslateSettingValue(),itemId,infoFunc,progressFunc)
        result=mangaTrnaslator.processTranslation()
        self.downloadLock.release()
        
        if result==-1:
            self.browser.ExecuteFunction("removeListItem", itemId)   
            self.showJSMessage("download failed. may be GoodbyeDPI not on")
        else:
            self.showJSMessage("downloaded to "+self.get_download_path())
        
    def startDownload(self,url):
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
    
    

    
