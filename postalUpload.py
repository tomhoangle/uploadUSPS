prod = {
    'env' : 'prod',
    #'curDir': '//odslafirstlogic/logs',
    'curDir': '',
}

dev = {
    'env' : 'dev',
    'curDir': '',
}


import shutil
import sys
import os, time
import datetime
import dateutil.relativedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from zipfile import ZipFile
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

#get all files in a directory
def get_all_file_paths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths

def envi_setup(enviDB):
    global curDir
    global enviro
    curDir = enviDB['curDir']
    enviro = enviDB['env']

#choose enviroment prod_Database or dev_Database
envi_setup(prod)

#create new directory
todayDate = datetime.datetime.today().strftime('%m-%d-%Y')
if(enviro == 'dev'):
    newDir = "C:\\Uploaded\\" + todayDate
elif(enviro == 'prod'):
    newDir = curDir + "/Uploaded/" + todayDate
if not os.path.exists(newDir):
    os.makedirs(newDir)
else:
    print(newDir + " already exist, please check")
    sys.exit()

#move files from last month
lastMonth = datetime.datetime.today() + dateutil.relativedelta.relativedelta(months=-1)
if(enviro == 'dev'):
    try:
        curFile = curDir + "\\BLCDZ" +  lastMonth.strftime('%m%y').lstrip("0") + ".DAT"
        shutil.move(curFile,newDir)
        curFile = curDir + "\\CLCDZ" +  lastMonth.strftime('%m%y').lstrip("0") + ".DAT"
        shutil.move(curFile,newDir)
        curFile = curDir + "\\PLCDZ" +  lastMonth.strftime('%m%y').lstrip("0") + ".DAT"
        shutil.move(curFile,newDir)
    except FileNotFoundError:
        print(curFile + " doesn't exist, please check")
        sys.exit()
elif(enviro == 'prod'):
    try:
        curFile = curDir + "/BLCDZ" +  lastMonth.strftime('%m%y').lstrip("0") + ".DAT"
        shutil.move(curFile,newDir)
        curFile = curDir + "/CLCDZ" +  lastMonth.strftime('%m%y').lstrip("0") + ".DAT"
        shutil.move(curFile,newDir)
        curFile = curDir + "/PLCDZ" +  lastMonth.strftime('%m%y').lstrip("0") + ".DAT"
        shutil.move(curFile,newDir)
    except FileNotFoundError:
        print(curFile + " doesn't exist, please check")
        sys.exit()


#Zip files
filePaths = get_all_file_paths(newDir)
if(enviro == 'dev'):
    zipName = newDir + "\\LCDZ" + lastMonth.strftime('%m%y').lstrip("0") + ".zip"
elif(enviro == 'prod'):
    zipName = newDir + "/LCDZ" + lastMonth.strftime('%m%y').lstrip("0") + ".zip"
with ZipFile(zipName,'w') as zip:
    for file in filePaths:
        zip.write(file)

chrome_options = Options()
#chrome_options.add_argument("--headless")
WINDOW_SIZE = "1920,1080"
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)
driver.get("https://epfup.usps.gov/up/upload.html")
wait.until(ec.visibility_of_element_located((By.XPATH, "//*[@id=\"login\"]"))).send_keys("")#Enter username here
wait.until(ec.visibility_of_element_located((By.XPATH, "//*[@id=\"pword\"]"))).send_keys("")#Enter password here
#wait.until(ec.visibility_of_element_located((By.XPATH, "//*[@id=\"pword\"]"))).send_keys({input('Enter Password: ')})
wait.until(ec.visibility_of_element_located((By.XPATH, "//*[@id=\"LoginForm\"]/table/tbody/tr[2]/td[3]/button[1]"))).click()
Select(wait.until(ec.visibility_of_element_located((By.XPATH, "//*[@id=\"role\"]")))).select_by_value('CSL')
wait.until(ec.visibility_of_element_located((By.XPATH, "//*[@id=\"epfuploadfile\"]"))).send_keys(zipName)
#upload file, don't test this!!!!!
#wait.until(ec.visibility_of_element_located((By.XPATH, "//*[@id=\"myUpldBtn\"]"))).click()"""
time.sleep(10)
