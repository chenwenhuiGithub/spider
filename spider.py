import sys
import time
import re
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Csdn():
    def __init__(self, driver, searchStr, displayCount):
        self.url = "https://so.csdn.net/so/search/s.do?q="
        self.searchStr = searchStr
        self.displayCount = displayCount
        self.retList = []
        self.driver = driver

    def sortResult(self):
        def sortKey(item):
            return int(item[0])
        self.retList.sort(key=sortKey, reverse=True)

    def desplayResult(self):
        if self.displayCount > len(self.retList):
            self.displayCount = len(self.retList)
        for retItem in self.retList[:self.displayCount]:
            print("%10s  "%retItem[0], retItem[1])

    def run(self):
        self.url += self.searchStr
        self.driver.get(self.url)
        searchList = self.driver.find_elements_by_xpath("//div[@class='search-list-con']/dl")
        for searchItem in searchList:
            try:
                a = searchItem.find_element_by_xpath("./dt//a[1]")
                mr16 = searchItem.find_element_by_xpath("./dd//span[@class='mr16']")
            except:
                # print("Csdn error: ", sys.exc_info()[0])
                continue

            href = a.get_attribute('href')
            article = href[0:href.find('?')]
            times = mr16.text
            self.retList.append((times, article))

        self.sortResult()
        self.desplayResult()


class Mzitu():
    def __init__(self, driver, pages):
        # get User-Agent from chrome://version/
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
        self.url = "http://www.mzitu.com/zipai" # http://www.zbjuran.com'
        self.pages = pages
        self.driver = driver
        self.savedDir = "images"
        self.makeDir(self.savedDir)
        os.chdir(self.savedDir)

    def makeDir(self, path):
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)

    def saveImage(self, imgHref, imgName):
        img = requests.get(imgHref, headers=self.headers)
        # self.driver.get(imgHref)
        f = open(imgName, 'wb')
        f.write(img.content)
        f.close()
        print('save image %s' %imgName)

    def saveImages(self, imgHrefs):
        for imgHref in imgHrefs:
            imgName = imgHref[imgHref.rfind('/')+1:] # *.jpg
            if not os.path.exists(imgName):
                self.saveImage(imgHref, imgName)

    def run(self):
        self.driver.get(self.url)
        latestPageElem = self.driver.find_element_by_xpath("//div[@class='pagenavi-cm']/span[@aria-current='page']")
        latestPageNum = int(latestPageElem.text) # 453

        for page in range(pages):
            dirName = str(latestPageNum - page)
            self.makeDir(dirName)
            os.chdir(dirName)

            imgHrefs = []
            urlPage = self.url + '/comment-page-' + dirName + '/#comments'
            self.driver.get(urlPage)
            imgElemList = self.driver.find_elements_by_xpath("//div[@class='comment-body']/p/img")
            for imgElem in imgElemList:
                imgHref = imgElem.get_attribute('data-original')
                imgHrefs.append(imgHref)

            self.saveImages(imgHrefs)
            os.chdir("..")


def initChromeDriver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('log-level=3')
    driverPath = r'C:\softPackage\chromedriver_win32\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=driverPath, options=options)
    return driver


if __name__ == '__main__':
    driver = initChromeDriver()

    '''
    # python spider.py "redis" 5
    searchStr = sys.argv[1]
    displayCount = int(sys.argv[2])
    csdn = Csdn(driver, searchStr, displayCount)
    csdn.run()
    '''

    # python spider.py 2
    pages = int(sys.argv[1])
    mzitu = Mzitu(driver, pages)
    mzitu.run()

    driver.quit()
