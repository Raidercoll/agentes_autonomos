import pandas as pd
from kpcon.Connections import connections as kpc
import os 
from sqlalchemy import text

# conect to the database
conn = kpc.postgresql()

# path and files
PATH = os.path.dirname(os.path.abspath(__file__))
FILES_PATH = os.path.join(PATH, 'files')

# querys used in this script
QUERY = "select * from agentes_autonomos.agente"
QUERY_DEL = "delete from agentes_autonomos.agente"
QUERY_FINAL = "select email from agentes_autonomos.agente where email is not NULL and email <> ' - '"

# read the excel files in the folder files
df_orama = pd.read_excel(os.path.join(FILES_PATH, "ORAMA.xlsx" ))
df_genial = pd.read_excel(os.path.join(FILES_PATH, "GENIAL.xlsx" ))
df_btg = pd.read_excel(os.path.join(FILES_PATH, "btg.xlsx" ))
df_guide = pd.read_excel(os.path.join(FILES_PATH, "guide.xlsx" ))

# change the columns names to the same name of the table in the database
# add the column origem to know where the data came from and delete the columns that are not necessary
df_genial.columns = ["email"]
df_genial['origem'] = 'genial'

df_orama.columns = ["nome_empresa", "telefone", "email"]
df_orama['origem'] = 'orama'

df_btg = df_btg.drop(columns=["Data contratação", "Bairro"])
df_btg.columns = ["nome_empresa", "documento", "email", "endereco", "telefone", "uf", "site", "cidade", "cep" , "nome_agente"]
df_btg['origem'] = 'btg'

df_guide = df_guide.drop(columns=['bairro', 'contratacao:'])
df_guide.columns = ["nome_empresa", "endereco", "cep", "uf", "cidade", 'telefone', 'documento', 'email', 'site' , "nome_agente", 'origem']

# select the data from the database
agentes_db = pd.read_sql(text(QUERY), conn)

# concat the data from the database with the data from the excel files deleting the duplicates
agentes = pd.concat([agentes_db,df_genial, df_orama, df_btg, df_guide])
agentes.drop_duplicates(inplace=True)

# clean the data in uf column
agentes['uf'] = agentes['uf'].apply(lambda x: str(x).replace(" ", "").replace("nan", ""))

# delete the data from the database and insert the new data
conn.execute(text(QUERY_DEL))

agentes.to_sql("agente", con=conn, schema="agentes_autonomos", index=False, index_label=False, if_exists="append")
conn.commit()

# get the emails from the database and save in a excel file
pd.read_sql(text(QUERY_FINAL), conn).to_excel(os.path.join(FILES_PATH, "emails.xlsx"), index=False)