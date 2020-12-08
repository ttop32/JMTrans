# -*- mode: python -*-
# -*- coding: utf-8 -*-

"""
This is a PyInstaller spec file.
"""

import os
from PyInstaller.building.api import PYZ, EXE, COLLECT
from PyInstaller.building.build_main import Analysis
from PyInstaller.utils.hooks import is_module_satisfies
from PyInstaller.archive.pyz_crypto import PyiBlockCipher


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

cipher_obj = None

a = Analysis(
    ["../gui.py"],
    hookspath=["."],  # To find "hook-cefpython3.py"
    cipher=cipher_obj,
    pathex=[r"C:\Users\tsop3\anaconda3\envs\py35\Lib\site-packages\PyQt5\Qt\bin",
    "../lib_/SickZil-Machine/src"],
    hiddenimports=[]
    
)




if not os.environ.get("PYINSTALLER_CEFPYTHON3_HOOK_SUCCEEDED", None):
    raise SystemExit("Error: Pyinstaller hook-cefpython3.py script was "
                     "not executed or it failed")

pyz = PYZ(a.pure,
          a.zipped_data,
          cipher=cipher_obj)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name="JMTrans",
          debug=True,
          strip=False,
          upx=False,
          console=True,
          icon="../icon/main_icon.ico")
          

COLLECT(exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=False,
        name="JMTrans")
