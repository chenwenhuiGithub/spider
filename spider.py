import sys
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


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

    searchStr = sys.argv[1]
    displayCount = int(sys.argv[2])
    csdn = Csdn(driver, searchStr, displayCount)
    csdn.run()

    driver.quit()
