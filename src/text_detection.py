import cv2
import os
from tqdm import tqdm

class TextDetection():
    def __init__(self, ):
        pass
    
    """
    ############################text cropping rectangle
    def getTextBox(self, img,ele_size=(8,2)): #
        #https://github.com/qzane/text-detection
        if len(img.shape)==3:
            img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)    
        img_sobel = cv2.Sobel(img,cv2.CV_8U,1,0)#same as default,None,3,1,0,cv2.BORDER_DEFAULT)
        img_threshold = cv2.threshold(img_sobel,0,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY)
        element = cv2.getStructuringElement(cv2.MORPH_RECT,ele_size)
        img_threshold = cv2.morphologyEx(img_threshold[1],cv2.MORPH_CLOSE,element)
        contours, hierarchy = cv2.findContours(img_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        Rect = [cv2.boundingRect(i) for i in contours if i.shape[0]>100]                                              #no padding, box    #x,y,w,h
        RectP = [(max(int(i[0]-10),0),max(int(i[1]-10),0),min(int(i[0]+i[2]+5),img.shape[1]),min(int(i[1]+i[3]+5),img.shape[0])) for i in Rect]       #with padding, box  x1,y1,x2,y2 
        return RectP,Rect
    """
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

        contours=[i for i in contours if i.shape[0]>100]     
        Rect = [cv2.boundingRect(i) for i in contours]                                              #no padding, box    #x,y,w,h
        RectP = [(max(int(i[0]-10),0),max(int(i[1]-10),0),min(int(i[0]+i[2]+5),img.shape[1]),min(int(i[1]+i[3]+5),img.shape[0])) for i in Rect]       #with padding, box  x1,y1,x2,y2 
        
        #filter rotated contour
        #if rotated contour(word) only have less than two child contour(char),remove
        rotateAngle=[abs(cv2.minAreaRect(i)[-1]) for i in contours ] 
        filteredRectList=[]
        for i,cnt in enumerate(contours): 
              if 15<rotateAngle[i] and rotateAngle[i]<75:
                  x,y,w,h=cv2.boundingRect(cnt)
                  cropped=img[y:y+h,x:x+w]
                  ret, thresh1 = cv2.threshold(cropped, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)   
                  rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(8,8)) 
                  dilate = cv2.dilate(thresh1, rect_kernel, iterations = 1) 
                  smallContours, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                  small_rect=[cv2.boundingRect(i)  for i in smallContours if i.shape[0]>100]    
                  if len(small_rect)<2: continue    #if has less than 2 , skip
              filteredRectList+=[cnt]
        contours=filteredRectList
        Rect = [cv2.boundingRect(i) for i in contours]                                              #no padding, box    #x,y,w,h
        RectP = [(max(int(i[0]-10),0),max(int(i[1]-10),0),min(int(i[0]+i[2]+5),img.shape[1]),min(int(i[1]+i[3]+5),img.shape[0])) for i in Rect]       #with padding, box  x1,y1,x2,y2     
        
        return RectP,Rect

    def textDetect(self,imgPath,textOnlyFolder):
        fileName=os.path.basename(imgPath)
        img = cv2.imread(textOnlyFolder+fileName)
        rectP,rect= self.text_detect(img,ele_size=(int(img.shape[1]/100*2.5),int(img.shape[0]/100*2.5)))  #x,y
        rectList=[rectP,rect]
            
        return rectList


