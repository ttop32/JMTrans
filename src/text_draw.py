

from PIL import Image, ImageFont, ImageDraw  
import textwrap              
from tqdm import tqdm
import os

class TextDraw():
    def __init__(self, fontStyle, fontSize):
        self.fontStyle=fontStyle
        
        if fontSize=="auto":
            self.fontSize=fontSize
        else:
            self.fontSize=int(fontSize)
            self.font = ImageFont.truetype(fontStyle, self.fontSize)
            
            
    #################draw text
    def drawText(self,imgPath,rect,textList,imageFont):
        img = Image.open(imgPath)
        draw = ImageDraw.Draw(img)
        for i,(x,y,w,h)  in enumerate(rect):
            text=textList[i]
            if text=="": continue
            margin, offset=x,y
            for line in textwrap.wrap(text, width=int(w/self.fontSize)+1):   #split text to fit into box
                #text stroke
                shadowcolor=(255,255,255) #white
                x,y=margin,offset
                strokeSize=2
                # thin border
                draw.text((x-strokeSize, y), line, font=imageFont, fill=shadowcolor)
                draw.text((x+strokeSize, y), line, font=imageFont, fill=shadowcolor)
                draw.text((x, y-strokeSize), line, font=imageFont, fill=shadowcolor)
                draw.text((x, y+strokeSize), line, font=imageFont, fill=shadowcolor)
                # thicker border
                draw.text((x-strokeSize, y-strokeSize), line, font=imageFont, fill=shadowcolor)
                draw.text((x+strokeSize, y-strokeSize), line, font=imageFont, fill=shadowcolor)
                draw.text((x-strokeSize, y+strokeSize), line, font=imageFont, fill=shadowcolor)
                draw.text((x+strokeSize, y+strokeSize), line, font=imageFont, fill=shadowcolor)
                #draw text
                draw.text((margin, offset), line, font=imageFont, fill=(0, 0, 0))  #black
                offset += imageFont.getsize(line)[1]+strokeSize*2
        return img

    def drawTextToImage(self,imgPath,textBoxList,textListList_trans,inpaintedFolder,transalatedFolder):
        fileName=os.path.basename(imgPath)
        rectP,rect=textBoxList
        if self.fontSize=="auto":
            img = Image.open(inpaintedFolder+fileName)
            self.fontSize=int(img.size[1]/100*2.0)
            self.font=ImageFont.truetype(self.fontStyle, self.fontSize)
            
        im=self.drawText(inpaintedFolder+fileName,rect,textListList_trans,self.font)
        im.save(transalatedFolder+fileName) 
        
            
            