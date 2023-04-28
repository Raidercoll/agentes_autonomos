import pandas as pd
from kpcon.Connections import connections as kpc
from sqlalchemy import text
import os
import  jpype
import datetime

# absolute path and files
PATH = os.path.dirname(os.path.abspath(__file__))
PATH_FILES = os.path.join(PATH, "files")
OUTPUT_PATH = os.path.join(PATH_FILES,"Output.txt")

conn = kpc.postgresql()

jpype.startJVM()
from asposecells.api import Workbook
workbook = Workbook(os.path.join(PATH_FILES, "emails.xlsx"))
workbook.save(OUTPUT_PATH)

jpype.shutdownJVM()

dictio = {
    'emails' : []
}

with open(OUTPUT_PATH) as f:
    readed = f.read()
    f.close()
    
readed = readed.replace(" ; ", "\n").replace("; ", "\n").replace(" ;", "\n").replace(";", "\n").replace("|", "\n").replace(".br ", ".br\n").replace("\n\n", "\n")
readed = readed.splitlines()
readed.pop()
readed.pop(0)

readed = (lambda x : [i.lower().strip("<> '/\n") for i in x])(readed)
dictio['emails'] = readed

df = pd.DataFrame(dictio)
df['data_insercao'] = datetime.date.today().strftime("%Y-%m-%d")

df.to_sql("emails", con=conn, schema="agentes_autonomos", index=False, index_label=False, if_exists="append")
conn.commit()

print('inserido com sucesso!!')
