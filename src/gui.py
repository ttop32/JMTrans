from cefpython3 import cefpython as cef
import ctypes
import platform
from gui_util import GuiUtil


def main():
    global browser
    global guiUtil

    cef.Initialize()
    window_info = cef.WindowInfo()
    parent_handle = 0
    window_info.SetAsChild(parent_handle, [0, 0, 900, 600])
    browser = cef.CreateBrowserSync(url='file:///index.html',
                                    window_info=window_info,
                                    window_title="JMTrans",)
    if platform.system() == "Windows":
        window_handle = browser.GetOuterWindowHandle()
        insert_after_handle = 0
        # X and Y parameters are ignored by setting the SWP_NOMOVE flag
        SWP_NOMOVE = 0x0002
        # noinspection PyUnresolvedReferences
        ctypes.windll.user32.SetWindowPos(window_handle, insert_after_handle,
                                          0, 0, 900, 600, SWP_NOMOVE)                  
    guiUtil=GuiUtil(browser)
    browser.SetClientHandler(LoadHandler())
    
    
    
    bindings = cef.JavascriptBindings()
    bindings.SetFunction("setINIValue", guiUtil.iniHandler.setINIValue)
    bindings.SetFunction("openBrowser", guiUtil.openBrowser)
    bindings.SetFunction("getGoogleCred", guiUtil.textOcr.getGoogleCred)
    bindings.SetFunction("installWinOcr", guiUtil.installWinOcr)
    bindings.SetFunction("processInputUrl", guiUtil.processInputUrl)
    bindings.SetFunction("checkInstall", guiUtil.checkInstall)
    
    
    
    browser.SetJavascriptBindings(bindings)
    
    
    cef.MessageLoop()
    del browser
    cef.Shutdown()



class LoadHandler(object):
    def OnLoadEnd(self, browser, **_):
        guiUtil.initSetting()
        guiUtil.checkClipboardChanged()
        
        
     
main()