from PIL import Image, ImageFont, ImageDraw  
import textwrap              
from tqdm import tqdm
import os

class TextDraw():
    def __init__(self, fontStyle, fontSize):
        self.fontStyle=fontStyle
        self.fontSize=fontSize
    
    
    def getFont(self,fontSize):
        return ImageFont.truetype(self.fontStyle , int(fontSize))
    
    #################draw text
    def drawText(self,imgPath,rect,textList,break_long_words=False):
      img = Image.open(imgPath)
      if self.fontSize=="auto":
        fontSize=img.size[1]*0.015
      else:
        fontSize=self.fontSize
      imageFont=self.getFont(fontSize)
      draw = ImageDraw.Draw(img)
      for text,(x,y,w,h)  in zip(textList,rect):
        if text=="": continue
        for line in textwrap.wrap(text, width=w//imageFont.size+1,break_long_words=break_long_words):   #split text to fit into box
            #text stroke
            shadowcolor=(255,255,255) #white
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
            draw.text((x, y), line, font=imageFont, fill=(0, 0, 0))  #black
            y += imageFont.size+strokeSize
      return img
         

    def drawTextToImage(self,imgPath,textBoxList,textListList_trans,inpaintedFolder,transalatedFolder):
        fileName=os.path.basename(imgPath)
        rectP,rect=textBoxList
        im=self.drawText(inpaintedFolder+fileName,rect,textListList_trans)
        im.save(transalatedFolder+fileName) 
        
        