import os
import requests
import threading


class Mzitu():
    def __init__(self, driver):
        self.driver = driver
        # get User-Agent info from chrome://version/
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
        self.urlHome = "http://www.mzitu.com/" # http://www.zbjuran.com'
        # self.modules = ["zipai", "xinggan", "mm", "hot"]
        self.modules = ["zipai"]
        self.dirHome = os.getcwd()

    def __makeDir(self, path):
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)

    def __saveImage(self, imgHref, imgName):
        img = requests.get(imgHref, headers=self.headers)
        # self.driver.get(imgHref)
        f = open(imgName, 'wb')
        f.write(img.content)
        f.close()

    def __saveImages(self, imgHrefList):
        def saveThread(imgHrefList, fileList):
            for imgHref in imgHrefList:
                imgName = imgHref[imgHref.rfind('/')+1:] # *.jpg
                if imgName not in fileList:
                    self.__saveImage(imgHref, imgName)

        threadList = []
        fileList = os.listdir('.')
        hrefListSize = len(imgHrefList)
        if hrefListSize < 4:
            thread1 = threading.Thread(target=saveThread, args=(imgHrefList, fileList))
            threadList.append(thread1)
        else:
            hrefThreadSize = int(hrefListSize/4)
            thread2 = threading.Thread(target=saveThread, args=(imgHrefList[0*hrefThreadSize:1*hrefThreadSize], fileList))
            thread3 = threading.Thread(target=saveThread, args=(imgHrefList[1*hrefThreadSize:2*hrefThreadSize], fileList))
            thread4 = threading.Thread(target=saveThread, args=(imgHrefList[2*hrefThreadSize:3*hrefThreadSize], fileList))
            thread5 = threading.Thread(target=saveThread, args=(imgHrefList[3*hrefThreadSize:], fileList))
            threadList.append(thread2)
            threadList.append(thread3)
            threadList.append(thread4)
            threadList.append(thread5)

        for thread in threadList:
            thread.start()

        for thread in threadList:
            thread.join()

    def downloadImages(self, pages):
        os.chdir(self.dirHome)

        savedDirRoot = "images"
        self.__makeDir(savedDirRoot)
        os.chdir(savedDirRoot)

        for module in self.modules:
            self.__makeDir(module)
            os.chdir(module)
            
            imgHrefList = []
            countBefore = len(os.listdir('.'))

            urlModule = self.urlHome + module
            self.driver.get(urlModule)
            pageLatestElem = self.driver.find_element_by_xpath("//div[@class='pagenavi-cm']/span[@aria-current='page']")
            pageLatest = int(pageLatestElem.text) # 453
            for page in range(pages):
                urlPage = urlModule + '/comment-page-' + str(pageLatest - page) + '/#comments'
                self.driver.get(urlPage)
                imgElemList = self.driver.find_elements_by_xpath("//div[@class='comment-body']/p/img")
                for imgElem in imgElemList:
                    imgHref = imgElem.get_attribute('data-original')
                    imgHrefList.append(imgHref)
            self.__saveImages(imgHrefList)

            countAfter = len(os.listdir('.'))
            print("saved %d images in dir:%s" %(countAfter-countBefore, module))

            os.chdir("..")
