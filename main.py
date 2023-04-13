from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import time
from tkinter import *
from tkinter import ttk
from threading import Thread


options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
# options.add_argument("--headless")



def dnsGetData():
    driver = webdriver.Chrome(options=options)

    stealth(driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True)

    try:
        global dnsUrl

        prices = []
        names = []
        
        driver.get(dnsUrl)
        prodCountTargetElem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'products-count')))
        
        strTotalNumElems = driver.find_element(By.CLASS_NAME, 'products-count').text
        if strTotalNumElems[-1] == "в":
            totalNumElems = int(strTotalNumElems[:-8])
        elif strTotalNumElems[-1] == "а":
            totalNumElems = int(strTotalNumElems[:-7])
        else:
            totalNumElems = int(strTotalNumElems[:-6])

        if totalNumElems == 0:
            tableDns.insert("", END, values=("Товары не найдены", ""))
            driver.quit()
            return

        pageNumElems = 18
        if totalNumElems < pageNumElems:
            lastPageIndex = 1
            lastPageNumElems = totalNumElems
        else:
            if totalNumElems % 18 == 0:
                lastPageIndex = totalNumElems / 18
                lastPageNumElems = 18
            else:
                lastPageIndex = totalNumElems // 18 + 1
                lastPageNumElems = totalNumElems - (lastPageIndex - 1) * 18


        urlPageIndPos = dnsUrl.find("p=")
        urlWithoutPageInd = dnsUrl[:urlPageIndPos + 2]
        
        pageIndex = 1
        while pageIndex <= lastPageIndex:
            if pageIndex != 1:
                driver.get(dnsUrl)

            if pageIndex == lastPageIndex:
                pageNumElems = lastPageNumElems

            priceTargetElem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-buy__price')))
            nameTargetElem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'catalog-product__name')))
            
            pagePriceElems = driver.find_elements(By.CLASS_NAME, 'product-buy__price')
            pageNameElems = driver.find_elements(By.CLASS_NAME, 'catalog-product__name')

            while len(pagePriceElems) != pageNumElems or len(pageNameElems) != pageNumElems:
                time.sleep(0.5)
                pagePriceElems = driver.find_elements(By.CLASS_NAME, 'product-buy__price')
                pageNameElems = driver.find_elements(By.CLASS_NAME, 'product-buy__price')
                driver.execute_script("window.scrollBy(0, 800)")

            for x in pagePriceElems:
                prices.append(x.text[:-2])

            for y in pageNameElems:
                names.append(y.text)

            pageIndex += 1
            dnsUrl = urlWithoutPageInd + str(pageIndex)


        i = 0
        while i < len(prices):
            index = prices[i].find("\n")
            if index != -1:
                prices[i] = prices[i][:(index - 2)]
            else:
                i += 1


        for g in range(len(prices)):
            tableDns.insert("", END, values=(names[g], prices[g]))

        l = 0
        for k in tableDns.get_children(""):
            l += 1
        print(l)


    except TimeoutException:
        for g in range(len(prices)):
            tableDns.insert("", END, values=(names[g], prices[g]))
        print("Ошибка!")

    driver.quit()





def citilinkGetData():
    driver = webdriver.Chrome(options=options)

    stealth(driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True)

    try:
        global citilinkUrl

        prices = []
        names = []

        driver.get(citilinkUrl)

        prodCategoryTitleElem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'e1e4gwta0')))
        prodTitleCountElem = driver.find_element(By.CLASS_NAME, 'e5lybcd0').find_elements(By.CSS_SELECTOR, '*')

        if len(prodTitleCountElem) == 1:
            tableCitilink.insert("", END, values=("Товары не найдены", ""))
            driver.quit()
            return


        citilinkPrcRangeTargetElem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'eklthoe0')))
        citilinkPrcRangeElems = driver.find_element(By.CLASS_NAME, 'eklthoe0').find_elements(By.TAG_NAME, 'input')
        
        citilinkPrcRange = []
        for t in range(2):
            citilinkPrcRange.append(citilinkPrcRangeElems[t].get_attribute("value"))
        print("HISUIGHIGUWRH(&*^&*&%^&*%*)")
        print(citilinkPrcRange)
        print("HISUIGHIGUWRH(&*^&*&%^&*%*)")

        strTotalNumElems = prodTitleCountElem[1].text
        if strTotalNumElems[-1] == "в":
            totalNumElems = int(strTotalNumElems[:-8])
        elif strTotalNumElems[-1] == "а":
            totalNumElems = int(strTotalNumElems[:-7])
        else:
            totalNumElems = int(strTotalNumElems[:-6])

        if totalNumElems == 0:
            tableCitilink.insert("", END, values=("Товары не найдены", ""))
            driver.quit()
            return


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


        urlPageIndStartPos = citilinkUrl.find("p=")
        urlPageIndEndPos = citilinkUrl.find("&", urlPageIndStartPos)

        urlWithoutPageInd = [citilinkUrl[:urlPageIndStartPos + 2], citilinkUrl[urlPageIndEndPos:]]

        pageIndex = 1
        while pageIndex <= lastPageIndex:
            if pageIndex != 1:
                driver.get(citilinkUrl)

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
            citilinkUrl = str(pageIndex).join(urlWithoutPageInd)

        for g in range(len(prices)):
            tableCitilink.insert("", END, values=(names[g], prices[g]))

        l = 0
        for k in tableCitilink.get_children(""):
            l += 1
        print(l)


    except TimeoutException:        
        for g in range(len(prices)):
            tableCitilink.insert("", END, values=(names[g], prices[g]))
        print("Ошибка!")

    driver.quit()













root = Tk()
root.title("Цены на товары")
root.geometry("595x400")


ctgsExplLabel = ttk.Label(text="Категория:")
ctgsExplLabel.place(x=10, y=10)

categories = ["Мониторы", "Системные блоки", "USB-флешки"]
ctgsBox = ttk.Combobox(values=categories, state="readonly")
ctgsBox.current(0)
ctgsBox.place(x=80, y=10)

mntrBrands = ["Acer", "AOC", "Dell", "LG", "Samsung"]
pcBrands = ["Acer", "Asus", "IRU", "Lenovo", "MSI"]
usbFlashBrands = ["A-DATA", "Kingston", "Sandisk", "Silicon Power", "Smartbuy"]


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


def is_digit(prcEntrySymb, oprCode, textBeforeChange):
    if int(oprCode) == 1:
        if prcEntrySymb.isdigit() and textBeforeChange != "0":
            return True
        else:
            return False
    else:
        return True


digCheck = (root.register(is_digit), "%P", "%d", "%s")


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
        if rsrcVars[0].get():
            global dnsUrl
            dnsUrlPriceRange = f'price={prcMinEntry.get()}-{prcMaxEntry.get()}'
            dnsUrlBrands = "brand="
            for e in range(5):
                if brandVars[e].get() == 1:
                    dnsUrlBrands += brandNamesVars[e].get().lower().replace(' ', '').replace('-', '') + "-"
            dnsUrlBrands = dnsUrlBrands[:-1]

            if ctgsBox.current() == 0:
                dnsUrl = f'https://www.dns-shop.ru/catalog/17a8943716404e77/monitory/?{dnsUrlPriceRange}&{dnsUrlBrands}&p=1'
            elif ctgsBox.current() == 1:
                dnsUrl = f'https://www.dns-shop.ru/catalog/17a8932c16404e77/personalnye-kompyutery/?{dnsUrlPriceRange}&{dnsUrlBrands}&p=1'
            else:
                dnsUrl = f'https://www.dns-shop.ru/catalog/ce3bebe8448b4e77/usb-flash/?{dnsUrlPriceRange}&{dnsUrlBrands}&p=1'

        
        if rsrcVars[1].get():
            global citilinkUrl
            citilinkUrlBrandsArr = []
            for e in range(5):
                if brandVars[e].get() == 1:
                    citilinkUrlBrandsArr.append(brandNamesVars[e].get().lower().replace(' ', '%20'))
            citilinkUrlBrands = ""
            for p in range(len(citilinkUrlBrandsArr)):
                citilinkUrlBrands += "%2C" + citilinkUrlBrandsArr[p]
            citilinkUrlBrandsCrop = ""
            for p in range(len(citilinkUrlBrandsArr) - 1):
                citilinkUrlBrandsCrop += "%2C" + citilinkUrlBrandsArr[p]

            if ctgsBox.current() == 0:
                citilinkUrl = f'https://www.citilink.ru/catalog/monitory/?p=1&sorting=price_asc&pf=available.all%2Cdiscount.any%2Crating.any{citilinkUrlBrandsCrop}&f=available.all%2Cdiscount.any%2Crating.any{citilinkUrlBrands}&pprice_min={prcMinEntry.get()}&pprice_max={prcMaxEntry.get()}&price_min={prcMinEntry.get()}&price_max={prcMaxEntry.get()}'
            elif ctgsBox.current() == 1:
                citilinkUrl = f'https://www.citilink.ru/catalog/sistemnye-bloki/?p=1&sorting=price_asc&pf=available.all%2Cdiscount.any%2Crating.any{citilinkUrlBrandsCrop}&f=available.all%2Cdiscount.any%2Crating.any{citilinkUrlBrands}&pprice_min={prcMinEntry.get()}&pprice_max={prcMaxEntry.get()}&price_min={prcMinEntry.get()}&price_max={prcMaxEntry.get()}'
            else:
                citilinkUrl = f'https://www.citilink.ru/catalog/fleshki/?p=1&sorting=price_asc&pf=available.all%2Cdiscount.any%2Crating.any{citilinkUrlBrandsCrop}&f=available.all%2Cdiscount.any%2Crating.any{citilinkUrlBrands}&pprice_min={prcMinEntry.get()}&pprice_max={prcMaxEntry.get()}&price_min={prcMinEntry.get()}&price_max={prcMaxEntry.get()}'



        global rsrcThreads
        rsrcThreads = []

        rsrcThreads.append(Thread(target=dnsGetData))
        rsrcThreads.append(Thread(target=citilinkGetData))

        for m in range(2):
            rsrcThreads[m].daemon = True


        threadsControl = Thread(target=threadsControlFunc)
        threadsControl.daemon = True
        threadsControl.start()
        disableInterface()
        processInfo["text"] = "Получение информации о товарах..."

        if tableDns.get_children("") != ():
            for x in tableDns.get_children(""): 
                tableDns.delete(x)
        if tableCitilink.get_children("") != ():
            for x in tableCitilink.get_children(""): 
                tableCitilink.delete(x)
        if tableMvideo.get_children("") != ():
            for x in tableMvideo.get_children(""): 
                tableMvideo.delete(x)


def disableInterface():
    getBtn["state"] = DISABLED
    ctgsBox["state"] = DISABLED
    for a in range(3):
        rsrcCheckbtns[a]["state"] = DISABLED
    prcMinEntry["state"] = DISABLED
    prcMaxEntry["state"] = DISABLED
    for b in range(5):
        brandCheckbtns[b]["state"] = DISABLED
    brandAllCheckbtn["state"] = DISABLED

def enableInterface():
    getBtn["state"] = NORMAL
    ctgsBox["state"] = NORMAL
    for a in range(3):
        rsrcCheckbtns[a]["state"] = NORMAL
    prcMinEntry["state"] = NORMAL
    prcMaxEntry["state"] = NORMAL
    for b in range(5):
        brandCheckbtns[b]["state"] = NORMAL
    brandAllCheckbtn["state"] = NORMAL

def threadsControlFunc():
    for n in range(3):
        if rsrcVars[n].get():
            rsrcThreads[n].start()
            rsrcThreads[n].join()

    enableInterface()
    processInfo["text"] = ""


getBtn = ttk.Button(text="Получить данные", padding=[5, 0], command=correctnessCheck)
getBtn.place(x=470, y=47, width=120, height=83)

processInfo = ttk.Label(justify=CENTER, wraplength=120)
processInfo.place(x=530, y=135, anchor=N)


root.mainloop()