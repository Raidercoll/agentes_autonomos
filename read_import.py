import pandas as pd
from kpcon.Connections import connections as kpc
import os 
from sqlalchemy import text

PATH = os.path.dirname(os.path.abspath(__file__))
FILES_PATH = os.path.join(PATH, 'files')


df_orama = pd.read_excel(os.path.join(FILES_PATH, "ORAMA.xlsx" ))
df_genial = pd.read_excel(os.path.join(FILES_PATH, "GENIAL.xlsx" ))

df_orama.fillna("", inplace=True)

df_genial.columns = ["email"]
df_orama.columns = ["nome_empresa", "telefone", "email"]

with kpc.postgresql() as conn:
    df_orama.to_sql("agente", con=conn, schema="agentes_autonomos", index=False, index_label=False, if_exists="append")
    conn.commit()
    df_genial.to_sql("agente", con=conn, schema="agentes_autonomos", index=False, index_label=False, if_exists="append")
    conn.commit()