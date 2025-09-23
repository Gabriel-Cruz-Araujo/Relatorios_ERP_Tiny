import streamlit as st
import pandas as pd
import os
from datetime import datetime

def pegar_arquivo_mais_recente(pasta, vendedor_select):
    arquivos = os.listdir(pasta)
    arquivos_vendedor = [f for f in arquivos if vendedor_select.upper() in f.upper() and f.endswith('.xlsx')]

    def extrair_data(nome_arquivo):
        partes = nome_arquivo.split('_')
        data_str = partes[-1].replace('.xlsx', '')
        return datetime.strptime(data_str, '%d-%m-%Y')

    arquivos_vendedor.sort(key=extrair_data, reverse=True)
    return os.path.join(pasta, arquivos_vendedor[0]) if arquivos_vendedor else None

# Função para mostrar um card estilizado
def mostrar_card(coluna, label, valor, cor_fundo):
    card_style = f"""
        <div style="
            background-color: {cor_fundo};
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            color: white;
            font-weight: bold;
            font-size: 18px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        ">
            <div>{label}</div>
            <div style="font-size: 22px; margin-top: 5px;">{valor}</div>
        </div>
    """
    coluna.markdown(card_style, unsafe_allow_html=True)

def mostrar_painel_vendedor(vendedor_nome):
    st.title(f"Painel de Vendas - {vendedor_nome}")

    df_vendas = pd.read_excel("relatorio_mensal.xlsx")
    df_vendedor = df_vendas[df_vendas['nome_vendedor'].str.upper().str.contains(vendedor_nome.upper())]

    if df_vendedor.empty:
        st.warning(f"Nenhum dado encontrado para {vendedor_nome}.")
        return

    total_vendido = df_vendedor['total_pedido'].sum()
    num_clientes = df_vendedor['cliente'].nunique()
    ticket_medio = total_vendido / len(df_vendedor) if len(df_vendedor) > 0 else 0

    # Filtrar vendas da data atual
    hoje = datetime.today().date()
    df_vendedor['data_pedido'] = pd.to_datetime(df_vendedor['data_pedido'], dayfirst=True).dt.date
    vendas_hoje = df_vendedor[df_vendedor['data_pedido'] == hoje]
    valor_vendas_hoje = vendas_hoje['total_pedido'].sum() if not vendas_hoje.empty else 0

    # =========================
    # Cards de métricas estilizados
    # =========================
    col1, col2, col3, col4 = st.columns(4)
    mostrar_card(col1, "Total vendido", f"R$ {total_vendido:,.2f}", "#17D343")
    mostrar_card(col2, "Clientes atendidos", f"{num_clientes:,}", "#3B82F6")
    mostrar_card(col3, "Ticket médio", f"R$ {ticket_medio:,.2f}", "#F59E0B")
    mostrar_card(col4, f"Vendas em {hoje.strftime('%d/%m/%Y')}", f"R$ {valor_vendas_hoje:,.2f}", "#8B5CF6")

    # =========================
    # Top 10 produtos
    # =========================
    st.markdown("### Top 10 Produtos mais vendidos")
    produtos = df_vendedor['produtos'].str.split(", ", expand=True).stack().reset_index(level=1, drop=True)
    produtos_counts = produtos.value_counts().head(10).reset_index()
    produtos_counts.columns = ['Produto', 'Quantidade Vendida']
    st.table(produtos_counts.style.format({"Quantidade Vendida": "{:,.0f}"}))

    # =========================
    # Vendas por dia
    # =========================
    st.markdown("### Vendas por dia")
    vendas_por_dia_tot = df_vendedor.groupby('data_pedido')['total_pedido'].sum()
    # Corrigir formatação do índice de datas
    vendas_por_dia_tot.index = pd.to_datetime(vendas_por_dia_tot.index).to_series().dt.strftime('%d/%m/%Y')
    st.bar_chart(vendas_por_dia_tot)

    # =========================
    # Detalhes dos pedidos
    # =========================
    st.markdown("### Detalhes dos Pedidos")
    df_detalhes = df_vendedor[['data_pedido', 'cliente', 'total_pedido', 'produtos']].copy()
    df_detalhes['data_pedido'] = pd.to_datetime(df_detalhes['data_pedido'], dayfirst=True).dt.strftime('%d/%m/%Y')
    df_detalhes = df_detalhes.rename(columns={
        'data_pedido': 'Data do Pedido',
        'cliente': 'Cliente',
        'total_pedido': 'Total do Pedido (R$)',
        'produtos': 'Produtos Comprados'
    })
    st.dataframe(df_detalhes.style.format({"Total do Pedido (R$)": "R$ {:,.2f}"}).set_properties(**{'text-align': 'left'}))

    # =========================
    # Relatório clientes ativos/inativos
    # =========================
    pasta = r"C:\Users\equip\Documents\relatorios\relatorio_vendedores"
    arquivo_clientes = pegar_arquivo_mais_recente(pasta, vendedor_nome)
    if not arquivo_clientes:
        st.error(f"Nenhum arquivo de {vendedor_nome} encontrado na pasta.")
        return

    df_clientes = pd.read_excel(arquivo_clientes)
    df_ativos = df_clientes[df_clientes['Situação'].str.upper() == "ATIVO"]
    df_inativos = df_clientes[df_clientes['Situação'].str.upper() == "INATIVO"]

    st.subheader("Clientes Ativos")
    st.write(f"Total de clientes ativos: {len(df_ativos)}")
    st.dataframe(df_ativos.style.format({"Dias sem compra": "{:.0f}"}))

    st.subheader("Clientes Inativos")
    st.write(f"Total de clientes inativos: {len(df_inativos)}")
    st.dataframe(df_inativos.style.format({"Dias sem compra": "{:.0f}"}))


def pagina_vendedor_1():
    mostrar_painel_vendedor("Vanessa")

def pagina_vendedor_2():
    mostrar_painel_vendedor("Katllen")

def pagina_vendedor_3():
    mostrar_painel_vendedor("Gabriel")
