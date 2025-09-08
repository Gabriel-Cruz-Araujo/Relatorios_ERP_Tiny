import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt
from src.relatorios.relatorio_vendedor import relatorio_cliente_vendedor
from src.utils.enviar_email import enviar_para_email
from src.ETL.processamento import processando_planilha

class MenuApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Relatórios")
        self.setGeometry(600, 300, 400, 350)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)  # Espaçamento entre widgets

        # Título
        self.title_label = QLabel("📊 MENU PRINCIPAL")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(self.title_label)

        # Botões menores e centralizados
        self.btn_rel_vendedor = QPushButton("Relatório Clientes por Vendedor")
        self.btn_rel_vendedor.setFixedSize(300, 40)
        self.btn_rel_vendedor.clicked.connect(self.relatorio_vendedor_ui)
        layout.addWidget(self.btn_rel_vendedor, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.btn_rel_dia = QPushButton("Relatório Clientes Trabalhados no Dia Anterior")
        self.btn_rel_dia.setFixedSize(300, 40)
        self.btn_rel_dia.clicked.connect(self.relatorio_dia)
        layout.addWidget(self.btn_rel_dia, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.btn_sair = QPushButton("Sair")
        self.btn_sair.setFixedSize(300, 40)
        self.btn_sair.clicked.connect(self.close)
        layout.addWidget(self.btn_sair, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(layout)

    # Função do relatório por vendedor
    def relatorio_vendedor_ui(self):
        # Criar janela para selecionar vendedor
        self.vendedor_window = QWidget()
        self.vendedor_window.setWindowTitle("Selecione o Vendedor")
        self.vendedor_window.setGeometry(650, 350, 300, 150)
        layout = QVBoxLayout()
        layout.setSpacing(15)

        layout.addWidget(QLabel("Escolha um vendedor:"))

        self.combo = QComboBox()
        self.combo.addItems(["Vanessa", "Katllen", "Gabriel"])
        layout.addWidget(self.combo)

        btn_gerar = QPushButton("Gerar Relatório")
        btn_gerar.setFixedSize(200, 35)
        btn_gerar.clicked.connect(self.gerar_relatorio_vendedor)
        layout.addWidget(btn_gerar, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.vendedor_window.setLayout(layout)
        self.vendedor_window.show()

    def gerar_relatorio_vendedor(self):
        escolha = self.combo.currentIndex() + 1  # 1, 2 ou 3
        relatorio_cliente_vendedor(escolha)
        QMessageBox.information(self, "Sucesso", "Relatório gerado com sucesso! ✅")
        self.vendedor_window.close()

    # Função do relatório do dia anterior
    def relatorio_dia(self):
        QMessageBox.information(self, "Processando", "⏳ Processando planilha...")
        processando_planilha()
        enviar_para_email()
        QMessageBox.information(self, "Sucesso", "Planilha processada e enviada com sucesso! 📧")

# Main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MenuApp()
    window.show()
    sys.exit(app.exec())
