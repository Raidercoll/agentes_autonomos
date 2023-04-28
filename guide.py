import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_string(elements_list: webdriver) ->list:
    array = []
    for i in range(0, len(elements_list)):
        array.append(elements_list[i].get_attribute('textContent').replace("\n", "").replace("ô", "o").replace('ú', "u").replace("-","").replace(",", "").replace("çã", "ca").lower())        
    return array

def drop_duplicates(array: webdriver) -> list:
    array = list(dict.fromkeys(array))
    return array

# path to chromedriver 
PATH = 'C:\Program Files (x86)\chromedriver.exe'

dictio = { 'nome_empresa' : [], 
          'endereco' : [],
          'cep' : [],
          'bairro': [],
          'estado:':[],
          'cidade:':[],
          'telefone:' : [],
          'documento' : [],
          'email:':[],
          'site:' : [],
          'contratacao:':[],
          'agentes' : [],
          'origem' : []}

# instantiate a webdriver and oppen the url
browser = webdriver.Chrome(executable_path=PATH)
browser.get('https://www.guide.com.br/escritorios-credenciados/')

div = browser.find_element(By.XPATH, "//div[@class='boxBiblioteca']")

li = div.find_elements(By.TAG_NAME, "Li")
print(len(li))

for l in range(0, len(li)):
    content = drop_duplicates(get_string(li[l].find_elements(By.TAG_NAME, "p")))
    
    try:
        nome_empresa = li[l].find_element(By.CLASS_NAME, "the_title").get_attribute('textContent').replace("\n", "")
        dictio['nome_empresa'].append(nome_empresa)
    except:
        continue
    
    keys = []
    x = 0
    while True:
        split = content[x].split(" ")
        if split[0] == "":
            keys.append(split[1])
            x+=1
            continue
        
        keys.append(split[0])
        x+=1
        if split[0] == 'agentes' or x >= len(content):
            break
    
    if keys[0] != 'CEP':
        dictio['endereco'].append(content[0])
        dif = list(set(dictio.keys()) - (set(['nome_empresa', 'endereco'])))
        i = 1
    else:
        dif = list(set(dictio.keys()) - (set('nome_empresa')))
        i = 0
        
    if 'cnpj:' in keys or 'cpf:' in keys:
        try:
            dictio['documento'].append(content[keys.index('cnpj:')].split(":")[1])
            dif = list(set(dif) - set(['documento']))
            
        except:
            dictio['documento'].append(content[keys.index("cpf:")].split(":")[1])
            dif = list(set(dif) - set(['documento']))
            
    while True:
        try:
            key = keys[i]
            if key == 'cnpj:' or key == 'cpf:':
                i+=1
                continue
            
            if 'cep' in key:
                aux = content[i].split(' ')
                try:
                    dictio['cep'].append(aux[1])
                except:
                    dictio['cep'].append("")
                    
                try:
                    dictio['bairro'].append(" ".join(aux[2:len(aux)-1]))
                except:
                    dictio['bairro'].append("")
                    
                dif = list(set(dif) - (set(['cep','bairro']))) 
                i+=1
                continue
            
            dif = list(set(dif) - set([key]))
            
            if key == 'telefone:' and keys[i+1] == 'telefone:':
                tel = content[i].split(":")[1]
                i+=1
                while keys[i] == 'telefone:':
                    tel = tel + "; " + content[i].split(":")[1]
                    i+=1
                    
                dictio['telefone:'].append(tel)
                 
                continue 
                 
            if 'agentes' in key:
                agen = ''
                for j in range(i+1, len(content)):
                    agen = agen + content[j] + '; '
                    
                dictio['agentes'].append(agen)
                
                for k in range(0, len(dif)):
                    dictio[dif[k]].append("")
                    
                break
            
            dictio[key].append(content[i].split(': ')[1])
            
            i+=1
        
        except:
            for k in range(0, len(dif)):
                    dictio[dif[k]].append("")
            break
        
df = pd.DataFrame(dictio)
df['origem'] = "guide"
df.to_excel("files/guide.xlsx", index=False)