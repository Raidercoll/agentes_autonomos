from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

# function to returns a list of textContent from a list of a selenium web elements
def get_text_content(elements_list):
    array = []
    for i in range(0, len(elements_list)):
        array.append(elements_list[i].get_attribute('textContent'))
        
    return array

# func to return a array without duplicates
def drop_duplicates(array):
    return list(dict.fromkeys(array))



# path to chromedriver
PATH = 'C:\Program Files (x86)\chromedriver.exe'

# instantiate a webdriver and oppen the url
browser = webdriver.Chrome(executable_path=PATH)
browser.get(url= "https://www.sejabtg.com/escritorios")


dictio = {'Razão Social':[],
          'CNPJ':[],
          'E-mail':[],
          'Endereço':[],
          'UF':[],
          'Cidade':[],
          'Bairro':[],
          'Sócio responsável':[],
          'Telefone':[],
          'Site':[],
          'Data contratação':[],
          'CEP':[]}

keys = list(dictio.keys())

j = 4
# j = 96
k = 0
# k = 46
while True:
    try:

        mother_div = browser.find_element(By.XPATH, f"//mat-expansion-panel[@class='mat-expansion-panel text-p2 accordion ng-tns-c71-{j} ng-star-inserted']")
        child_div = mother_div.find_element(By.XPATH, f"//div[@id='cdk-accordion-child-{k}']")
        div = child_div.find_element(By.XPATH, f"//div[@class='mat-expansion-panel-body ng-tns-c71-{j}']")
        
        title = div.find_elements(By.CLASS_NAME, "title")  
        content = div.find_elements(By.CLASS_NAME, "info") 

        title = drop_duplicates(get_text_content(title)) 
        content = drop_duplicates(get_text_content(content))
        
        for i in range(0, len(title)):
            if title[i] == 'Responsável pela filial':
                    title[i] = 'Sócio responsável'
            try: 
                if title[i] in keys:
                    dictio[title[i]].append(content[i])
                else:
                    dictio[title[i]] = [content[i]]     
            except:
                dictio[title[i]].append("")
                
        dif = list(set(keys) - set(title))

        for i in range(0, len(dif)):
            dictio[dif[i]].append("")
    
        k += 1
        j += 2
            
    except:
        print(f"j: {j}")
        break

pd.DataFrame(dictio).to_excel('btg.xlsx', index=False)
