import selenium
import time
from selenium import webdriver
#import tarfile
import lzma
import shutil
import time 
import os 
import traceback
# browser.get('http://pubchemqc.riken.jp/Compound_000000001_000025000.html');
# browser.maximize_window()
def zipdownload(ininumber,ternumber):
    options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'C:\\jimmy\\ch305\\oraldefense\\python', 'profile.default_content_settings.multiple-automatic-downloads':1 }
    options.add_experimental_option('prefs', prefs)
    #options.add_argument("--headless") #是否開啟視窗
    driver = webdriver.Chrome('chromedriver.exe', chrome_options=options) 
    try:        
        driver.get('http://pubchemqc.riken.jp/Compound_000000001_000025000.html')
    except:
            pass
    for i in range(ininumber,ternumber):
        filename=str(i)
        print(i)
        filename=filename.zfill(9)
        filename_temp="{temp}.b3lyp_6-31g(d).log.xz"
        filename=filename_temp.format(temp=filename)
        filename_temp='//a[text()="{temp}"]'.format(temp=filename)
        try:
            driver.find_element_by_xpath(filename_temp).click()
        except:
            continue

def extractallfile(ininumber,ternumber):
    for i in range(ininumber,ternumber):
        filename=str(i)
        filename=filename.zfill(9)
        filename_temp="C:\\jimmy\\ch305\\oraldefense\\python\\{temp}.b3lyp_6-31g(d).log.xz"
        outfilename_temp="C:\\jimmy\\ch305\\oraldefense\\python\\{temp}.b3lyp_6-31g(d).log"
        extfileout=outfilename_temp.format(temp=filename)
        filename=filename_temp.format(temp=filename)
        try:
            with lzma.open(filename,'rb') as extfile:
                with open(extfileout,'wb') as output:
                    shutil.copyfileobj(extfile,output)
        except :
            continue

            
#zipdownload(501,1500)#爬第n到第m個檔案
extractallfile(501,1500)
