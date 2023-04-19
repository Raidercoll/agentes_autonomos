import pandas as pd
from kpcon.Connections import connections as kpc
import os 
from sqlalchemy import text

# conection com o banco
conn = kpc.postgresql()

# PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.getcwd()
FILES_PATH = os.path.join(PATH, 'files')

QUERY = "select * from agentes_autonomos.agente"
QUERY_DEL = "delete from agentes_autonomos.agente"

df_orama = pd.read_excel(os.path.join(FILES_PATH, "ORAMA.xlsx" ))
df_genial = pd.read_excel(os.path.join(FILES_PATH, "GENIAL.xlsx" ))
df_btg = pd.read_excel(os.path.join(FILES_PATH, "btg.xlsx" ))

# df_orama.fillna("", inplace=True)

df_genial.columns = ["email"]
df_genial['origem'] = 'genial'

df_orama.columns = ["nome_empresa", "telefone", "email"]
df_orama['origem'] = 'orama'

df_btg = df_btg.drop(columns=["Data contratação", "Bairro"])
df_btg.columns = ["nome_empresa", "documento", "email", "endereco", "telefone", "uf", "site", "cidade", "cep" , "nome_agente"]
df_btg['origem'] = 'btg'

agentes_db = pd.read_sql(text(QUERY), conn)

agentes = pd.concat([agentes_db,df_genial, df_orama, df_btg])
agentes.drop_duplicates(inplace=True)

agentes['uf'] = agentes['uf'].apply(lambda x: str(x).replace(" ", "").replace("nan", ""))

conn.execute(text(QUERY_DEL))

agentes.to_sql("agente", con=conn, schema="agentes_autonomos", index=False, index_label=False, if_exists="append")
conn.commit()