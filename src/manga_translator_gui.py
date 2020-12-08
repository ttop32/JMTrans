from manga_translator import MangaTranslator
import os 
from tqdm import tqdm
import shutil
import sys


class MangaTranslatorGUI(MangaTranslator):
    def __init__(self, url,settingValueDict, id,infoFunc,progressFunc):
        super().__init__(url,settingValueDict) 
        self.id=id
        
        self.infoFunc=infoFunc
        self.progressFunc=progressFunc
        self.loadCustomTqdm()
        
        
    def loadCustomTqdm(self,):
        class EtaStream(object):
          def __init__(self, func):
            super().__init__()
            self.func=func
        
          def write(self, bar):
            sys.stderr.write(bar)
            try:
                progressPercent=int(bar.split('%')[0])
                progressTime=bar.split('[')[-1]
                progressTime=progressTime.split(',')[0]
                self.func(progressPercent,progressTime)
            except:
              pass
            else:
              pass
          def flush(self):
            sys.stderr.flush()
        self.customTqdm = lambda rangeList: tqdm(rangeList, file=EtaStream(self.setProgress))
    
    def setProgress(self,progress,time):
        self.progressFunc(self.id,progress,time)
        
        
    def sendInfo(self,title,image,pages):
        listItemFolder="./listItem/"
        imagePath = os.path.join(listItemFolder, os.path.basename(image))
        if not os.path.exists(imagePath):            
            if not os.path.exists(listItemFolder):
                os.makedirs(listItemFolder)
            shutil.copy(image, listItemFolder)
        
        self.infoFunc(self.id,title,imagePath,str(pages))
        
        
        
        
        