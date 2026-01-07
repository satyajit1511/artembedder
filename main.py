import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from app.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Use absolute path for icon to ensure Linux taskbar compatibility
    import os
    basedir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(basedir, "assets", "music.png")
    app.setWindowIcon(QIcon(icon_path))
    
    # Optional: Apply a dark theme or style
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
