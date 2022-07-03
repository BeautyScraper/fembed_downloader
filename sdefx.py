# from numpy import byte_bounds
# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from seleniumwire.utils import decode
import json

from pathlib import Path

import subprocess
from internetdownloadmanager import Downloader
import galleryCrawler as gC
import msvcrt
import os
import time
# breakpoint()
# binary = FirefoxBinary(".\\geckodriver-v0.26.0-win64\\geckodriver.exe")

website_name = 'sdefx.cloud' 

opts = Options()
# opts.set_headless()
driver = webdriver.Firefox(options=opts)
driver.implicitly_wait(60)


# url = "https://mrdeepfakes.com/video/9133/shraddha-kapoor-doggy-style-faceset-test-dfl-2-0-request"
# driver.get(url)
# assert "Python" in driver.title


def getLastArgWithoutException(testF,listResolution):
    lastWorking = ""
    for reso in listResolution:
        try:
            testF(reso)
            lastWorking = reso
        except:
            break
    return lastWorking

def alreadyNotDone(func):
    def wrapper(*args, **kwargs):
        filename = website_name+'.txt'
        p = "".join(args)
        print(p)
        ret = gC.rssImageExtractor()
        if ret.alreadyNotDownloaded(filename,p):
            func(*args, **kwargs)
            ret.downloadCompleteRegister(filename,p)
    return wrapper

def checkElementExist(reso):
    driver.find_element_by_link_text(reso)

@alreadyNotDone
def VideoDownload(url):
    driver.get(url)

    # breakpoint()

    # driver.find_element_by_css_selector("div#loading")
    # driver.find_element(by=By.CSS_SELECTOR, value="div#loading")
    # breakpoint()
    # driver.execute_script("arguments[0].click();", streamsb)
    fpPath = r'C:\Personal\Developed\GalleryDownloader\galleryLinks.opml'
    fp = open(fpPath,'a+')
                
    time.sleep(10)
    
    
    for request in driver.requests:
        # https://streamtape.com/e/1RL4VXgYmoSewZw
        srstring = 'https://streamtape.com/e/'
        if srstring in request.url:
            fp.write(request.url.replace('/e/', '/v/')+'\n')
    fp.close()
    # resp = json.loads(body.decode("utf-8"))  
    # videoUrl = resp['data'][-1]['file']
    # videoUrl = videoUrl.replace('\\\\','\\')  
    # driver.get('http://192.168.0.114')
    # savePath = Path("D:\\paradise\\stuff\\new\\JAV")
    # savePath.mkdir(exist_ok=True,parents=True)
    # print(videoUrl)
    # import pdb;pdb.set_trace()
    # breakpoint()
    # ariaDownload(videoUrl, str(savePath), filename)
    
def ariaDownload(url,downPath,filename,connections=4):
    # import pdb;pdb.set_trace()
    subprocess.call(['aria2c', '--dir', downPath, '-o', filename,'-x', str(connections) , url])


def UserCommand(key=b'm'):
    if msvcrt.kbhit():
        pKey = msvcrt.getch()
        print("you pressed: ",pKey)
        if pKey == key:
            return True
        return False
    
if __name__ == "__main__":
    with open("test.opml","r") as fp:
        for url in fp:
            if not website_name in url and not 'strdef.world' in url:
                continue
            if UserCommand(b'q'):
              print('Closing webDriver')
              break  
            try:
                VideoDownload(url.strip())    
            except Exception as e:
                print(f"while processing {url} something happend {e}" , e)
                continue        
    driver.quit()
            # driver.get(url)
