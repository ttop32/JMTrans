import os
originalWorkingPath=os.getcwd()
import sys
sys.path.append("./lib_/SickZil-Machine/src")
import tensorflow as tf
import core
import imgio
import utils.fp as fp
import cv2
from tqdm import tqdm
import consts
import tensorflow as tf

class TextSegmenation():
    def __init__(self, ):
        pass
        #tf.reset_default_graph
        #core.load_model(consts.SNETPATH, '0.1.0')
        #core.load_model(consts.CNETPATH, '0.1.0')
    
    def imgpath2mask(self, imgpath):
        return fp.go(
            imgpath,
            lambda path: imgio.load(path, imgio.NDARR),     
            core.segmap,
            imgio.segmap2mask)

    def segmentPage(self,imgPath,outputInpaintedPath,outputTextOnlyPath):
        
        
        img = cv2.imread(imgPath) 
        if img.shape[0]>3000:
            img = cv2.resize(img, (int(3000*img.shape[1]/img.shape[0]),3000), interpolation = cv2.INTER_AREA)
        cv2.imwrite(imgPath, img) 
        
        fileName=os.path.basename(imgPath)
        oriImage = imgio.load(imgPath, imgio.IMAGE)                      #ori image
        maskImage  = imgio.mask2segmap(self.imgpath2mask(imgPath))        #mask image
        inpaintedImage = core.inpainted(oriImage, maskImage)        #notext image
        textOnlyImage= cv2.bitwise_and(oriImage,maskImage)         #text only image
        textOnlyImage[maskImage==0] = 255                     
        imgio.save(outputInpaintedPath+fileName, inpaintedImage)
        imgio.save(outputTextOnlyPath+fileName, textOnlyImage)

