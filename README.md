# JMTrans - Japanese Manga Translator
get japanese manga from url to translate manga image using SickZil(tensorflow model), google ocr and eztrans xp
  
download latest version  (using eztrans xp translator, korean only)  
https://github.com/ttop32/JMTrans/releases/latest/download/JMTrans.zip
  
pre released colab version  (using google translator, suport multi lang)  
https://colab.research.google.com/drive/1XbR7fNXtT4TGlLI1FBcCQv7Gj5mlDvwb?usp=sharing


# Result
![result](doc/result1.png)
![result](doc/result2.png)
![result](doc/result3.png)
![result](doc/result4.png)
![result](doc/result5.png)
![result](doc/result6.png)
![result](doc/result7.png)

# Workflow
- use gallery-dl to get managa from url 
- do text segmentation from manga image using SickZil
- use opencv to crop text image based on text segmentation results
- get text from image using pytesseract ocr and nhocr
- translating
- use pil to place translated text


# Supported URL
gallery-dl is used to download. Its support sites are:
- [supported site list](https://github.com/mikf/gallery-dl/blob/master/docs/supportedsites.rst)

# Acknowledgement and References
- [SickZil-Machine](https://github.com/KUR-creative/SickZil-Machine)
- [OpenCV with Python wrapper](https://pypi.org/project/opencv-python/)
- [Google Translate API for Python](https://pypi.org/project/googletrans/)
- [Tesseract](https://github.com/tesseract-ocr/tesseract)
- [Pytesseract](https://pypi.python.org/pypi/pytesseract)
- [nhocr](https://github.com/fireae/nhocr)
- [text-detection](https://github.com/qzane/text-detection)
- [ehnd](https://github.com/sokcuri/ehnd)
- [cefpython](https://github.com/cztomczak/cefpython)
- [google drive](https://developers.google.com/drive/api/v3/quickstart/python)
- [gallery-dl](https://github.com/mikf/gallery-dl)


# pip requirements 
python3.5  
pip install tensorflow==1.14.0  
pip install tqdm  funcy PyQt5  opencv-python Pillow  
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib  
pip install pyinstaller  
pip install cefpython3  
pip install pywin32  
pip install matplotlib  
pip install imageio  
pip install googletrans   (not included yet)

