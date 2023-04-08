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



try:
    driver.get("https://www.citilink.ru/catalog/monitory/")

    prodCountTargetElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'e1di3r8d0')))
    
    strTotalNumElems = driver.find_element(By.CLASS_NAME, 'e1di3r8d0').text
    if strTotalNumElems[-1] == "в":
        totalNumElems = int(strTotalNumElems[:-8])
    elif strTotalNumElems[-1] == "а":
        totalNumElems = int(strTotalNumElems[:-7])
    else:
        totalNumElems = int(strTotalNumElems[:-6])

    if totalNumElems == 0:
        driver.quit()

    print(totalNumElems) 

    # targetElem = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, 'e1j9birj0')))


    # totalNumElems = int(driver.find_element(By.CLASS_NAME, 'e1di3r8d0').text[:-8])
    # numElems = 48

    # if totalNumElems < numElems:
    #     numElems = totalNumElems

    # elems = driver.find_elements(By.CSS_SELECTOR, '.e1j9birj0.e106ikdt0.app-catalog-175fskm.e1gjr6xo0')

    # while len(elems) < numElems:
    #     time.sleep(0.5)
    #     elems = driver.find_elements(By.CSS_SELECTOR, '.e1j9birj0.e106ikdt0.app-catalog-175fskm.e1gjr6xo0')
    #     driver.execute_script("window.scrollBy(0, 400)")

    # while len(elems) > numElems:
    #     elems.pop()

    # prices = []
    # for x in elems:
    #     prices.append(x.text)

    # print(len(prices))
    # print(prices)
    
    # i = 0
    # while i < len(prices):
    #     index = prices[i].find("\n")
    #     if index != -1:
    #         prices[i] = prices[i][:(index - 2)]
    #     else: i+=1

    # f = open('data-citilink.txt', 'w')
    # f.write(str(prices))
    # f.close()

except TimeoutException:
    print("Ошибка!")


driver.quit()