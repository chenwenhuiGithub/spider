import sys


class Csdn():
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://so.csdn.net/so/search/s.do?q="
        self.retList = []
        self.displayCount = 0

    def __sortResult(self):
        def sortKey(item):
            return int(item[0])
        self.retList.sort(key=sortKey, reverse=True)

    def __desplayResult(self):
        if self.displayCount > len(self.retList):
            self.displayCount = len(self.retList)
        for retItem in self.retList[:self.displayCount]:
            print("%10s  "%retItem[0], retItem[1], retItem[2])

    def search(self, searchStr, displayCount):
        self.retList = []
        self.displayCount = displayCount
        searchUrl = self.url + searchStr

        self.driver.get(searchUrl)
        searchElemList = self.driver.find_elements_by_xpath("//div[@class='search-list-con']/dl")
        for searchElem in searchElemList:
            try:
                hrefElem = searchElem.find_element_by_xpath("./dt//a[1]")
                timesElem = searchElem.find_element_by_xpath("./dd//span[@class='mr16']")
            except:
                # print("Csdn error: ", sys.exc_info()[0])
                continue

            fullHref = hrefElem.get_attribute('href')
            href = fullHref[0:fullHref.find('?')]
            title = hrefElem.text
            times = timesElem.text
            self.retList.append((times, href, title))

        self.__sortResult()
        self.__desplayResult()
