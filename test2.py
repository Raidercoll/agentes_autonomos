import requests 
import pandas as pd
response = requests.get('https://www.sejabtg.com/escritorios')

print(response.text)