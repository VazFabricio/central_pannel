import streamlit as st
import random
import pandas as pd
import numpy as np
import time
from conection import collect
import matplotlib.pyplot as plt
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import datetime



query = """SELECT login,
 lastactive,
 created_time FROM server.accounts;"""

df = collect(query)

# Converter a coluna 'timestamp' para datetime
df['lastactive'] = pd.to_datetime(df['lastactive'], unit='s')
df['lastactive'] = df['lastactive'].dt.strftime('%d-%m-%Y %H:%M:%S')

# Converter a coluna 'timestamp' para datetime
df['created_time'] = pd.to_datetime(df['created_time'], unit='s')
df['created_time'] = df['created_time'].dt.strftime('%d-%m-%Y %H:%M:%S')

df['created_time'] = pd.to_datetime(df['created_time'], dayfirst=True)
df['lastactive'] = pd.to_datetime(df['lastactive'], dayfirst=True)

# Agrupar por data de 'createtime' para ver o número de cadastros por dia
df['createtime_date'] = df['created_time'].dt.date
df['lastAccess_date'] = df['lastactive'].dt.date

# Contar o número de cadastros por dia
createtime_counts = df['createtime_date'].value_counts().sort_index()

# Contar o número de saídas por dia
lastAccess_counts = df['lastAccess_date'].value_counts().sort_index()

st.set_page_config(layout="wide")

st.title("Central de controle")
st.header("Dashboard")

last_five_days_created = createtime_counts[-10:]
last_five_days_lasted = lastAccess_counts[-10:]
delta_last_five_days_created = last_five_days_created.iloc[-1] - last_five_days_created.iloc[0]
delta_last_five_days_lasted = last_five_days_lasted.iloc[-1] - last_five_days_lasted.iloc[0]


col1, col2 = st.columns([1, 1])


with col1:
    st.metric(label="New Players", value=str(last_five_days_created.iloc[-1]), delta=str(delta_last_five_days_created))
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=createtime_counts.index,
        y=createtime_counts.values,
        marker_color='blue',
    ))
    fig.update_layout(
        title='Número de Cadastros por Dia',
        xaxis_title='Data',
        yaxis_title='Número de Cadastros',
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig)

with col2:
    st.metric(label="Players exit", value=str(last_five_days_lasted.iloc[-1]), delta=str(delta_last_five_days_lasted))
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=lastAccess_counts.index,
        y=lastAccess_counts.values,
        marker_color='red',
    ))
    fig.update_layout(
        title='Número de Saídas por Dia',
        xaxis_title='Data',
        yaxis_title='Número de Saídas',
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig)

query_money = """
SELECT 
account,
valor,
price,
currency,
status,
data
FROM server.site_donations;
 """

df_money = collect(query_money)


# Converter a coluna 'timestamp' para datetime
df_money['data'] = pd.to_datetime(df_money['data'], unit='s')
df_money['data'] = df_money['data'].dt.strftime('%d-%m-%Y %H:%M:%S')

df_money['data'] = pd.to_datetime(df_money['data'], dayfirst=True)
df_money = df_money[df_money['status']==4]

import plotly.graph_objects as go
import pandas as pd 

scatter = go.Scatter(
    x=df_money[df_money['currency'] == 'BRL']['data'],
    y=df_money[df_money['currency'] == 'BRL']['valor'],
    mode='markers', 
    name='Dispersão',
    marker=dict(color='blue')
)

line = go.Scatter(
    x=df_money[df_money['currency'] == 'BRL']['data'],
    y=df_money[df_money['currency'] == 'BRL']['valor'],
    mode='lines', 
    name='Linha Conectada',
    line=dict(color='rgba(0, 0, 255, 0.5)', width=1, dash='solid') 
)

layout = go.Layout(
    title='Income',
    xaxis=dict(title='Data'),
    yaxis=dict(title='Valor'),
)

fig2 = go.Figure(data=[scatter, line], layout=layout)

st.plotly_chart(fig2)
