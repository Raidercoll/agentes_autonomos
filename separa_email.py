import pandas as pd
from kpcon.Connections import connections as kpc
from sqlalchemy import text
import os
import  jpype
import datetime

# absolute path and files
PATH = os.path.dirname(os.path.abspath(__file__))
PATH_FILES = os.path.join(PATH, "files")
OUTPUT_PATH = os.path.join(PATH_FILES,"emails.txt")

# conect to the database
conn = kpc.postgresql()

# start the jvm to use the asposecells
jpype.startJVM()
from asposecells.api import Workbook

# convert the excel file to txt
workbook = Workbook(os.path.join(PATH_FILES, "emails.xlsx"))
workbook.save(OUTPUT_PATH)

jpype.shutdownJVM()

dictio = {
    'emails' : []
}

# read the txt file and clean the data 
with open(OUTPUT_PATH) as f:
    readed = f.read()
    f.close()
    
readed = readed.replace(" ; ", "\n").replace("; ", "\n").replace(" ;", "\n").replace(";", "\n").replace("|", "\n").replace(".br ", ".br\n").replace("\n\n", "\n")

# split the data in lines and delete the first and last line that are not necessary
readed = readed.splitlines()
readed.pop()
readed.pop(0)

# last clean in the data
readed = (lambda x : [i.lower().strip("<> '/\n") for i in x])(readed)
dictio['emails'] = readed

# transform the data in a dataframe and insert in the database
df = pd.DataFrame(dictio)
df['data_insercao'] = datetime.date.today().strftime("%Y-%m-%d")

df.to_sql("emails", con=conn, schema="agentes_autonomos", index=False, index_label=False, if_exists="append")
conn.commit()

print('inserido com sucesso!!')
