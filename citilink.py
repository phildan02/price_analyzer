from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import time


options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
# options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True
        )

url = "https://www.citilink.ru/catalog/monitory/?p=1&sorting=price_asc&pf=discount.any%2Crating.any&f=discount.any%2Crating.any%2Cavailable.all"

try:
    # global url
    prices = []
    names = []

    driver.get(url)
    prodCountTargetElem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'e1di3r8d0')))
    
    strTotalNumElems = driver.find_element(By.CLASS_NAME, 'e1di3r8d0').text
    if strTotalNumElems[-1] == "в":
        totalNumElems = int(strTotalNumElems[:-8])
    elif strTotalNumElems[-1] == "а":
        totalNumElems = int(strTotalNumElems[:-7])
    else:
        totalNumElems = int(strTotalNumElems[:-6])

    if totalNumElems == 0:
        # tableCitilink.insert("", END, values=("Товары не найдены", ""))
        driver.quit()
        # return


    pageNumElems = 48
    if totalNumElems < pageNumElems:
        lastPageIndex = 1
        lastPageNumElems = totalNumElems
    else:
        if totalNumElems % 48 == 0:
            lastPageIndex = totalNumElems / 48
            lastPageNumElems = 48
        else:
            lastPageIndex = totalNumElems // 48 + 1
            lastPageNumElems = totalNumElems - (lastPageIndex - 1) * 48


    urlPageIndStartPos = url.find("p=")
    urlPageIndEndPos = url.find("&", urlPageIndStartPos)

    urlWithoutPageInd = [url[:urlPageIndStartPos + 2], url[urlPageIndEndPos:]]

    pageIndex = 1
    while pageIndex <= lastPageIndex:
        if pageIndex != 1:
            driver.get(url)

        if pageIndex == lastPageIndex:
            pageNumElems = lastPageNumElems

        priceTargetElem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'e1j9birj0')))
        nameTargetElem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'e1259i3g0')))
            
        pagePriceElems = driver.find_elements(By.CLASS_NAME, 'e1j9birj0')
        pageNameElems = driver.find_elements(By.CLASS_NAME, 'e1259i3g0')

        while len(pagePriceElems) < pageNumElems or len(pageNameElems) < pageNumElems:
            time.sleep(0.5)
            pagePriceElems = driver.find_elements(By.CLASS_NAME, 'e1j9birj0')
            pageNameElems = driver.find_elements(By.CLASS_NAME, 'e1259i3g0')
            driver.execute_script("window.scrollBy(0, 600)")

        while len(pagePriceElems) > pageNumElems:
            pagePriceElems.pop()

        while len(pageNameElems) > pageNumElems:
            pageNameElems.pop()

        for x in pagePriceElems:
            prices.append(x.text)

        for y in pageNameElems:
            names.append(y.text)

        pageIndex += 1
        url = str(pageIndex).join(urlWithoutPageInd)

    print(prices)
    print(names)


except TimeoutException:
    print("Ошибка!")


driver.quit()