from datetime import datetime

def obter_datas_mes_atual():
    hoje = datetime.today()
    data_inicial = hoje.replace(day=1).strftime("%d/%m/%Y")
    data_final = hoje.strftime("%d/%m/%Y")
    return data_inicial, data_final


