from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

def get_divs(browser, value):
    big_div = browser.find_element(By.XPATH, f"//div[@class='mat-expansion-panel-body ng-tns-c71-{value}']")
    div = big_div.find_elements(By.TAG_NAME, "p")
    return div

def get_offices_information(div) -> dict:
    dic = {}
    for i in range(0,len(div), 2):
        dic[f"{div[i].get_attribute('textContent')}"] = f"{div[i+1].get_attribute('textContent')}"
    
    return dic

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(url= "https://www.sejabtg.com/escritorios")
offices = []

for i in range(4, 8, 2):
    try:
        div = get_divs(browser, i)
        offices.append(get_offices_information(div))
    except:
        print(f"i: {i}\nbreak")
        break
    
print(offices[0])
    