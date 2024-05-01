import subprocess
from PySide6.QtCore import QUrl, Slot
from PySide6.QtWidgets import (QApplication, QLineEdit, QMainWindow, QPushButton, QToolBar, QCheckBox, QButtonGroup, QMessageBox)
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
import sys

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

        self.pag_nav = QWebEngineView()
        self.setCentralWidget(self.pag_nav)
        url_inicial = "http://youtube.com"
        self.campo_url.setText(url_inicial)
        self.pag_nav.load(QUrl(url_inicial))
        self.pag_nav.page().titleChanged.connect(self.setWindowTitle)
        self.pag_nav.page().urlChanged.connect(self.mudanca_url)

        self.baixado_msg = QMessageBox()
        self.baixado_msg.setText("Download terminado!")


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
        resultado = subprocess.run([".\\yt-dlp\\yt-dlp.exe", "-P", ".\\videos\\", "-f", formato, url_txt], capture_output=True, text=True)
        self.baixado_msg.exec()



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
