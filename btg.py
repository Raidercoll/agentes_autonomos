from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


# function to returns a list of textContent from a list of a selenium web elements
def get_text_content(elements_list):
    array = []
    for i in range(0, len(elements_list)):
        array.append(elements_list[i].get_attribute('textContent'))        
    return array

# path to chromedriver
PATH = 'C:\Program Files (x86)\chromedriver.exe'

# instantiate a webdriver and oppen the url
browser = webdriver.Chrome(executable_path=PATH)
browser.get(url= "https://www.sejabtg.com/escritorios")

# dictionary to store the data
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

# variables to iterate over the elements
j = 4
k = 0

while True:
    try:
        # find the element div of the agent
        mother_div = browser.find_element(By.XPATH, f"//mat-expansion-panel[@class='mat-expansion-panel text-p2 accordion ng-tns-c71-{j} ng-star-inserted']")
        child_div = mother_div.find_element(By.XPATH, f"//div[@id='cdk-accordion-child-{k}']")
        div = child_div.find_element(By.XPATH, f"//div[@class='mat-expansion-panel-body ng-tns-c71-{j}']")
        
        # title and content of the agent
        title = div.find_elements(By.CLASS_NAME, "title")  
        content = div.find_elements(By.CLASS_NAME, "info") 

        title = get_text_content(title)
        content = get_text_content(content)
        
        
        for i in range(0, len(title)):
            # adjust the title
            if title[i] == 'Responsável pela filial':
                    title[i] = 'Sócio responsável'
            
            # adjust the content in the 'Telefone' key
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
                    content.insert(i, None) # <-- if the content has no value, insert a None element on the position
                    
            # store the data in the dictionary
            if title[i] in keys: 
                dictio[title[i]].append(content[i])
            else:
                dictio[title[i]] = [content[i]] # <-- if the key is not in the dictionary, create a new key
    
        dif = list(set(keys) - set(title))

        # insert None in the keys that are not in the agent
        for i in range(0, len(dif)):
            dictio[dif[i]].append(None)
    
        k += 1
        j += 2
        
    except:
        print(f"Foram captados {k} agentes!!")
        break

pd.DataFrame(dictio).to_excel('./files/btg.xlsx', index=False)