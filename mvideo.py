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
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True
        )


driver.get("https://www.mvideo.ru/komputernaya-tehnika-4107/sistemnye-bloki-80")
delay = 10
try:
    targetElem = WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'price__main-value')))

    totalNumElems = int(driver.find_element(By.CLASS_NAME, 'count').text)
    numElems = 24

    if totalNumElems < numElems:
        numElems = totalNumElems

    curNumElems = 0
    elems = []

    while len(elems) != numElems:
        while len(elems) == curNumElems:
            time.sleep(0.5)
            elems = driver.find_elements(By.CLASS_NAME, 'price__main-value')
        
        curNumElems = len(elems)
        driver.execute_script("window.scrollBy(0, 800)")


    prices = []
    for x in elems:
        prices.append(x.text[:-2])

    print(prices)

    f = open('data-mvideo.txt', 'w')
    f.write(str(prices))
    f.close()

except TimeoutException:
    print("Loading took too much time!")


driver.quit()