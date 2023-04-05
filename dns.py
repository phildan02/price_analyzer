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

    except TimeoutException:
        print("Ошибка!")

    driver.quit()





root = Tk()
root.title("Анализ цен")
root.geometry("570x300")


ctgsExplLabel = ttk.Label(text="Категория:")
ctgsExplLabel.place(x=10, y=10)

categories = ["Мониторы", "Системные блоки", "Жёсткие диски"]
ctgsBox = ttk.Combobox(values=categories, state="readonly")
ctgsBox.current(0)
ctgsBox.place(x=80, y=10)


resourceFrame = ttk.LabelFrame(text="Ресурс", padding=[8, 4])
resourceFrame.place(x=10, y=40)

rsrcErr = ttk.Label(wraplength=95, foreground="red")
rsrcErr.place(x=10, y=130)

rsrcNames = ["DNS", "Ситилинк", "М.видео"]

rsrcVars = []
for t in range(3):
    rsrcVars.append(BooleanVar())
    rsrcVars[t].set(1)


rsrcCheckbtns = []

for k in range(3):
    rsrcCheckbtns.append(ttk.Checkbutton(
        resourceFrame, text=rsrcNames[k], variable=rsrcVars[k]))
    rsrcCheckbtns[k].pack(anchor=W)


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
        else:
            return False
    else:
        return True


digCheck = (root.register(is_digit), "%P", "%d", "%i")


prcMinEntry = ttk.Entry(width=10, validate="key", validatecommand=digCheck)
prcMinEntry.place(x=190, y=65)
prcMaxEntry = ttk.Entry(width=10, validate="key", validatecommand=digCheck)
prcMaxEntry.place(x=190, y=95)

prcRangeErr = ttk.Label(wraplength=135, foreground="red")
prcRangeErr.place(x=120, y=130)


brandFrame = ttk.LabelFrame(text="Бренд", padding=[8, 4])
brandFrame.place(x=270, y=40)

mntrBrands = ["Acer", "AOC", "Samsung", "Asus", "Dell"]

brandVars = []
for i in range(5):
    brandVars.append(BooleanVar())

brandCheckbtns = []

for n in range(5):
    brandCheckbtns.append(ttk.Checkbutton(
        brandFrame, text=mntrBrands[n], variable=brandVars[n]))

for m in range(3):
    brandCheckbtns[m].grid(row=m, column=0, sticky=W)

brandCheckbtns[3].grid(row=0, column=1, sticky=W)
brandCheckbtns[4].grid(row=1, column=1, sticky=W)


def brandAllFunc():
    j = 0
    if brandAllVar.get() == 1:
        for j in range(len(brandCheckbtns)):
            brandVars[j].set(1)
            brandCheckbtns[j]["state"] = DISABLED
    else:
        for j in range(len(brandCheckbtns)):
            brandCheckbtns[j]["state"] = NORMAL


brandAllVar = BooleanVar()
brandAllCheckbtn = ttk.Checkbutton(
    brandFrame, text="Все", variable=brandAllVar, command=brandAllFunc)
brandAllCheckbtn.grid(row=2, column=1, sticky=W)

brandErr = ttk.Label(wraplength=135, foreground="red")
brandErr.place(x=270, y=130)



notebook = ttk.Notebook()
notebook.pack(expand=True, fill=BOTH, padx=10, pady=[170, 10])
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

citilinkScrollbar = ttk.Scrollbar(
    notebook, orient=VERTICAL, command=tableCitilink.yview)
tableCitilink.configure(yscroll=citilinkScrollbar.set)
citilinkScrollbar.grid(row=0, column=1, sticky='nese', pady=[20, 0])


tableMvideo = ttk.Treeview(notebook, columns=columns, show="headings")
tableMvideo.grid(row=0, column=0)
tableMvideo.heading("name", text="Наименование товара", anchor=W)
tableMvideo.heading("price", text="Цена", anchor=W)

mvideoScrollbar = ttk.Scrollbar(
    notebook, orient=VERTICAL, command=tableMvideo.yview)
tableMvideo.configure(yscroll=mvideoScrollbar.set)
mvideoScrollbar.grid(row=0, column=1, sticky='nese', pady=[20, 0])


notebook.add(tableDns, text="DNS")
notebook.add(tableCitilink, text="Ситилинк")
notebook.add(tableMvideo, text="М.видео")


def correctnessCheck():
    for u in range(len(rsrcVars)):
        if rsrcVars[u].get() == True:
            rsrcErr["text"] = ""
            break
        elif u == len(rsrcVars) - 1:
            rsrcErr["text"] = "Выберите хотя бы один ресурс"
    
    if prcMinEntry.get() == "" or prcMaxEntry.get() == "" or int(prcMaxEntry.get()) < int(prcMinEntry.get()):
        prcRangeErr["text"] = "Введите корректный ценовой диапазон"
    else:
        prcRangeErr["text"] = ""
    
    for p in range(len(brandVars)):
        if brandVars[p].get() == True:
            brandErr["text"] = ""
            break
        elif p == len(brandVars) - 1:
            brandErr["text"] = "Выберите хотя бы один бренд"


    if rsrcErr["text"] == "" and prcRangeErr["text"] == "" and brandErr["text"] == "":
        getPrices()



getBtn = ttk.Button(text="Получить данные", padding=[5, 0], command=correctnessCheck)
getBtn.place(x=440, y=47, height=83)


root.mainloop()