'''
This is the main entry point for the application. It initializes the necessary components and starts the main loop.
It shall follow the implementation_plan.md and the design document. It is responsible for setting up the application environment,
loading configurations, and managing the overall flow of the program.

'''

import sys
from importlib import import_module
from pathlib import Path

from PyQt5 import QtWidgets, QtGui, QtCore

# Modificação para refletir a nova estrutura modular do projeto, mantendo a compatibilidade com o restante do código.
from src import ui
from src.ui import Ui_MainWindow


class EspToolMainWindow(QtWidgets.QMainWindow):
    """
    Main application window for ESP32-Tool.
    Implements default Qt event handling with useful behavior.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ESP32-Tool")
        self.setToolTip("ESP32 Tool Main Window")

    def closeEvent(self, event):
        event.accept()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)

    def showEvent(self, event):
        super().showEvent(event)


def main():
    """
    Ponto de entrada da aplicação ESP32-Tool.
    Inicializa o QApplication, aplica o tema escuro e carrega a interface modular.
    """
    app = QtWidgets.QApplication(sys.argv)
    
    # Define o estilo base como Fusion para melhor compatibilidade de temas em diferentes SOs
    app.setStyle("Fusion")

    # Configuração da Paleta de Cores (Dark Theme - Nord inspired)
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor("#2E3440"))
    palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor("#D8DEE9"))
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor("#3B4252"))
    palette.setColor(QtGui.QPalette.Text, QtGui.QColor("#ECEFF4"))
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor("#4C566A"))
    palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor("#ECEFF4"))
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor("#81A1C1"))
    palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor("#2E3440"))
    app.setPalette(palette)

    # Inicialização da Janela Principal
    MainWindow = QtWidgets.QMainWindow()
    
    # Instancia e configura a interface a partir do módulo ui.py
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    # Exibe a janela e executa o loop da aplicação
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()