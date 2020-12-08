import configparser
from matplotlib import font_manager



class IniHandler():
    def __init__(self, ):    
        self.config = configparser.ConfigParser();
        self.configPath="setting.ini"
        self.optionList=dict()
        
        self.createOption("OCR",self.getOcrList(),"Google OCR")
        self.createOption("Translator",self.getTranslaotrList(),"EZTrans XP")
        self.createOption("Language",self.getLanguageList(),"korean")
        self.createOption("FontStyle",self.getFontStyleList(),"NotoSans")
        self.createOption("FontSize",self.getFontSizeList(),"auto")
        self.createOption("detectiondone",{"done":"done","notDone":"notDone"},"notDone",show=False)
        self.currentSettingValDict=self.loadINI()

    def createOption(self,name, optionItemDict, defaultItem,show=True):
        self.optionList[name]={"optionItemDict":optionItemDict, "defaultItem":defaultItem,"show":show}
    def getDefault(self,):
        defaultDict=dict()
        for key in sorted(self.optionList.keys()):  
            defaultDict[key]=self.optionList[key]["defaultItem"]
        return defaultDict

    def setINIValue(self,name,value):        
        inv_map = {v: k for k, v in self.optionList[name]["optionItemDict"].items()}
        print(name,value,inv_map[value])
        
        self.currentSettingValDict[name]=inv_map[value]
        self.saveINIwithDict(self.currentSettingValDict)
        
    def saveINIwithDict(self,settingDict):
        self.config['setting'] = settingDict
        with open(self.configPath, 'w') as configfile:
            self.config.write(configfile)
        
    def loadINI(self,):
        self.config.read(self.configPath)
        if "setting" not in self.config.sections():
            self.saveINIwithDict(self.getDefault()) 
        iniDict=dict(self.config["setting"])
            
        #lower case to upper case key
        iniDict_new=dict()
        for key_optionList in self.optionList.keys():  
            for key_iniDict in iniDict.keys():  
                if key_optionList.lower()==key_iniDict:
                    iniDict_new[key_optionList]=iniDict[key_iniDict]
            
        return iniDict_new

    def getOcrList(self,):
        ocrDidct=dict({"Google OCR":"googleocr","Window OCR":"windowocr" })
        return ocrDidct
        
    def getTranslaotrList(self,):
        translatorDict=dict({"EZTrans XP":"eztrans","Google":"google" })
        return translatorDict
        
    def getLanguageList(self,):
        LANGUAGES = {'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy', 'azerbaijani': 'az', 'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn', 'bosnian': 'bs', 'bulgarian': 'bg', 'catalan': 'ca', 'cebuano': 'ceb', 'chichewa': 'ny', 'chinese (simplified)': 'zh-cn', 'chinese (traditional)': 'zh-tw', 'corsican': 'co', 'croatian': 'hr', 'czech': 'cs', 'danish': 'da', 'dutch': 'nl', 'english': 'en', 'esperanto': 'eo', 'estonian': 'et', 'filipino': 'tl', 'finnish': 'fi', 'french': 'fr', 'frisian': 'fy', 'galician': 'gl', 'georgian': 'ka', 'german': 'de', 'greek': 'el', 'gujarati': 'gu', 'haitian creole': 'ht', 'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'iw', 'hindi': 'hi', 'hmong': 'hmn', 'hungarian': 'hu', 'icelandic': 'is', 'igbo': 'ig', 'indonesian': 'id', 'irish': 'ga', 'italian': 'it', 'japanese': 'ja', 'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km', 'korean': 'ko', 'kurdish (kurmanji)': 'ku', 'kyrgyz': 'ky', 'lao': 'lo', 'latin': 'la', 'latvian': 'lv', 'lithuanian': 'lt', 'luxembourgish': 'lb', 'macedonian': 'mk', 'malagasy': 'mg', 'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt', 'maori': 'mi', 'marathi': 'mr', 'mongolian': 'mn', 'myanmar (burmese)': 'my', 'nepali': 'ne', 'norwegian': 'no', 'pashto': 'ps', 'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa', 'romanian': 'ro', 'russian': 'ru', 'samoan': 'sm', 'scots gaelic': 'gd', 'serbian': 'sr', 'sesotho': 'st', 'shona': 'sn', 'sindhi': 'sd', 'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so', 'spanish': 'es', 'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv', 'tajik': 'tg', 'tamil': 'ta', 'telugu': 'te', 'thai': 'th', 'turkish': 'tr', 'ukrainian': 'uk', 'urdu': 'ur', 'uzbek': 'uz', 'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'}
        return LANGUAGES
     
    def getFontSizeList(self,):
        sizeDict=dict({})
        for i in range(10,100):
            sizeDict[str(i)]=str(i)
        sizeDict["auto"]="auto"
        return sizeDict

    def getFontStyleList(self,):
        font_manager._rebuild()
        # 리스트의 원소(폰트파일의 경로)만큼 반복
        fontDict=dict()
        for v in font_manager.findSystemFonts(fontpaths=None, fontext='ttf'):
            try:
                # 각 폰트파일의 경로를 사용하여 폰트 속성 객체 얻기
                fprop = font_manager.FontProperties(fname=v)
                # 폰트 속성중 이름과 파일 경로를 딕셔러리로 구성하여 리스트에 추가.
                fontDict[fprop.get_name()]=fprop.get_file()
            except:
                continue
        fontDict["NotoSans"]="./font/NotoSansKR-Regular.otf"
        return fontDict
    def getCurrentSetting(self,):
        nonDisplayDict=dict()
        for key in self.currentSettingValDict.keys():  
            nonDisplayDict[key]=self.optionList[key]["optionItemDict"][self.currentSettingValDict[key]]
        return nonDisplayDict
        