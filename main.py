import sys
import Csdn
import Mzitu
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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
    # python main.py "redis" 5
    searchStr = sys.argv[1]
    displayCount = int(sys.argv[2])
    csdn = Csdn.Csdn(driver)
    csdn.search(searchStr, displayCount)
    '''
    
    # python main.py 2
    pages = int(sys.argv[1])
    mzitu = Mzitu.Mzitu(driver)
    mzitu.downloadImages(pages)

    driver.quit()
