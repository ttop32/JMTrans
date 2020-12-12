import browser_cookie3
import requests
import json
import os

#python 3.6
#pip install browser_cookie3
def main():
    print("get cookie")
    try:
        cookies = browser_cookie3.chrome(domain_name='exhentai.org')
        cookies_dict=requests.utils.dict_from_cookiejar(cookies)
        print(cookies_dict)
        confPath='./lib_/gallery-dl.conf'
        isIdExist="ipb_member_id" in cookies_dict.keys() and "ipb_pass_hash" in cookies_dict.keys()
        
        if isIdExist:
            if os.path.exists(confPath):
                with open(confPath) as f:
                    json_object = json.load(f)
                json_object["extractor"]["exhentai"]={"cookies":cookies_dict}
            else:
                json_object={"extractor":{"exhentai":{"cookies":cookies_dict}}}


        with open(confPath, 'w') as f:
            json.dump(json_object, f)
    except:
        pass

main()