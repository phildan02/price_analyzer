from selenium import webdriver
# from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import undetected_chromedriver as uc

# options = webdriver.ChromeOptions()

driver = uc.Chrome()

# stealth(driver=driver,
#     languages=["ru-RU", "ru"],
#     vendor="Google Inc.",
#     platform="Win32",
#     webgl_vendor="Intel Inc.",
#     renderer="Intel Iris OpenGL Engine",
#     fix_hairline=True,
#     run_on_insecure_origins=True)


driver.get("https://www.dns-shop.ru/catalog/17a8a01d16404e77/smartfony/")

prodCountTargetElem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'products-count')))

strTotalNumElems = driver.find_element(By.CLASS_NAME, 'products-count').text
print(strTotalNumElems)
