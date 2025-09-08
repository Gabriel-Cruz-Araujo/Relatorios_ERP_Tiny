import sys
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QComboBox, QMessageBox, QListWidget
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QMovie
from dotenv import load_dotenv
from src.relatorios.relatorio_vendedor import relatorio_cliente_vendedor
from src.utils.enviar_email import enviar_para_email
from src.ETL.processamento import processando_planilha

# Caminho base para PyInstaller
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

# Carregar .env
load_dotenv(os.path.join(base_path, ".env"))

# Caminho do GIF
caminho_gif = os.path.join(base_path, "loading.gif")

class WorkerThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, func, *args):
        super().__init__()
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)
        self.finished.emit("Concluído")

class MenuApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📊 Sistema de Relatórios")
        self.setGeometry(600, 300, 500, 450)
        self.setStyleSheet("background-color: #f0f0f0;")
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)

        # Título
        self.title_label = QLabel("📊 MENU PRINCIPAL")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #333;")
        self.layout.addWidget(self.title_label)

        # Botões principais
        button_style = """
            QPushButton {
                background-color: #8d779d; 
                color: white; 
                border-radius: 8px; 
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """

        self.btn_rel_vendedor = QPushButton("Relatório Clientes por Vendedor")
        self.btn_rel_vendedor.setFixedSize(300, 40)
        self.btn_rel_vendedor.setStyleSheet(button_style)
        self.btn_rel_vendedor.clicked.connect(self.mostrar_vendedor_opcoes)
        self.layout.addWidget(self.btn_rel_vendedor, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.btn_rel_dia = QPushButton("Relatório Clientes Trabalhados no Dia Anterior")
        self.btn_rel_dia.setFixedSize(300, 40)
        self.btn_rel_dia.setStyleSheet(button_style)
        self.btn_rel_dia.clicked.connect(self.relatorio_dia)
        self.layout.addWidget(self.btn_rel_dia, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.btn_sair = QPushButton("Sair")
        self.btn_sair.setFixedSize(300, 40)
        self.btn_sair.setStyleSheet(button_style)
        self.btn_sair.clicked.connect(self.close)
        self.layout.addWidget(self.btn_sair, alignment=Qt.AlignmentFlag.AlignHCenter)

        # ComboBox para escolher vendedor (escondido inicialmente)
        self.combo_vendedor = QComboBox()
        self.combo_vendedor.addItems(["Vanessa", "Katllen", "Gabriel"])
        self.combo_vendedor.setFixedSize(200, 35)
        self.combo_vendedor.setVisible(False)
        self.layout.addWidget(self.combo_vendedor, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Botão Gerar Relatório (escondido inicialmente)
        self.btn_gerar_vendedor = QPushButton("Gerar Relatório")
        self.btn_gerar_vendedor.setFixedSize(200, 35)
        self.btn_gerar_vendedor.setStyleSheet(button_style)
        self.btn_gerar_vendedor.clicked.connect(self.iniciar_relatorio_vendedor)
        self.btn_gerar_vendedor.setVisible(False)
        self.layout.addWidget(self.btn_gerar_vendedor, alignment=Qt.AlignmentFlag.AlignHCenter)

        # GIF Ampulheta
        self.loading_label = QLabel()
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setVisible(False)
        self.movie = QMovie(caminho_gif)
        self.movie.setScaledSize(QSize(64, 64))
        self.loading_label.setMovie(self.movie)
        self.layout.addWidget(self.loading_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Lista de relatórios gerados
        self.lista_relatorios = QListWidget()
        self.lista_relatorios.setFixedHeight(100)
        self.layout.addWidget(self.lista_relatorios)

        self.setLayout(self.layout)

        # Pasta para salvar relatórios
        documentos = os.path.expanduser("~/Documents")
        self.pasta_relatorios = os.path.join(documentos, "relatorios")
        os.makedirs(self.pasta_relatorios, exist_ok=True)

    def mostrar_vendedor_opcoes(self):
        self.combo_vendedor.setVisible(True)
        self.btn_gerar_vendedor.setVisible(True)

    def iniciar_relatorio_vendedor(self):
        escolha = self.combo_vendedor.currentIndex() + 1
        nomes = {1: "Vanessa", 2: "Katllen", 3: "Gabriel"}
        nome_arquivo = f"relatorio_clientes_vendedor_{nomes[escolha]}.xlsx"
        caminho_arquivo = os.path.join(self.pasta_relatorios, nome_arquivo)

        self.loading_label.setVisible(True)
        self.movie.start()

        self.thread = WorkerThread(relatorio_cliente_vendedor, escolha)
        self.thread.finished.connect(lambda msg: self.terminou_relatorio(msg, caminho_arquivo))
        self.thread.start()

    def terminou_relatorio(self, msg, caminho_arquivo):
        self.movie.stop()
        self.loading_label.setVisible(False)
        QMessageBox.information(self, "Sucesso", f"Relatório gerado: {caminho_arquivo} ✅")
        self.lista_relatorios.addItem(caminho_arquivo)
        self.combo_vendedor.setVisible(False)
        self.btn_gerar_vendedor.setVisible(False)

    def relatorio_dia(self):
        QMessageBox.information(self, "Processando", "⏳ Processando planilha...")
        self.loading_label.setVisible(True)
        self.movie.start()

        self.thread = WorkerThread(self.processar_dia)
        self.thread.finished.connect(lambda msg: self.terminou_dia(msg))
        self.thread.start()

    def processar_dia(self):
        processando_planilha()
        enviar_para_email()

    def terminou_dia(self, msg):
        self.movie.stop()
        self.loading_label.setVisible(False)
        QMessageBox.information(self, "Sucesso", "Planilha processada e enviada com sucesso! 📧")
        self.lista_relatorios.addItem(os.path.join(self.pasta_relatorios, "Última planilha processada"))
