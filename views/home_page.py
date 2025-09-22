import streamlit as st
import pandas as pd
import plotly.express as px
import glob
import os
from datetime import datetime

def pagina_inicial():
    # =======================
    # Leitura de arquivos e tratamento de NaN
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

            # Converter data_pedido
            if 'data_pedido' in df_tmp.columns:
                df_tmp['data_pedido'] = pd.to_datetime(
                    df_tmp['data_pedido'], dayfirst=True, errors='coerce'
                )
            else:
                st.warning(f"Arquivo {arq} não possui 'data_pedido', será ignorado.")
                continue

            # Preencher NaN
            df_tmp = df_tmp.fillna({
                'cliente': 'Não informado',
                'Forma de Pagamento': 'Não informado',
                'Total do Pedido': 0,
                'data_pedido': pd.Timestamp.today()
            })

            dfs.append(df_tmp)
        except Exception as e:
            st.warning(f"Erro ao ler {arq}: {e}")

    if not dfs:
        st.error("Nenhum dado válido encontrado.")
        st.stop()

    df = pd.concat(dfs, ignore_index=True)

    # -----------------------
    # Filtro de datas
    # -----------------------
    datas_unicas = sorted(df['data_pedido'].dt.date.unique().tolist())
    datas_formatadas = [d.strftime("%d/%m/%Y") for d in datas_unicas]
    opcoes_datas = ["Todos"] + datas_formatadas

    datas_selecionadas = st.multiselect(
        "Selecione datas",
        options=opcoes_datas,
        default=["Todos"]
    )

    if "Todos" in datas_selecionadas:
        df_filtrado = df.copy()
    else:
        datas_convertidas = [pd.to_datetime(d, format="%d/%m/%Y").date() for d in datas_selecionadas]
        df_filtrado = df[df['data_pedido'].dt.date.isin(datas_convertidas)]

    # -----------------------
    # Filtro de formas de pagamento
    # -----------------------
    formas_pagamento = df_filtrado['Forma de Pagamento'].unique()
    opcoes_formas = ["Todas"] + list(formas_pagamento)

    formas_selecionadas = st.multiselect(
        "Selecione as Formas de Pagamento",
        options=opcoes_formas,
        default=["Todas"]
    )

    if "Todas" not in formas_selecionadas:
        df_filtrado = df_filtrado[df_filtrado['Forma de Pagamento'].isin(formas_selecionadas)]

    # -----------------------
    # KPIs estilizados
    # -----------------------
    col1, col2, col3, col4, col5 = st.columns(5)

    total_vendido = df_filtrado['Total do Pedido'].sum()
    qtd_clientes = df_filtrado['cliente'].nunique()
    ticket_medio = total_vendido / qtd_clientes if qtd_clientes > 0 else 0
    meta = 110000
    percentual_meta = (total_vendido / meta) * 100 if meta > 0 else 0

    # Prospecção de faturamento (dias úteis)
    hoje = datetime.today()
    ano = hoje.year
    mes = hoje.month
    primeiro_dia = datetime(ano, mes, 1)
    ultimo_dia = datetime(ano, mes, pd.Period(f'{ano}-{mes}').days_in_month)
    datas_mes = pd.date_range(primeiro_dia, ultimo_dia, freq='D')
    dias_uteis = datas_mes[datas_mes.weekday < 5]
    dias_uteis_passados = sum(dias_uteis <= hoje)
    dias_uteis_restantes = sum(dias_uteis > hoje)
    media_diaria_uteis = total_vendido / dias_uteis_passados if dias_uteis_passados > 0 else 0
    faturamento_projetado = total_vendido + (media_diaria_uteis * dias_uteis_restantes)

    # Função para exibir KPI em Markdown/HTML
    def kpi(col, titulo, valor, subtitulo=None, cor_valor=None, tamanho_valor=22):
        cor_html = f"color:{cor_valor};" if cor_valor else ""
        subtitulo_html = f"<p style='font-size:14px; margin:0;'>{subtitulo}</p>" if subtitulo else ""
        col.markdown(f"""
            <div style="text-align:center;">
                <p style="font-size:16px; margin:0;">{titulo}</p>
                <p style="font-size:{tamanho_valor}px; font-weight:bold; margin:0; {cor_html}">{valor}</p>
                {subtitulo_html}
            </div>
        """, unsafe_allow_html=True)

    kpi(col1, "Total Vendido", f"R$ {total_vendido:,.0f}")
    kpi(col2, "Clientes Únicos", qtd_clientes)
    kpi(col3, "Ticket Médio", f"R$ {ticket_medio:,.0f}")
    kpi(col4, "Faturamento Projetado", f"R$ {faturamento_projetado:,.0f}", tamanho_valor=20)
    
    if percentual_meta < 50:
        cor_meta = "#FF4B4B"  # vermelho
    elif percentual_meta > 100:
        cor_meta = "#FFD700"  # dourado ou qualquer cor que queira para acima de 100%
    else:
        cor_meta = "#17D343"  # verde
    
    kpi(col5, "Meta Atingida", f"{percentual_meta:.0f}%", 
        subtitulo=f"R$ {total_vendido:,.0f} / R$ {meta:,.0f}", 
        cor_valor=cor_meta)

    # -----------------------
    # Gráficos lado a lado
    # -----------------------
    chart_col1, chart_col2 = st.columns(2)

    # Top 10 Clientes
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

    # Gráfico de pizza
    df_pizza = df_filtrado.copy()
    fig_pie = px.pie(
        df_pizza,
        names='Forma de Pagamento',
        values='Total do Pedido',
        title="Distribuição por Forma de Pagamento",
        color='Forma de Pagamento',
        color_discrete_map={
            "Cartão": "#2E86C1",       # azul escuro
            "Dinheiro": "#28B463",     # verde
            "PIX": "#F39C12",          # laranja
            "Boleto": "#8E44AD",       # roxo
            "Não informado": "#95A5A6" # cinza
        }
    )
    chart_col2.plotly_chart(fig_pie, use_container_width=True)

    # -----------------------
    # Tabela detalhada
    # -----------------------
    st.subheader("Tabela Detalhada")
    st.dataframe(
        df_filtrado.assign(data_pedido=df_filtrado['data_pedido'].dt.strftime("%d/%m/%Y")),
        use_container_width=True
    )
