
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import plotly.express as px
import numpy as np
import datetime

def collect(query):
# Conectar ao MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="data@ccess",
        database="server"
    )
    cursor = conn.cursor()

    # Executar a query
    query =query
    cursor.execute(query)

    colunas = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(cursor.fetchall(), columns=colunas)

    # Fechar conexões
    cursor.close()
    conn.close()

    return df
