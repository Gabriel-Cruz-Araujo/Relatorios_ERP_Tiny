# from src.robos.gerar_relatorio_clientes_dia import gerar_relatorios_cliente_dia
# from src.utils.menu_options import menu

# # gerar_relatorios_cliente_dia()
# menu()

from src.utils.menu_options import MenuApp
import sys
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MenuApp()
    window.show()
    sys.exit(app.exec())
