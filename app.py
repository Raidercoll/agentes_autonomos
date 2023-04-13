from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = 'C:\Program Files (x86)\chromedriver.exe'
browser = webdriver.Chrome(executable_path=PATH)

browser.get(url= "https://www.sejabtg.com/escritorios")

big_div = browser.find_element(By.XPATH, "//div[@class='mat-expansion-panel-body ng-tns-c71-4']")
                                        # "//div[@class='mat-expansion-panel-body ng-tns-c71-6']"
div = big_div.find_elements(By.CLASS_NAME, "ng-tns-c71-4")
# div[0].get_dom_attribute('textContent')
print(div[0].get_attribute('textContent'))



# offices = []
# dic = {}
# for i in range(0,len(div), 2):
#     dic[f"{div[i].get_attribute('textContent')}"] = f"{div[i+1].get_attribute('textContent')}"

# print(dic)
