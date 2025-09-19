from src.api.obter_ultimo_pdv import pedidos_diarios
import pandas as pd
import os
from datetime import datetime


def relatorio_pdv_diario(data):
    """
    Código para realizar a extração dos pedidos 
    diários do  sistema e salvando em duas pastas diferentes.
    
    """
    # data = "17/09/2025"
    pdv_diario = pedidos_diarios(data)

    if not pdv_diario:
        print(f"Nenhum pedido encontrado para a data {data}. Relatório não gerado.")
        return

    df = pd.DataFrame(pdv_diario)
    df["Total do Pedido"] = (
        df["Total do Pedido"].astype(str).str.replace(",", ".").astype(float)
    )

    # Agrupar totais por forma de pagamento
    totais = df.groupby("Forma de Pagamento")["Total do Pedido"].sum()

    # Criar linhas de resumo
    linhas_resumo = []
    for forma, valor in totais.items():
        linhas_resumo.append({
            "numero_pedido": f"TOTAL {forma}",
            "data_pedido": "",
            "cliente": "",
            "situacao": "",
            "Forma de Pagamento": "",
            "Total do Pedido": valor,
            "Conferencia": ""
        })

    # Total geral
    linhas_resumo.append({
        "numero_pedido": "TOTAL GERAL",
        "data_pedido": "",
        "cliente": "",
        "situacao": "",
        "Forma de Pagamento": "",
        "Total do Pedido": df["Total do Pedido"].sum(),
        "Conferencia": "",
        "Total Geral": df["Total do Pedido"].sum()
    })

    # Adicionar as linhas ao DataFrame
    df_resumo = pd.DataFrame(linhas_resumo)
    df_final = pd.concat([df, df_resumo], ignore_index=True)

    # Substituir NaN por string vazia para evitar erros
    df_final_filled = df_final.fillna("")

    # Criar pastas
    documentos = os.path.expanduser("~/Documents")
    pasta_relatorios = os.path.join(documentos, "relatorios")
    subpasta_pedidos = os.path.join(pasta_relatorios, "pedidos_de_venda")
    subpasta_pedidos_powerbi = os.path.join(pasta_relatorios, "pdv_power_bi")
    os.makedirs(subpasta_pedidos, exist_ok=True)
    os.makedirs(subpasta_pedidos_powerbi, exist_ok=True)

    # Nome do arquivo
    data_hoje = data.replace("/", "-")
    arquivo = os.path.join(
        subpasta_pedidos, f"relatorio_pedidos_de_venda_{data_hoje}.xlsx"
    )

    # Salvar Excel com bordas só nas células necessárias
    with pd.ExcelWriter(arquivo, engine="xlsxwriter") as writer:
        df_final_filled.to_excel(writer, index=False, sheet_name="Relatório")

        workbook = writer.book
        worksheet = writer.sheets["Relatório"]

        # Formatações
        border_fmt = workbook.add_format({"border": 1})   # borda fina
        bold_border = workbook.add_format({"border": 1, "bold": True})  # borda + negrito

        n_rows, n_cols = df_final_filled.shape

        # Aplicar borda e negrito
        for row in range(n_rows + 1):  # +1 para incluir header
            for col in range(n_cols):
                valor = df_final_filled.columns[col] if row == 0 else df_final_filled.iloc[row - 1, col]

                fmt = border_fmt
                if row > 0 and "TOTAL" in str(df_final_filled.iloc[row - 1, 0]):
                    fmt = bold_border

                worksheet.write(row, col, valor, fmt)

        # Ajustar largura das colunas
        for col_num, col_name in enumerate(df_final_filled.columns):
        # Maior tamanho entre o cabeçalho e os valores da coluna
            max_len = max(
                df_final_filled[col_name].astype(str).map(len).max(),
                len(col_name)
            )
            # Adicionar um pequeno extra para folga
            worksheet.set_column(col_num, col_num, max_len + 5)

        # Ativar gridlines para consistência
        worksheet.print_gridlines = True
        worksheet.show_gridlines = True

    print(f"Arquivo Excel criado: {arquivo}")
    
#============================== Gerando arquivo excell para o power_bi ===============================
    totais_dict = df.groupby("Forma de Pagamento")["Total do Pedido"].sum().to_dict()
    totais_dict["TOTAL GERAL"] = df["Total do Pedido"].sum()

    # Criar dataframe com os pedidos normais
    df_resumo_colunas = df.copy()

    # Adicionar os totais em colunas no final
    for forma, valor in totais_dict.items():
        df_resumo_colunas[forma] = ""

    # Inserir uma linha final com os totais em colunas
    linha_total = {col: "" for col in df_resumo_colunas.columns}
    for forma, valor in totais_dict.items():
        linha_total[forma] = valor
    df_resumo_colunas = pd.concat(
        [df_resumo_colunas, pd.DataFrame([linha_total])], ignore_index=True
    )

    # Salvar
    arquivo_resumo = os.path.join(
        subpasta_pedidos_powerbi, f"relatorio_pedidos_de_venda_powerbi_{data_hoje}.xlsx"
    )
    df_resumo_colunas.to_excel(arquivo_resumo, index=False)
    print(f"Planilha para o powerbi criada em: {arquivo_resumo}")


if __name__ == "__main__":
    relatorio_pdv_diario()
