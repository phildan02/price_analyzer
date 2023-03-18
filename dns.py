from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import time
from tkinter import *
from tkinter import ttk

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


def getPrices():
    driver.get("https://www.dns-shop.ru/catalog/17a8a01d16404e77/smartfony/?review=1")
    try:
        targetElem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'product-buy__price')))

        strTotalNumElems = driver.find_element(By.CLASS_NAME, 'products-count').text
        if strTotalNumElems[-1] == "в":
            totalNumElems = int(strTotalNumElems[:-8])
        else:
            totalNumElems = int(strTotalNumElems[:-7])
        
        numElems = 18

        if totalNumElems < numElems:
            numElems = totalNumElems

        elems = driver.find_elements(By.CLASS_NAME, 'product-buy__price')

        while len(elems) != numElems:
            time.sleep(0.5)
            elems = driver.find_elements(By.CLASS_NAME, 'product-buy__price')
            driver.execute_script("window.scrollBy(0, 800)")


        prices = []
        for x in elems:
            prices.append(x.text[:-2])
        
        i = 0
        while i < len(prices):
            index = prices[i].find("\n")
            if index != -1:
                prices[i] = prices[i][:(index - 2)]
            else: i+=1

        prcsLabel["text"] = f'{str(prices[0])} - {str(prices[-1])}'

    except TimeoutException:
        prcsLabel["text"]="Ошибка загрузки!"

    driver.quit()



def execution():
    prcsLabel["text"]="Идёт поиск цен..."
    getPrices()


root = Tk()
root.title("Анализ цен")
root.geometry("300x250")

prcsLabel = ttk.Label()
prcsLabel.pack(anchor=NW)

explLabel = ttk.Label(text="Выберите категорию товаров:")
explLabel.pack(anchor=NW)

categories = ["Системные блоки", "Мониторы", "Клавиатуры"]
ctgsBox = ttk.Combobox(values=categories)
ctgsBox.pack(anchor=NW)

getBtn = ttk.Button(text="Получить цены", command=execution)
getBtn.pack(anchor=NW)

root.mainloop()