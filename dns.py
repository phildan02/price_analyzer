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

url = ""

def dnsGetPrices():
    global url
    try:
        priceElems = []
        nameElems = []

        driver.get(url)
        prodCountTargetElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'products-count')))
        
        strTotalNumElems = driver.find_element(By.CLASS_NAME, 'products-count').text
        if strTotalNumElems[-1] == "в":
            totalNumElems = int(strTotalNumElems[:-8])
        else:
            totalNumElems = int(strTotalNumElems[:-7])

        numElems = 18

        if totalNumElems < numElems:
            numElems = totalNumElems

        if totalNumElems % 18 == 0:
            lastPageIndex = totalNumElems / 18
        else: 
            lastPageIndex = totalNumElems // 18 + 1
            lastPageNumElems = totalNumElems - (lastPageIndex - 1) * 18
        
        print(lastPageIndex)
        print(lastPageNumElems)

        pageIndex = 1
        while len(priceElems) != totalNumElems or len(nameElems) != totalNumElems:
            if pageIndex != 1:
                driver.get(url)

            if pageIndex == lastPageIndex:
                numElems = lastPageNumElems

            priceTargetElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-buy__price')))
            nameTargetElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'catalog-product__name')))
            
            pagePriceElems = driver.find_elements(By.CLASS_NAME, 'product-buy__price')
            pageNameElems = driver.find_elements(By.CLASS_NAME, 'catalog-product__name')

            while len(pagePriceElems) != numElems or len(pageNameElems) != numElems:
                time.sleep(0.5)
                pagePriceElems = driver.find_elements(By.CLASS_NAME, 'product-buy__price')
                pageNameElems = driver.find_elements(By.CLASS_NAME, 'product-buy__price')
                driver.execute_script("window.scrollBy(0, 800)")
            
            priceElems += pagePriceElems
            nameElems += pageNameElems

            pageIndex += 1
            url = url[:-1] + str(pageIndex)


        print(type(priceElems))
        prices = []
        for x in priceElems:
            prices.append(x.text[:-2])
        i = 0
        while i < len(prices):
            index = prices[i].find("\n")
            if index != -1:
                prices[i] = prices[i][:(index - 2)]
            else:
                i += 1

        names = []
        for y in nameElems:
            names.append(y.text)


        for g in range(len(prices)):
            tableDns.insert("", END, values=(names[g], prices[g]))


    except TimeoutException:
        print("Ошибка!")

    driver.quit()








root = Tk()
root.title("Анализ цен")
root.geometry("595x300")


ctgsExplLabel = ttk.Label(text="Категория:")
ctgsExplLabel.place(x=10, y=10)

categories = ["Мониторы", "Системные блоки", "USB-флешки"]
ctgsBox = ttk.Combobox(values=categories, state="readonly")
ctgsBox.current(0)
ctgsBox.place(x=80, y=10)

mntrBrands = ["Acer", "AOC", "Samsung", "Asus", "Dell"]
pcBrands = ["Acer", "Asus", "Hiper", "IRU", "MSI"]
usbFlashBrands = ["Kingston", "Mirex", "Silicon Power", "Smartbuy", "Sandisk"]


ctgsBoxLastValue = 0
def remembLastValue(event):
    global ctgsBoxLastValue
    ctgsBoxLastValue = ctgsBox.current()

ctgsBox.bind("<ButtonPress>", remembLastValue)


def brandsDeter(event):
    if ctgsBox.current() != ctgsBoxLastValue:
        for r in range(5):
            brandVars[r].set(0)
            brandCheckbtns[r]["state"] = NORMAL
            brandAllVar.set(0)
        if ctgsBox.current() == 0:
            for w in range(5):
                brandNamesVars[w].set(mntrBrands[w])
        elif ctgsBox.current() == 1:
            for w in range(5):
                brandNamesVars[w].set(pcBrands[w])
        else:
            for w in range(5):
                brandNamesVars[w].set(usbFlashBrands[w])

ctgsBox.bind("<<ComboboxSelected>>", brandsDeter)

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

brandVars = []
for i in range(5):
    brandVars.append(BooleanVar())

brandNamesVars = []
for q in range(5):
    brandNamesVars.append(StringVar())
    brandNamesVars[q].set(mntrBrands[q])


brandCheckbtns = []
for n in range(5):
    brandCheckbtns.append(ttk.Checkbutton(brandFrame, textvariable=brandNamesVars[n], variable=brandVars[n]))

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
brandAllCheckbtn = ttk.Checkbutton(brandFrame, text="Все", variable=brandAllVar, command=brandAllFunc)
brandAllCheckbtn.grid(row=2, column=1, sticky=W)

brandErr = ttk.Label(wraplength=135, foreground="red")
brandErr.place(x=270, y=130)



notebook = ttk.Notebook()
notebook.pack(expand=True, fill=BOTH, padx=10, pady=[170, 10])
columns = ("name", "price")


tableDnsFrame = ttk.Frame(notebook)
tableDnsFrame.pack()

tableDnsFrame.columnconfigure(index=0, weight=1)
tableDnsFrame.columnconfigure(index=1, weight=0)
tableDnsFrame.rowconfigure(index=0, weight=1)

tableDns = ttk.Treeview(tableDnsFrame, columns=columns, show="headings")
tableDns.heading("name", text="Наименование товара", anchor=W)
tableDns.heading("price", text="Цена", anchor=W)
tableDns.column("#1", width=400)
tableDns.grid(row=0, column=0, sticky='nsew')

dnsScrollbar = ttk.Scrollbar(tableDnsFrame, orient=VERTICAL, command=tableDns.yview)
tableDns.configure(yscroll=dnsScrollbar.set)
dnsScrollbar.grid(row=0, column=1, sticky='ns')


tableCitilinkFrame = ttk.Frame(notebook)
tableCitilinkFrame.pack()

tableCitilinkFrame.columnconfigure(index=0, weight=1)
tableCitilinkFrame.columnconfigure(index=1, weight=0)
tableCitilinkFrame.rowconfigure(index=0, weight=1)

tableCitilink = ttk.Treeview(tableCitilinkFrame, columns=columns, show="headings")
tableCitilink.heading("name", text="Наименование товара", anchor=W)
tableCitilink.heading("price", text="Цена", anchor=W)
tableCitilink.column("#1", width=400)
tableCitilink.grid(row=0, column=0, sticky='nsew')

citilinkScrollbar = ttk.Scrollbar(tableCitilinkFrame, orient=VERTICAL, command=tableCitilink.yview)
tableCitilink.configure(yscroll=citilinkScrollbar.set)
citilinkScrollbar.grid(row=0, column=1, sticky='ns')


tableMvideoFrame = ttk.Frame(notebook)
tableMvideoFrame.pack()

tableMvideoFrame.columnconfigure(index=0, weight=1)
tableMvideoFrame.columnconfigure(index=1, weight=0)
tableMvideoFrame.rowconfigure(index=0, weight=1)

tableMvideo = ttk.Treeview(tableMvideoFrame, columns=columns, show="headings")
tableMvideo.heading("name", text="Наименование товара", anchor=W)
tableMvideo.heading("price", text="Цена", anchor=W)
tableMvideo.column("#1", width=400)
tableMvideo.grid(row=0, column=0, sticky='nsew')

mvideoScrollbar = ttk.Scrollbar(tableMvideoFrame, orient=VERTICAL, command=tableMvideo.yview)
tableMvideo.configure(yscroll=mvideoScrollbar.set)
mvideoScrollbar.grid(row=0, column=1, sticky='ns')


notebook.add(tableDnsFrame, text="DNS")
notebook.add(tableCitilinkFrame, text="Ситилинк")
notebook.add(tableMvideoFrame, text="М.видео")



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
        global url
        if ctgsBox.current() == 0:
            url = "https://www.dns-shop.ru/catalog/17a8943716404e77/monitory/?price=8501-11000&p=1"
        elif ctgsBox.current() == 1:
            url = "https://www.dns-shop.ru/catalog/17a8932c16404e77/personalnye-kompyutery/?p=1"
        else:
            url = "https://www.dns-shop.ru/catalog/ce3bebe8448b4e77/usb-flash/?p=1"
        
        
        dnsGetPrices()



getBtn = ttk.Button(text="Получить данные", padding=[5, 0], command=correctnessCheck)
getBtn.place(x=470, y=47, height=83)


root.mainloop()