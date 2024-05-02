import subprocess
from PySide6.QtCore import QUrl, Slot, QObject, Signal
from PySide6.QtWidgets import (QApplication, QLineEdit, QMainWindow, QPushButton, QToolBar, QCheckBox, QButtonGroup, QMessageBox, QFileDialog, QProgressBar)
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
import sys
import threading

class GerenciadorDeMensagens(QObject):
    sucesso_msg = Signal()
    erro_msg = Signal()

class JanelaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Youtube Video Downloader")

        self.barra_de_tarefas = QToolBar()
        self.addToolBar(self.barra_de_tarefas)

        self.btn_voltar = QPushButton(text="<")
        self.btn_voltar.clicked.connect(self.pag_ant)
        self.barra_de_tarefas.addWidget(self.btn_voltar)

        self.btn_avancar= QPushButton(text=">")
        self.btn_avancar.clicked.connect(self.pag_prox)
        self.barra_de_tarefas.addWidget(self.btn_avancar)

        self.campo_url = QLineEdit()
        self.campo_url.returnPressed.connect(self.carregar_pag)
        self.barra_de_tarefas.addWidget(self.campo_url)

        self.btn_ir = QPushButton(text="Ir")
        self.btn_ir.clicked.connect(self.carregar_pag)
        self.barra_de_tarefas.addWidget(self.btn_ir)

        self.btn_baixar = QPushButton(text="Baixar")
        self.btn_baixar.clicked.connect(self.baixar_video)
        self.barra_de_tarefas.addWidget(self.btn_baixar)

        self.radio_mp4 = QCheckBox(text="MP4")
        self.radio_mp4.setChecked(True)
        self.radio_mp3 = QCheckBox(text="M4A")
        
        self.baixar_opts = QButtonGroup()
        
        self.baixar_opts.addButton(self.radio_mp4)
        self.baixar_opts.addButton(self.radio_mp3)

        self.barra_de_tarefas.addWidget(self.radio_mp4)
        self.barra_de_tarefas.addWidget(self.radio_mp3)

        self.gerenciador_msg = GerenciadorDeMensagens()
        self.gerenciador_msg.sucesso_msg.connect(self.mostra_msg_sucesso)
        self.gerenciador_msg.erro_msg.connect(self.mostra_msg_erro)

        self.pag_nav = QWebEngineView()
        self.setCentralWidget(self.pag_nav)
        url_inicial = "http://youtube.com"
        self.campo_url.setText(url_inicial)
        self.pag_nav.load(QUrl(url_inicial))
        self.pag_nav.page().titleChanged.connect(self.setWindowTitle)
        self.pag_nav.page().urlChanged.connect(self.mudanca_url)


    Slot()
    def carregar_pag(self):
        url_txt = self.campo_url.text()
        if not url_txt.startswith("http"):
            url_txt = "http://" + url
        url = QUrl.fromUserInput(url_txt)
        if url.isValid():
            self.pag_nav.load(url)

    Slot()
    def pag_ant(self):
        self.pag_nav.page().triggerAction(QWebEnginePage.Back)

    Slot()
    def pag_prox(self):
        self.pag_nav.page().triggerAction(QWebEnginePage.Forward)
    
    Slot(QUrl)
    def mudanca_url(self, url):
        self.campo_url.setText(url.toString())

    Slot()
    def baixar_video(self):
        url_txt = self.campo_url.text()
        formato = "m4a" if self.radio_mp3.isChecked() else "mp4"
        if not url_txt.startswith("http"):
            url_txt = "http://" + url_txt
        caminho_download = QFileDialog.getExistingDirectory(self, "Selecione a pasta onde o video deverá ser baixado")
        if caminho_download:
            comandos = [".\\yt-dlp\\yt-dlp.exe", "-P", caminho_download, "-f", formato, url_txt]
            threading.Thread(target=self.executar_processo_dowload, args=[comandos]).start()

    def executar_processo_dowload(self, comandos):
        resultado = subprocess.run(comandos, capture_output=True, text=True)
        if resultado.returncode == 0:
            self.gerenciador_msg.sucesso_msg.emit()
        else:
            self.gerenciador_msg.erro_msg.emit()

    
    Slot()
    def mostra_msg_sucesso(self):
        QMessageBox.information(self, "Download concluído", "O video foi baixado com sucesso!")

    Slot()
    def mostra_msg_erro(self):
        QMessageBox.information(self, "Falha no download", "Ocorreu um erro ao tentar baixar o video.")
    



if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela_principal = JanelaPrincipal()
    espaco_disp = janela_principal.screen().availableGeometry()
    janela_principal.resize(espaco_disp.width() * 2 / 3, espaco_disp.height() * 2 / 3)
    janela_principal.show()
    sys.exit(app.exec())
# Run a simple shell command
# result = subprocess.run([".\\yt-dlp\\yt-dlp.exe", "-P", ".\\videos\\", "https://www.youtube.com/watch?v=LMD6MqwErzc"], capture_output=True, text=True)

# Print the output
#print(result.stdout)
