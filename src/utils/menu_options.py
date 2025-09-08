# import sys
# import os
# from PyQt6.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
#     QComboBox, QMessageBox, QListWidget, QProgressBar
# )
# from PyQt6.QtCore import Qt
# from src.relatorios.relatorio_vendedor import relatorio_cliente_vendedor
# from src.utils.enviar_email import enviar_para_email
# from src.ETL.processamento import processando_planilha
# from datetime import datetime

# class MenuApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Sistema de Relatórios")
#         self.setGeometry(600, 300, 500, 450)
#         self.init_ui()

#     def init_ui(self):
#         self.layout = QVBoxLayout()
#         self.layout.setSpacing(15)

#         # Título
#         self.title_label = QLabel("📊 MENU PRINCIPAL")
#         self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.title_label.setStyleSheet("font-size: 22px; font-weight: bold;")
#         self.layout.addWidget(self.title_label)

#         # Botão Relatório por Vendedor
#         self.btn_rel_vendedor = QPushButton("Relatório Clientes por Vendedor")
#         self.btn_rel_vendedor.setFixedSize(300, 40)
#         self.btn_rel_vendedor.clicked.connect(self.mostrar_vendedor_opcoes)
#         self.layout.addWidget(self.btn_rel_vendedor, alignment=Qt.AlignmentFlag.AlignHCenter)

#         # Botão Relatório do Dia Anterior
#         self.btn_rel_dia = QPushButton("Relatório Clientes Trabalhados no Dia Anterior")
#         self.btn_rel_dia.setFixedSize(300, 40)
#         self.btn_rel_dia.clicked.connect(self.relatorio_dia)
#         self.layout.addWidget(self.btn_rel_dia, alignment=Qt.AlignmentFlag.AlignHCenter)

#         # Botão Sair
#         self.btn_sair = QPushButton("Sair")
#         self.btn_sair.setFixedSize(300, 40)
#         self.btn_sair.clicked.connect(self.close)
#         self.layout.addWidget(self.btn_sair, alignment=Qt.AlignmentFlag.AlignHCenter)

#         # ComboBox para escolher vendedor (inicialmente escondido)
#         self.combo_vendedor = QComboBox()
#         self.combo_vendedor.addItems(["Vanessa", "Katllen", "Gabriel"])
#         self.combo_vendedor.setFixedSize(200, 35)
#         self.combo_vendedor.setVisible(False)
#         self.layout.addWidget(self.combo_vendedor, alignment=Qt.AlignmentFlag.AlignHCenter)

#         # Botão Gerar Relatório (inicialmente escondido)
#         self.btn_gerar_vendedor = QPushButton("Gerar Relatório")
#         self.btn_gerar_vendedor.setFixedSize(200, 35)
#         self.btn_gerar_vendedor.clicked.connect(self.gerar_relatorio_vendedor)
#         self.btn_gerar_vendedor.setVisible(False)
#         self.layout.addWidget(self.btn_gerar_vendedor, alignment=Qt.AlignmentFlag.AlignHCenter)

#         # Barra de progresso (inicialmente escondida)
#         self.progress = QProgressBar()
#         self.progress.setVisible(False)
#         self.layout.addWidget(self.progress)

#         # Lista de relatórios gerados
#         self.lista_relatorios = QListWidget()
#         self.lista_relatorios.setFixedHeight(100)
#         self.layout.addWidget(self.lista_relatorios)

#         self.setLayout(self.layout)

#         # Caminho base para salvar relatórios
#         documentos = os.path.expanduser("~/Documents")
#         self.pasta_relatorios = os.path.join(documentos, "relatorios")
#         os.makedirs(self.pasta_relatorios, exist_ok=True)

#     # Mostrar combo e botão para escolher vendedor
#     def mostrar_vendedor_opcoes(self):
#         self.combo_vendedor.setVisible(True)
#         self.btn_gerar_vendedor.setVisible(True)

#     # Gerar relatório do vendedor
#     def gerar_relatorio_vendedor(self):
#         escolha = self.combo_vendedor.currentIndex() + 1
#         # Nome do arquivo de acordo com o vendedor
#         nomes = {1: "Vanessa", 2: "Katllen", 3: "Gabriel"}
#         nome_arquivo = f"relatorio_clientes_vendedor_{nomes[escolha]}.xlsx"
#         caminho_arquivo = os.path.join(self.pasta_relatorios, nome_arquivo)

#         # Processamento (simples, chamando a função existente)
#         self.progress.setVisible(True)
#         self.progress.setValue(0)
#         QApplication.processEvents()
#         relatorio_cliente_vendedor(escolha)  # Aqui você pode adaptar para salvar diretamente no caminho
#         self.progress.setValue(100)

#         # Adiciona à lista de relatórios gerados
#         self.lista_relatorios.addItem(caminho_arquivo)

#         QMessageBox.information(self, "Sucesso", f"Relatório gerado: {caminho_arquivo} ✅")
#         # Esconde combo e botão novamente
#         self.combo_vendedor.setVisible(False)
#         self.btn_gerar_vendedor.setVisible(False)
#         self.progress.setVisible(False)

#     # Relatório do dia anterior
#     def relatorio_dia(self):
#         QMessageBox.information(self, "Processando", "⏳ Processando planilha...")
#         self.progress.setVisible(True)
#         self.progress.setValue(0)
#         QApplication.processEvents()
#         processando_planilha()
#         enviar_para_email()
#         self.progress.setValue(100)
#         self.progress.setVisible(False)
#         QMessageBox.information(self, "Sucesso", "Planilha processada e enviada com sucesso! 📧")
#         # Opcional: adicionar à lista
#         self.lista_relatorios.addItem(os.path.join(self.pasta_relatorios, "Última planilha processada"))

# # Main
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MenuApp()
#     window.show()
#     sys.exit(app.exec())

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QComboBox, QMessageBox, QListWidget, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from src.relatorios.relatorio_vendedor import relatorio_cliente_vendedor
from src.utils.enviar_email import enviar_para_email
from src.ETL.processamento import processando_planilha

class WorkerThread(QThread):
    finished = pyqtSignal(str)  # sinal emitido quando terminar
    progress = pyqtSignal(int)  # sinal para atualizar barra de progresso

    def __init__(self, func, *args):
        super().__init__()
        self.func = func
        self.args = args

    def run(self):
        # Aqui você pode adicionar atualizações parciais de progresso se quiser
        self.progress.emit(50)
        self.func(*self.args)
        self.progress.emit(100)
        self.finished.emit("Concluído")

class MenuApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Relatórios")
        self.setGeometry(600, 300, 500, 450)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)

        # Título
        self.title_label = QLabel("📊 MENU PRINCIPAL")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        # Botão Relatório por Vendedor
        self.btn_rel_vendedor = QPushButton("Relatório Clientes por Vendedor")
        self.btn_rel_vendedor.setFixedSize(300, 40)
        self.btn_rel_vendedor.clicked.connect(self.mostrar_vendedor_opcoes)
        self.layout.addWidget(self.btn_rel_vendedor, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Botão Relatório do Dia Anterior
        self.btn_rel_dia = QPushButton("Relatório Clientes Trabalhados no Dia Anterior")
        self.btn_rel_dia.setFixedSize(300, 40)
        self.btn_rel_dia.clicked.connect(self.relatorio_dia)
        self.layout.addWidget(self.btn_rel_dia, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Botão Sair
        self.btn_sair = QPushButton("Sair")
        self.btn_sair.setFixedSize(300, 40)
        self.btn_sair.clicked.connect(self.close)
        self.layout.addWidget(self.btn_sair, alignment=Qt.AlignmentFlag.AlignHCenter)

        # ComboBox para escolher vendedor (inicialmente escondido)
        self.combo_vendedor = QComboBox()
        self.combo_vendedor.addItems(["Vanessa", "Katllen", "Gabriel"])
        self.combo_vendedor.setFixedSize(200, 35)
        self.combo_vendedor.setVisible(False)
        self.layout.addWidget(self.combo_vendedor, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Botão Gerar Relatório (inicialmente escondido)
        self.btn_gerar_vendedor = QPushButton("Gerar Relatório")
        self.btn_gerar_vendedor.setFixedSize(200, 35)
        self.btn_gerar_vendedor.clicked.connect(self.iniciar_relatorio_vendedor)
        self.btn_gerar_vendedor.setVisible(False)
        self.layout.addWidget(self.btn_gerar_vendedor, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Barra de progresso
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.layout.addWidget(self.progress)

        # Lista de relatórios gerados
        self.lista_relatorios = QListWidget()
        self.lista_relatorios.setFixedHeight(100)
        self.layout.addWidget(self.lista_relatorios)

        self.setLayout(self.layout)

        # Caminho base para salvar relatórios
        documentos = os.path.expanduser("~/Documents")
        self.pasta_relatorios = os.path.join(documentos, "relatorios")
        os.makedirs(self.pasta_relatorios, exist_ok=True)

    # Mostrar combo e botão para escolher vendedor
    def mostrar_vendedor_opcoes(self):
        self.combo_vendedor.setVisible(True)
        self.btn_gerar_vendedor.setVisible(True)

    # Inicia thread para relatório por vendedor
    def iniciar_relatorio_vendedor(self):
        escolha = self.combo_vendedor.currentIndex() + 1
        nomes = {1: "Vanessa", 2: "Katllen", 3: "Gabriel"}
        nome_arquivo = f"relatorio_clientes_vendedor_{nomes[escolha]}.xlsx"
        caminho_arquivo = os.path.join(self.pasta_relatorios, nome_arquivo)

        # Mostra barra de progresso
        self.progress.setVisible(True)
        self.progress.setValue(0)

        # Cria thread
        self.thread = WorkerThread(relatorio_cliente_vendedor, escolha)
        self.thread.progress.connect(self.progress.setValue)
        self.thread.finished.connect(lambda msg: self.terminou_relatorio(msg, caminho_arquivo))
        self.thread.start()

    # Finalização do relatório por vendedor
    def terminou_relatorio(self, msg, caminho_arquivo):
        QMessageBox.information(self, "Sucesso", f"Relatório gerado: {caminho_arquivo} ✅")
        self.lista_relatorios.addItem(caminho_arquivo)
        self.combo_vendedor.setVisible(False)
        self.btn_gerar_vendedor.setVisible(False)
        self.progress.setVisible(False)

    # Relatório do dia anterior
    def relatorio_dia(self):
        QMessageBox.information(self, "Processando", "⏳ Processando planilha...")

        self.progress.setVisible(True)
        self.progress.setValue(0)

        # Cria thread
        self.thread = WorkerThread(self.processar_dia)
        self.thread.progress.connect(self.progress.setValue)
        self.thread.finished.connect(lambda msg: self.terminou_dia(msg))
        self.thread.start()

    # Função que processa planilha e envia e-mail
    def processar_dia(self):
        processando_planilha()
        enviar_para_email()

    def terminou_dia(self, msg):
        QMessageBox.information(self, "Sucesso", "Planilha processada e enviada com sucesso! 📧")
        self.lista_relatorios.addItem(os.path.join(self.pasta_relatorios, "Última planilha processada"))
        self.progress.setVisible(False)

# Main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MenuApp()
    window.show()
    sys.exit(app.exec())
