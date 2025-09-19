import streamlit as st
import pandas as pd
import plotly.express as px
import glob
import os

# =======================
# Leitura de arquivos
# =======================
pasta_relatorios = r"C:\Users\equip\Documents\relatorios\pdv_power_bi"
arquivos = glob.glob(os.path.join(pasta_relatorios, "*.xlsx"))

if not arquivos:
    st.error(f"Nenhum arquivo Excel encontrado em: {pasta_relatorios}")
    st.stop()

dfs = []
for arq in arquivos:
    try:
        df_tmp = pd.read_excel(arq)

        # Garantir que 'data_pedido' é datetime
        if 'data_pedido' in df_tmp.columns:
            df_tmp['data_pedido'] = pd.to_datetime(df_tmp['data_pedido'], dayfirst=True, errors='coerce')
        else:
            st.warning(f"Arquivo {arq} não possui a coluna 'data_pedido', será ignorado.")
            continue

        dfs.append(df_tmp)
    except Exception as e:
        st.warning(f"Erro ao ler {arq}: {e}")

if not dfs:
    st.error("Nenhum dado válido encontrado nos arquivos.")
    st.stop()

# Concatena todos os dados e remove linhas sem data
df = pd.concat(dfs, ignore_index=True)
df = df[df['data_pedido'].notna()]


#❗❗ Aviso para saber se os arquivos foram carregados ❗❗
# st.success(f"{len(df)} linhas carregadas de {len(dfs)} arquivos.")


# =======================
# TITULO DA PÀGINA
# =======================

st.title("Extratos da Terra")

# =======================
# Filtro de datas (multiselect com "Todos") formatado dd/mm/YYYY
# =======================
datas_unicas = sorted(df['data_pedido'].dropna().dt.date.unique().tolist())
datas_formatadas = [d.strftime("%d/%m/%Y") for d in datas_unicas]

opcoes_datas = ["Todos"] + datas_formatadas

datas_selecionadas = st.multiselect(
    "Selecione datas",
    options=opcoes_datas,
    default=["Todos"]
)

# Converter datas selecionadas de volta para datetime.date
if "Todos" in datas_selecionadas:
    df_filtrado = df.copy()
else:
    datas_convertidas = [pd.to_datetime(d, format="%d/%m/%Y").date() for d in datas_selecionadas]
    df_filtrado = df[df['data_pedido'].dt.date.isin(datas_convertidas)]

# =======================
# Filtro Forma de Pagamento
# =======================
formas_pagamento = df_filtrado['Forma de Pagamento'].unique()
opcoes_formas = ["Todas"] + list(formas_pagamento)

formas_selecionadas = st.multiselect(
    "Selecione as Formas de Pagamento",
    options=opcoes_formas,
    default=["Todas"]
)

# Filtra o dataframe
if "Todas" not in formas_selecionadas:
    df_filtrado = df_filtrado[df_filtrado['Forma de Pagamento'].isin(formas_selecionadas)]

# =======================
# KPIs
# =======================
col1, col2, col3, col4 = st.columns(4)

total_vendido = df_filtrado['Total do Pedido'].sum()
qtd_clientes = df_filtrado['cliente'].nunique()
ticket_medio = total_vendido / qtd_clientes if qtd_clientes > 0 else 0
meta = 110000
percentual_meta = (total_vendido / meta) * 100 if meta > 0 else 0

col1.metric("Total Vendido", f"R$ {total_vendido:,.0f}")
col2.metric("Clientes Únicos", qtd_clientes)
col3.metric("Ticket Médio", f"R$ {ticket_medio:,.0f}")
col4.metric("Meta Atingida", f"{percentual_meta:.0f}%", delta=f"R$ {total_vendido:,.0f} / R$ {meta:,.0f}")

# =======================
# Gráficos lado a lado
# =======================
chart_col1, chart_col2 = st.columns(2)

# Top 10 Clientes com % do total
df_clientes = (
    df_filtrado.groupby("cliente")['Total do Pedido']
    .sum()
    .reset_index()
    .sort_values(by="Total do Pedido", ascending=False)
)

total_vendido_filtro = df_clientes['Total do Pedido'].sum()
df_clientes['% do Total'] = (df_clientes['Total do Pedido'] / total_vendido_filtro * 100).round(1)
df_top10 = df_clientes.head(10)

fig_top10 = px.bar(
    df_top10,
    x="cliente",
    y="Total do Pedido",
    text=df_top10['% do Total'].apply(lambda x: f"{x:.1f}%"),
    title="Top 10 Clientes por Valor"
)
fig_top10.update_traces(textposition="outside")
chart_col1.plotly_chart(fig_top10, use_container_width=True)

# Gráfico de pizza (formas de pagamento)
df_pizza = df_filtrado.copy()
fig_pie = px.pie(
    df_pizza,
    names='Forma de Pagamento',
    values='Total do Pedido',
    title="Distribuição por Forma de Pagamento"
)
chart_col2.plotly_chart(fig_pie, use_container_width=True)


# =======================
# Tabela detalhada com data formatada
# =======================
st.subheader("Tabela Detalhada")
st.dataframe(
    df_filtrado.assign(data_pedido=df_filtrado['data_pedido'].dt.strftime("%d/%m/%Y")),
    use_container_width=True
)
