from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import io
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import os
import pickle
from tqdm import tqdm
import cv2
import re
import subprocess

class TextOcr():
    def __init__(self, ocrType):
        self.service=None
        self.ocrType=ocrType


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

    def filterText(self,inputText):
        inputText = re.sub('[\\\\+/§◎*)@<>#%(&=$_\-^01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz:;«¢~「」〃ゝゞヽヾ一●▲・ヽ÷①↓®▽■◆『£〆∴∞▼™↑←]', '', inputText)   #remove special char
        inputText = ''.join(inputText.split())    #remove whitespace
        return inputText

        
    def getTextGoogleOcr(self,img):
        if self.service is None:
            self.service=self.getGoogleCred()

        exceptionCount=0
        while exceptionCount<5:
            try:
                #https://tanaikech.github.io/2017/05/02/ocr-using-google-drive-api/
                txtPath = 'googleocr.txt'  # Text file outputted by OCR
                imgPath="googleocr.jpg"
                cv2.imwrite(imgPath, img)  
                mime = 'application/vnd.google-apps.document'
                res = self.service.files().create(
                    body={'name': imgPath,
                        'mimeType': mime },
                    media_body=MediaFileUpload(imgPath, mimetype=mime, resumable=True) ).execute()
                downloader = MediaIoBaseDownload(
                    io.FileIO(txtPath, 'wb'),
                    self.service.files().export_media(fileId=res['id'], mimeType="text/plain"))
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                self.service.files().delete(fileId=res['id']).execute()
                with  open(txtPath, "r", encoding="utf-8" ) as f:   text_google = f.read()    #txt to str
                text_google=text_google.replace('\ufeff', '') 
                text_google=self.filterText(text_google)
            except:
                exceptionCount+=1
                continue
            break
        return text_google   
        
    def getTextWindowOcr(self,img):
        inputFile="lib_/input.jpg"
        outputFile='lib_/output.txt'
        cv2.imwrite(inputFile, img)        
        p = subprocess.Popen(('./lib_/winocr/winocr.exe'))
        p.wait()       
        with  open(outputFile, "r", encoding="utf-8" ) as f:   text = f.read()    #txt to str
        if os.path.exists(inputFile):  os.remove(inputFile)
        if os.path.exists(outputFile):  os.remove(outputFile)
        text=self.filterText(text)
        return text
        
    def checkWindowOcr(self,):
        p = subprocess.Popen(('./lib_/winocr/winocr.exe'))
        p.wait() 
        if os.path.exists("./lib_/loadResult.txt"):          
            with  open("./lib_/loadResult.txt", "r", encoding="utf-8" ) as f:   text = f.read()    #txt to str
            if text=="True":
                return True
        return False
        
    def getTextFromImg(self,imgPath,rectList,textOnlyFolder):
        fileName=os.path.basename(imgPath)
        img = cv2.imread(textOnlyFolder+fileName)
        textList=[]
        rectP,rect=rectList
        for x1,y1,x2,y2 in rectP: 
          # Cropping the text block for giving input to OCR 
          cropped = img[y1: y2, x1: x2] 
          
          if self.ocrType=="googleocr":
            text=self.getTextGoogleOcr(cropped)          
          elif self.ocrType=="windowocr":
            text=self.getTextWindowOcr(cropped)
          textList+=[text]
        
        return textList
        
 