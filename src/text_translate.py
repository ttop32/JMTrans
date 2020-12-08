import os
from tqdm import tqdm
from google_trans_new import google_translator  
translator = google_translator()  
import pickle
import subprocess

class TextTranslator():
    def __init__(self, translatorType,language):
        self.translatorType=translatorType
        self.language=language
        
    def translateList(self, textList,translateFunc):
        textList_trans=[]
        for text in textList:
            text_trans=translateFunc(text) if len(text)!=0 else ""
            textList_trans+=[text_trans] 
        return textList_trans
    def translateGoogle(self,text):
        text_trans=translator.translate(text, lang_tgt=self.language,) 
        return text_trans
        
    def translateEztrans(self,text):
        with open('input.txt', 'wb') as f:
            pickle.dump(text, f)    
        p = subprocess.Popen(('./lib_/ez_trans.exe'))
        p.wait()       
        with open('output.txt', 'rb') as f:
            text = pickle.load(f)
        if os.path.exists('input.txt'):  os.remove('input.txt')
        if os.path.exists('output.txt'):  os.remove('output.txt')
        return text
            
    def translate(self, textList):
        if self.translatorType=="google":
            transFunc=self.translateGoogle
        elif self.translatorType=="eztrans":
            transFunc=self.translateEztrans
        textList_trans=self.translateList(textList,transFunc )
        return textList_trans
        
if __name__ == "__main__":
    pass