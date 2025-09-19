from src.utils.enviar_email import enviar_para_email
from src.ETL.processamento import processando_planilha
from src.robos.gerar_vendas_ganhas import vendas_ganhas
from src.relatorios.relatorio_vendedor import relatorio_cliente_vendedor
from src.robos.gerar_relatorio_clientes_dia import gerar_relatorios_cliente_dia
from src.relatorios.relatorio_pedidos_de_venda_diario import relatorio_pdv_diario



def menu():
    """
    Função para gerar o Menu do sistema 
    com as opções selecionadas.
    
    """
    while True:
        print("\n=== MENU ===")
        print("1 - Relatório Clientes por Vendedor")
        print("2 - Relatório Clientes Trabalhados no Dia Anterior")
        print("3 - Relatório Vendas Ganhas")
        print("4 - Relatório Caixa")
        print("0 - Sair")
            
        opcao = input("Escolha uma opção: ")

        match opcao:
            case "1":
                while True:
                    print("\n=== Selecione o vendedor para Gerar o Relatório ===")
                    print("1 - Vanessa ")
                    print("2 - Katllen")
                    print("3 - Gabriel")
                    print("4 - Voltar")
                    escolha_vendedor = int(input("Escolha uma opção: "))
                    
                    if escolha_vendedor in [1, 2, 3]:
                        relatorio_cliente_vendedor(escolha_vendedor)
                        break  
                    elif escolha_vendedor == 4:
                        break
                    else:
                        print("Opção inválida! Escolha 1, 2 ou 3.")
            case "2":
                processando_planilha()
                enviar_para_email()
            case "3":
                vendas_ganhas()
            case "4":
                data = input("Digite a data que deseja tirar o caixa: ")
                relatorio_pdv_diario(data)
            case "0":
                print("Saindo do programa...")
                break
            case _:
                print("Opção inválida! Tente novamente.")
                
if __name__ == "__main__":
    menu()
