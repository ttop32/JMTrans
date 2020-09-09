# -*- coding: utf-8 -*-
from ctypes import WinDLL, c_char_p, c_int, c_wchar_p
from ctypes.wintypes import BOOL
import re
import os
import pickle

class TransEngine:
    def __init__(self, ):
        mainPath='C:\Program Files (x86)\ChangShinSoft\ezTrans XP'
        dllPath=os.path.join(mainPath,"J2KEngineH.dll")
        datPath= str.encode(os.path.join(mainPath,"Dat"))
        
        engine=WinDLL(dllPath)
    
        self.start = engine.J2K_InitializeEx
        self.start.argtypes = [c_char_p, c_char_p]
        self.start.restype = BOOL

        self.trans = engine.J2K_TranslateMMNTW
        self.trans.argtypes = [c_int, c_wchar_p]
        self.trans.restype = c_wchar_p

        self.start_obj = self.start(b"CSUSER123455", datPath)
    def translate_j2k(self, src_text):
        trans_obj = self.encode_text(self.trans(0, self.decode_text(src_text)))
        return trans_obj

    def decode_text(self,txt):
        chars = "↔◁◀▷▶♤♠♡♥♧♣⊙◈▣◐◑▒▤▥▨▧▦▩♨☏☎☜☞↕↗↙↖↘♩♬㉿㈜㏇™㏂㏘＂＇∼ˇ˘˝¡˚˙˛¿ː∏￦℉€㎕㎖㎗ℓ㎘㎣㎤㎥㎦㎙㎚㎛㎟㎠㎢㏊㎍㏏㎈㎉㏈㎧㎨㎰㎱㎲㎳㎴㎵㎶㎷㎸㎀㎁㎂㎃㎄㎺㎻㎼㎽㎾㎿㎐㎑㎒㎓㎔Ω㏀㏁㎊㎋㎌㏖㏅㎭㎮㎯㏛㎩㎪㎫㎬㏝㏐㏓㏃㏉㏜㏆┒┑┚┙┖┕┎┍┞┟┡┢┦┧┪┭┮┵┶┹┺┽┾╀╁╃╄╅╆╇╈╉╊┱┲ⅰⅱⅲⅳⅴⅵⅶⅷⅸⅹ½⅓⅔¼¾⅛⅜⅝⅞ⁿ₁₂₃₄ŊđĦĲĿŁŒŦħıĳĸŀłœŧŋŉ㉠㉡㉢㉣㉤㉥㉦㉧㉨㉩㉪㉫㉬㉭㉮㉯㉰㉱㉲㉳㉴㉵㉶㉷㉸㉹㉺㉻㈀㈁㈂㈃㈄㈅㈆㈇㈈㈉㈊㈋㈌㈍㈎㈏㈐㈑㈒㈓㈔㈕㈖㈗㈘㈙㈚㈛ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⒜⒝⒞⒟⒠⒡⒢⒣⒤⒥⒦⒧⒨⒩⒪⒫⒬⒭⒮⒯⒰⒱⒲⒳⒴⒵⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂"
        for c in chars:
            if c in txt:
                txt = txt.replace(c,"\\u" + str(hex(ord(c)))[2:])
        return txt

    def encode_text(self,txt):
        return re.sub(r'(?i)(?<!\\)(?:\\\\)*\\u([0-9a-f]{4})', lambda m: chr(int(m.group(1), 16)), txt)
        



    

if __name__ == "__main__":
    eng = TransEngine()
    
    with open('input.txt', 'rb') as f:
        text = pickle.load(f)
    
    text=eng.translate_j2k(text)
    
    with open('output.txt', 'wb') as f:
        pickle.dump(text, f)    


