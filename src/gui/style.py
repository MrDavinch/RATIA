# Estilos CSS centralizados

def dark_theme():
    return """
    * {
        font-family: 'Segoe UI';
    }
    QMainWindow {
        background-color: #121212;
    }
    QPushButton {
        background-color: #008971;
        border: none;
        padding: 10px;
        font-weight: bold;
        color: #000;
        border-radius: 6px;
    }
    QPushButton:hover {
        background-color: #00FFAA;
    }
    QComboBox {
        background-color: #1e1e1e;
        color: #ccc;
        padding: 5px;
        border: 1px solid #555;
        border-radius: 4px;
    }
    QLabel {
        color: #ccc;
    }

    QTableWidget {
        background-color: #1e1e1e;  /* Fondo oscuro */
        color: white;
        gridline-color: #3a3a3a;
        font-size: 14px;
    }
    QHeaderView::section {
        background-color: #2c2c2c;
        color: #00ffaa;
        font-weight: bold;
        padding: 5px;
        border: 1px solid #3a3a3a;
    }
    QTableWidget::item {
        border: 1px solid #3a3a3a;
        padding: 5px;
    }

    """
