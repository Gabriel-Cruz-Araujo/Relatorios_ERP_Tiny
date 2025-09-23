from datetime import datetime, timedelta
import pandas as pd
from src.api.obter_relatorio_vendedor_mensal import pedidos_diarios_mensal

def relatorio_pdv_mensal(data_inicial, data_final, delay=2, arquivo_saida="relatorio_mensal.xlsx"):
    """
    Gera o relatório mensal de PDVs, chamando a API dia a dia.
    """
    # Converte datas
    inicio = datetime.strptime(data_inicial, "%d/%m/%Y")
    fim = datetime.strptime(data_final, "%d/%m/%Y")
    data_atual = inicio

    todos_pedidos = []

    while data_atual <= fim:
        data_str = data_atual.strftime("%d/%m/%Y")
        print(f"Consultando pedidos do dia: {data_str}")
        
        # Busca pedidos do dia
        pedidos = pedidos_diarios_mensal(data_str, data_str, delay=delay)
        if pedidos:
            todos_pedidos.extend(pedidos)
        else:
            print(f"Nenhum pedido encontrado em {data_str}")

        data_atual += timedelta(days=1)

    if not todos_pedidos:
        print(f"Nenhum pedido encontrado no período {data_inicial} até {data_final}. Relatório não gerado.")
        return

    # Cria DataFrame e salva em Excel
    df = pd.DataFrame(todos_pedidos)
    df.to_excel(arquivo_saida, index=False)
    print(f"Relatório gerado: {arquivo_saida}")
    
    
