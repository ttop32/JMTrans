import cv2
import os
from tqdm import tqdm

class TextDetection():
    def __init__(self, ContourSize):
        pass
        self.contourSize=float(ContourSize)
    
    ############################text cropping rectangle
    def text_detect(self,img,ele_size=(8,2)): #
        #https://github.com/qzane/text-detection
        if len(img.shape)==3:
            img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img_sobel = cv2.Sobel(img,cv2.CV_8U,1,0)#same as default,None,3,1,0,cv2.BORDER_DEFAULT)
        img_threshold = cv2.threshold(img_sobel,0,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY)
        element = cv2.getStructuringElement(cv2.MORPH_RECT,ele_size)
        img_threshold_morp = cv2.morphologyEx(img_threshold[1],cv2.MORPH_CLOSE,element)
        contours, hierarchy = cv2.findContours(img_threshold_morp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        noiseSizeParam=int(ele_size[0]/3)
        contours=[i for i in contours if i.shape[0]>noiseSizeParam** 2]     
        Rect = [cv2.boundingRect(i) for i in contours]                                              #no padding, box    #x,y,w,h
        RectP = [(max(int(i[0]-noiseSizeParam),0),max(int(i[1]-noiseSizeParam),0),min(int(i[0]+i[2]+noiseSizeParam),img.shape[1]),min(int(i[1]+i[3]+noiseSizeParam),img.shape[0])) for i in Rect]       #with padding, box  x1,y1,x2,y2 

        
        return RectP,Rect

    def textDetect(self,imgPath,textOnlyFolder):
        fileName=os.path.basename(imgPath)
        img = cv2.imread(textOnlyFolder+fileName)
        rectP,rect= self.text_detect(img,ele_size=(int(img.shape[0]*self.contourSize),int(img.shape[0]*self.contourSize)))  #x,y
        rectList=[rectP,rect]
            
        return rectList


