DARK_QSS = """
QWidget {
    background-color: #22252A;
    color: #ECECEC;
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 14px;
}
QLabel {
    color: #B8C0D4;
    font-size: 14px;
}
QLineEdit, QComboBox {
    background-color: #282C34;
    color: #ECECEC;
    border: 1px solid #393E46;
    border-radius: 8px;
    padding: 8px 14px;
    min-width: 160px;
    min-height: 30px;
}
QTextEdit {
    background-color: #282C34;
    color: #ECECEC;
    border: 1px solid #393E46;
    border-radius: 8px;
    padding: 8px;
}
QTreeWidget, QListWidget {
    background-color: #272930;
    color: #ECECEC;
    border: 1.5px solid #393E46;
    border-radius: 12px;
    font-size: 15px;
}
QListWidget {
    padding: 10px 0px 10px 12px;
    min-width: 155px;
    min-height: 250px;
}
QListWidget::item {
    margin-bottom: 6px;
    padding: 8px 0px 8px 8px;
    border-radius: 8px;
}
QListWidget::item:selected {
    background: #384264;
    color: #FFF;
}
QSplitter::handle {
    background: #22252A;
}
QPushButton {
    background-color: #31343B;
    color: #6EF1B4;
    border: none;
    border-radius: 10px;
    padding: 9px 24px;
    font-weight: 600;
    font-size: 15px;
    margin-right: 8px;
}
QPushButton:hover {
    background-color: #425060;
    color: #ECECEC;
}
QTextEdit[readOnly="true"] {
    background: #24272F;
    color: #B9D4F7;
    border: 1px solid #393E46;
}
QGroupBox {
    border: 1.5px solid #393E46;
    border-radius: 16px;
    margin-top: 9px;
}
"""
