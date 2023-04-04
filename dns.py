from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import time
from tkinter import *
from tkinter import ttk
import re


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
    driver.get(
        "https://www.dns-shop.ru/catalog/17a8a01d16404e77/smartfony/?review=1")
    try:
        targetElem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'product-buy__price')))

        strTotalNumElems = driver.find_element(
            By.CLASS_NAME, 'products-count').text
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
            else:
                i += 1

        prcsLabel["text"] = f'{str(prices[0])} - {str(prices[-1])}'

    except TimeoutException:
        prcsLabel["text"] = "Ошибка загрузки!"

    driver.quit()


root = Tk()
root.title("Анализ цен")
root.geometry("600x300")

ctgsExplLabel = ttk.Label(text="Категория:")
ctgsExplLabel.place(x=10, y=10)

categories = ["Мониторы", "Системные блоки", "Жёсткие диски"]
ctgsBox = ttk.Combobox(values=categories, state="readonly")
ctgsBox.place(x=80, y=10)

resourceFrame = ttk.LabelFrame(text="Ресурс", padding=[8, 4])
resourceFrame.place(x=10, y=40)

rsrcVars = []
for t in range(3):
    rsrcVars.append(BooleanVar())

dnsCheckbtn = ttk.Checkbutton(resourceFrame, text="DNS", variable=rsrcVars[0])
dnsCheckbtn.pack(anchor=W)

citilinkCheckbtn = ttk.Checkbutton(resourceFrame, text="Ситилинк", variable=rsrcVars[1])
citilinkCheckbtn.pack(anchor=W)

mvideoCheckbtn = ttk.Checkbutton(resourceFrame, text="М.видео", variable=rsrcVars[2])
mvideoCheckbtn.pack(anchor=W)


prcMinExplLabel = ttk.Label(text="Мин.цена")
prcMinExplLabel.place(x=120, y=65)
prcMaxExplLabel = ttk.Label(text="Макс.цена")
prcMaxExplLabel.place(x=120, y=95)

def is_digit(prcEntrySymb, oprCode, prcEntryInd):
    if int(oprCode) == 1:
        if prcEntryInd == prcEntrySymb:
            return False
        if prcEntrySymb.isdigit():
            return True
        else: return False
    else: return True

digCheck = (root.register(is_digit), "%P", "%d", "%i")

prcMinEntry = ttk.Entry(width=10, validate="key", validatecommand=digCheck)
prcMinEntry.place(x=190, y=65)
prcMaxEntry = ttk.Entry(width=10, validate="key", validatecommand=digCheck)
prcMaxEntry.place(x=190, y=95)


brandFrame = ttk.LabelFrame(text="Бренд", padding=[8, 4])
brandFrame.place(x=270, y=40)

mntrVars = []
for i in range(5):
    mntrVars.append(BooleanVar())

mntrAcerCheckbtn = ttk.Checkbutton(brandFrame, text="Acer", variable=mntrVars[0])
mntrAcerCheckbtn.grid(row=0, column=0, sticky=W)

mntrAocCheckbtn = ttk.Checkbutton(brandFrame, text="Aoc", variable=mntrVars[1])
mntrAocCheckbtn.grid(row=1, column=0, sticky=W)

mntrSamsungCheckbtn = ttk.Checkbutton(brandFrame, text="Samsung", variable=mntrVars[2])
mntrSamsungCheckbtn.grid(row=2, column=0, sticky=W)

mntrAsusCheckbtn = ttk.Checkbutton(brandFrame, text="Asus", variable=mntrVars[3])
mntrAsusCheckbtn.grid(row=0, column=1, sticky=W)

mntrDellCheckbtn = ttk.Checkbutton(brandFrame, text="Dell", variable=mntrVars[4])
mntrDellCheckbtn.grid(row=1, column=1, sticky=W)


mntrCheckbtns = [mntrAcerCheckbtn, mntrAocCheckbtn, mntrSamsungCheckbtn, mntrAsusCheckbtn, mntrDellCheckbtn]


def mntrAllFunc():
    j = 0
    if mntrAllVar.get() == 1:
        for j in range(len(mntrCheckbtns)):
            mntrVars[j].set(1)
            mntrCheckbtns[j]["state"] = DISABLED
    else:
        for j in range(len(mntrCheckbtns)):
            mntrCheckbtns[j]["state"] = NORMAL


mntrAllVar = BooleanVar()
mntrAllCheckbtn = ttk.Checkbutton(brandFrame, text="Все", variable=mntrAllVar, command=mntrAllFunc)
mntrAllCheckbtn.grid(row=2, column=1, sticky=W)



notebook = ttk.Notebook()
notebook.pack(expand=True, fill=BOTH, padx=10, pady=[150, 10])
notebook.rowconfigure(index=0, weight=1)
notebook.columnconfigure(index=0, weight=1)
notebook.columnconfigure(index=1, weight=1)


columns = ("name", "price")
tableDns = ttk.Treeview(notebook, columns=columns, show="headings")
tableDns.grid(row=0, column=0)
tableDns.heading("name", text="Наименование товара", anchor=W)
tableDns.heading("price", text="Цена", anchor=W)
monitor = ("Монитор AOC 24 LCD IPS", "13000")
tableDns.insert("", END, values=monitor)

dnsScrollbar = ttk.Scrollbar(notebook, orient=VERTICAL, command=tableDns.yview)
tableDns.configure(yscroll=dnsScrollbar.set)
dnsScrollbar.grid(row=0, column=1, sticky='nese', pady=[20, 0])



tableCitilink = ttk.Treeview(notebook, columns=columns, show="headings")
tableCitilink.grid(row=0, column=0)
tableCitilink.heading("name", text="Наименование товара", anchor=W)
tableCitilink.heading("price", text="Цена", anchor=W)

citilinkScrollbar = ttk.Scrollbar(notebook, orient=VERTICAL, command=tableCitilink.yview)
tableCitilink.configure(yscroll=citilinkScrollbar.set)
citilinkScrollbar.grid(row=0, column=1, sticky='nese', pady=[20, 0])


tableMvideo = ttk.Treeview(notebook, columns=columns, show="headings")
tableMvideo.grid(row=0, column=0)
tableMvideo.heading("name", text="Наименование товара", anchor=W)
tableMvideo.heading("price", text="Цена", anchor=W)

mvideoScrollbar = ttk.Scrollbar(notebook, orient=VERTICAL, command=tableMvideo.yview)
tableMvideo.configure(yscroll=mvideoScrollbar.set)
mvideoScrollbar.grid(row=0, column=1, sticky='nese', pady=[20, 0])


notebook.add(tableDns, text="DNS")
notebook.add(tableCitilink, text="Ситилинк")
notebook.add(tableMvideo, text="М.видео")


getBtn = ttk.Button(text="Получить данные", padding=[5, 0], command=getPrices)
getBtn.place(x=440, y=47, height=83)


root.mainloop()