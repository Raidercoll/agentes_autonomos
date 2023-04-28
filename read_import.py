import pandas as pd
from kpcon.Connections import connections as kpc
import os 
from sqlalchemy import text

# conection com o banco
conn = kpc.postgresql()

PATH = os.path.dirname(os.path.abspath(__file__))
# PATH = os.getcwd()
FILES_PATH = os.path.join(PATH, 'files')

QUERY = "select * from agentes_autonomos.agente"
QUERY_DEL = "delete from agentes_autonomos.agente"
QUERY_FINAL = "select email from agentes_autonomos.agente where email is not NULL and email <> ' - '"

df_orama = pd.read_excel(os.path.join(FILES_PATH, "ORAMA.xlsx" ))
df_genial = pd.read_excel(os.path.join(FILES_PATH, "GENIAL.xlsx" ))
df_btg = pd.read_excel(os.path.join(FILES_PATH, "btg.xlsx" ))
df_guide = pd.read_excel(os.path.join(FILES_PATH, "guide.xlsx" ))

df_genial.columns = ["email"]
df_genial['origem'] = 'genial'

df_orama.columns = ["nome_empresa", "telefone", "email"]
df_orama['origem'] = 'orama'

df_btg = df_btg.drop(columns=["Data contratação", "Bairro"])
df_btg.columns = ["nome_empresa", "documento", "email", "endereco", "telefone", "uf", "site", "cidade", "cep" , "nome_agente"]
df_btg['origem'] = 'btg'

df_guide = df_guide.drop(columns=['bairro', 'contratacao:'])
df_guide.columns = ["nome_empresa", "endereco", "cep", "uf", "cidade", 'telefone', 'documento', 'email', 'site' , "nome_agente", 'origem']

agentes_db = pd.read_sql(text(QUERY), conn)

agentes = pd.concat([agentes_db,df_genial, df_orama, df_btg, df_guide])
agentes.drop_duplicates(inplace=True)

agentes['uf'] = agentes['uf'].apply(lambda x: str(x).replace(" ", "").replace("nan", ""))

conn.execute(text(QUERY_DEL))

agentes.to_sql("agente", con=conn, schema="agentes_autonomos", index=False, index_label=False, if_exists="append")
conn.commit()

pd.read_sql(text(QUERY_FINAL), conn).to_excel(os.path.join(FILES_PATH, "emails.xlsx"), index=False)