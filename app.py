from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


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
          'Telefone':[],
          'UF':[],
          'Site':[],
          'Cidade':[],
          'Data contratação':[],
          'Bairro':[],
          'CEP':[],
          'Sócio responsável':[]}

keys = dictio.keys()

j = 4
k = 0
while True:
    try:

        mother_div = browser.find_element(By.XPATH, f"//mat-expansion-panel[@class='mat-expansion-panel text-p2 accordion ng-tns-c71-{j} ng-star-inserted']")
        child_div = mother_div.find_element(By.XPATH, f"//div[@id='cdk-accordion-child-{k}']")
        div = child_div.find_element(By.XPATH, f"//div[@class='mat-expansion-panel-body ng-tns-c71-{j}']")
        
        title = div.find_elements(By.CLASS_NAME, "title")  
        content = div.find_elements(By.CLASS_NAME, "info") 

        title = get_text_content(title)
        content = get_text_content(content)
        
        for i in range(0, len(title)):
            if title[i] == 'Responsável pela filial':
                    title[i] = 'Sócio responsável'
                    
            if title[i] == 'Telefone':
                if "\xa0\xa0\xa0-\xa0\xa0\xa0(" in content[i]:
                    content.pop(i+1)
                    content.pop(i+1)
                elif ")" in content[i]:
                    content.pop(i+1)
                elif " - " in content[i]:
                    pass
                elif "" in content[i]:
                    pass
                else: 
                    content.insert(i, None)
                    
            try: 
                if title[i] in keys:
                    dictio[title[i]].append(content[i])
                else:
                    dictio[title[i]] = [content[i]]     
            except:
                dictio[title[i]].append(None)
                
        dif = list(set(keys) - set(title))

        for i in range(0, len(dif)):
            dictio[dif[i]].append(None)
    
        k += 1
        j += 2
        
    except:
        print(f"Foram captados {k} agentes!!")
        break

pd.DataFrame(dictio).to_excel('btg.xlsx', index=False)
