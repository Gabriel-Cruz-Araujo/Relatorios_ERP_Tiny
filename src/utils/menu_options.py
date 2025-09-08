from src.relatorios.relatorio_vendedor import relatorio_cliente_vendedor
from src.robos.gerar_relatorio_clientes_dia import gerar_relatorios_cliente_dia
from src.ETL.processamento import processando_planilha

def menu():
    while True:
        print("\n=== MENU ===")
        print("1 - Relatório Clientes por Vendedor")
        print("2 - Relatório Clientes Trabalhados no Dia Anterior")
        print("0 - Sair")
            
        opcao = input("Escolha uma opção: ")

        match opcao:
            case "1":
                while True:
                    print("\n=== Selecione o vendedor para Gerar o Relatório ===")
                    print("1 - Vanessa ")
                    print("2 - Katllen")
                    print("3 - Gabriel")
                    escolha_vendedor = int(input("Escolha uma opção: "))
                    
                    if escolha_vendedor in [1, 2, 3]:
                        relatorio_cliente_vendedor(escolha_vendedor)
                        break  # Sai do loop interno e volta para o menu
                    else:
                        print("Opção inválida! Escolha 1, 2 ou 3.")
            case "2":
                processando_planilha()
            case "0":
                print("Saindo do programa...")
                break
            case _:
                print("Opção inválida! Tente novamente.")
                
if __name__ == "__main__":
    menu()
