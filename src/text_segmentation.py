import os
originalWorkingPath=os.getcwd()
import sys
sys.path.append("./lib/SickZil-Machine/src")
import tensorflow as tf
import core
import imgio
import utils.fp as fp
import cv2
from tqdm import tqdm
import consts

class TextSegmenation():
    def __init__(self, ):
        pass
    
    def imgpath2mask(self, imgpath):
        return fp.go(
            imgpath,
            lambda path: imgio.load(path, imgio.NDARR),     
            core.segmap,
            imgio.segmap2mask)

    def segmentPage(self,imgPath,outputInpaintedPath,outputTextOnlyPath):
        core.load_model(consts.SNETPATH, '0.1.0')
        core.load_model(consts.CNETPATH, '0.1.0')

        fileName=os.path.basename(imgPath)
        oriImage = imgio.load(imgPath, imgio.IMAGE)                      #ori image
        maskImage  = imgio.mask2segmap(self.imgpath2mask(imgPath))        #mask image
        inpaintedImage = core.inpainted(oriImage, maskImage)        #notext image
        textOnlyImage= cv2.bitwise_and(oriImage,maskImage)         #text only image
        textOnlyImage[maskImage==0] = 255                     
        imgio.save(outputInpaintedPath+fileName, inpaintedImage)
        imgio.save(outputTextOnlyPath+fileName, textOnlyImage)

