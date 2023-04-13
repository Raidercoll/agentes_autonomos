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
paragraph = big_div.find_elements(By.TAG_NAME, "p")
link_tag = big_div.find_elements(By.TAG_NAME, "a")

'''
offices = []
dic = {}
print(len(paragraph))
for i in range(0,len(paragraph), 2):
    dic[f"{paragraph[i].get_attribute('textContent')}"] = f"{paragraph[i+1].get_attribute('textContent')}"
    '''

for i in range(0, len(link_tag)):
    if link_tag[i].get_attribute('textContent').__contains__('@') == True:
        for j in range(0, len(paragraph)):
            if paragraph[j].get_attribute('textContent').__contains__('E-') == True:
                paragraph.insert(j, link_tag[i])
         
offices = []
dic = {}
print(len(paragraph))
for i in range(0,len(paragraph), 2):
    dic[f"{paragraph[i].get_attribute('textContent')}"] = f"{paragraph[i+1].get_attribute('textContent')}"
  
print(dic)         
# print(paragraph[0].get_attribute('textContent'))
# print(link_tag[0].get_attribute('textContent'))
