# Ventana principal de la app
import cv2
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QComboBox, QTableWidget, QTableWidgetItem, QAbstractItemView, QSizePolicy, QHeaderView
)
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QIcon, QPixmap, QImage, QColor, QBrush
from src.gui.style import dark_theme
from src.camera.camera_handler import CameraHandler

import pandas as pd
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt




class MonitorGrimaceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.last_frame = None
        self.setWindowTitle("Monitor de Observación Grimace")
        self.setWindowIcon(QIcon("resources/logo.jpeg"))
        self.setGeometry(100, 100, 1280, 800)
        self.setStyleSheet(dark_theme())

        self.setup_ui()
        self.setup_timers()




        self.camera_handler = None
        self.frame_timer = QTimer()
        self.frame_timer.timeout.connect(self.update_frame)
        self.connect_button.clicked.connect(self.toggle_camera)
  
    def setup_ui(self):
        main_layout = QVBoxLayout()

        header = QLabel("🔬 Monitor de Observación Grimace - Sistema de Monitoreo de Dolor")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 20px; font-weight: bold; color: #008971; padding: 10px;")
        main_layout.addWidget(header)

        camera_controls = QHBoxLayout()
        self.camera_selector = QComboBox()
        self.camera_selector.addItems(["Cámara 0", "Cámara 1", "Cámara Virtual"])

        self.connect_button = QPushButton("🔌 CONECTAR")
        self.camera_status = QLabel("● DESCONECTADO")
        self.set_camera_status("Desconectado")

        camera_controls.addWidget(self.camera_selector)
        camera_controls.addWidget(self.connect_button)
        camera_controls.addWidget(self.camera_status)
        main_layout.addLayout(camera_controls)

        self.camera_display = QLabel("📷 Conectar cámara")
        self.camera_display.setMinimumHeight(400)
        self.camera_display.setAlignment(Qt.AlignCenter)
        self.camera_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.camera_display.setScaledContents(True)
        self.camera_display.setStyleSheet("border: 2px dashed #444; color: #777; font-size: 26px; font-weight: bold;background-color: black;")
        main_layout.addWidget(self.camera_display, stretch=5)


        # Cronómetros
        time_layout = QHBoxLayout()
        self.experiment_timer_label = QLabel("🧪 Tiempo Experimento: 00:00:00")
        self.experiment_timer_label.setStyleSheet("""color: #dddddd; font-size: 18px;font-weight: bold;""")

        self.pain_timer_label = QLabel("😖 Tiempo Episodio Dolor: 00:00:00")
        self.pain_timer_label.setStyleSheet("""color: #ffaa00; font-size: 18px; font-weight: bold; """)
        
        time_layout.addWidget(self.experiment_timer_label)
        time_layout.addWidget(self.pain_timer_label)
        main_layout.addLayout(time_layout)

        control_layout = QHBoxLayout()
        self.experiment_button = QPushButton("▶ INICIAR EXPERIMENTO")
        self.experiment_button.clicked.connect(self.toggle_experiment)

        self.stop_button = QPushButton("")
        control_layout.addWidget(self.stop_button)

        self.pain_button = QPushButton("⚠ EPISODIO DE DOLOR")
        self.pain_button.clicked.connect(self.toggle_pain_episode)

        self.export_button = QPushButton("💾 EXPORTAR DATOS")
        self.export_button.clicked.connect(self.export_table_to_excel)
        self.stop_button.clicked.connect(lambda: (self.finalize_experiment(), self.export_table_to_excel()))


        control_layout.addWidget(self.experiment_button)
        control_layout.addWidget(self.pain_button)
        control_layout.addWidget(self.export_button)
        main_layout.addLayout(control_layout)

        self.table = QTableWidget(0, 5)
        self.table.setShowGrid(True)
        self.table.setGridStyle(Qt.SolidLine)

        self.table.setHorizontalHeaderLabels(["#Ep", "Tiempo", "Duración", "Estado", "Acción"])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
        main_layout.addWidget(self.table)

        footer = QLabel("Dev David Monsalve | amrentamos@gmail.com | +584263331723")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("font-size: 16px; color: gray; padding: 10px; font-weight: italic;")
        main_layout.addWidget(footer)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def setup_timers(self):
        self.experiment_timer = QTimer()
        self.experiment_time = QTime(0, 0, 0)
        self.experiment_timer.timeout.connect(self.update_experiment_time)

        self.pain_timer = QTimer()
        self.pain_time = QTime(0, 0, 0)
        self.pain_timer.timeout.connect(self.update_pain_time)

    def set_camera_status(self, status):
        colors = {
            "DESCONECTADO": "#FF5555",
            "CONECTANDO": "#FFD700",
            "CONECTADO": "#55FF55"
        }
        self.camera_status.setText(f"● {status}")
        self.camera_status.setStyleSheet(f"color: {colors.get(status, 'white')}; font-weight: bold;")

    def toggle_experiment(self):
        if self.experiment_timer.isActive():
            self.experiment_timer.stop()
            self.experiment_button.setText("▶ INICIAR EXPERIMENTO")
        else:
            self.experiment_time = QTime(0, 0, 0)
            self.experiment_timer.start(1000)
            self.experiment_button.setText("⏹ DETENER EXPERIMENTO")

    def toggle_pain_episode(self):
        if self.pain_timer.isActive():
            # Finalizar episodio
            duration = self.pain_time.toString("hh:mm:ss")
            self.complete_episode(duration)
            self.pain_timer.stop()
            self.pain_button.setText("⚠ EPISODIO DE DOLOR")
        else:
            # Iniciar episodio
            timestamp = self.experiment_time.toString("hh:mm:ss")
            self.start_episode(timestamp)
            self.pain_time = QTime(0, 0, 0)
            self.pain_timer.start(1000)
            self.pain_button.setText("🛑 FIN DEL EPISODIO")


    def update_experiment_time(self):
        self.experiment_time = self.experiment_time.addSecs(1)
        self.experiment_timer_label.setText(f"🧪 TIEMPO EXPERIMENTO: {self.experiment_time.toString('hh:mm:ss')}")

    def update_pain_time(self):
        self.pain_time = self.pain_time.addSecs(1)
        self.pain_timer_label.setText(f"😖 TIEMPO EPISODIO DOLOR: {self.pain_time.toString('hh:mm:ss')}")

    def _create_table_item(self, text, is_header=False):
        item = QTableWidgetItem(text)
        item.setForeground(QBrush(QColor("#dddddd")))
        return item

    def _style_row(self, row):
        # Set text color for all items
        for col in range(self.table.columnCount()):
            item = self.table.item(row, col)
            if item:
                item.setForeground(QBrush(QColor("#dddddd")))
        
        # Style status item
        state_item = self.table.item(row, 3)
        if state_item:
            if state_item.text() == "COMPLETADO":
                state_item.setBackground(QBrush(QColor(46, 139, 87)))  # Verde
            elif state_item.text() == "EN CURSO":
                state_item.setBackground(QBrush(QColor(218, 165, 32)))  # Amarillo

    def delete_row(self, row_to_delete):
        self.table.removeRow(row_to_delete)
        # Renumerar y re-estilizar las filas restantes
        for i in range(self.table.rowCount()):
            self.table.item(i, 0).setText(str(i + 1))
            self._style_row(i)

    def start_episode(self, timestamp_str):
        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, self._create_table_item(str(row + 1)))
        self.table.setItem(row, 1, self._create_table_item(timestamp_str))
        self.table.setItem(row, 2, self._create_table_item("—"))
        
        state_item = self._create_table_item("EN CURSO")
        self.table.setItem(row, 3, state_item)
        
        self.table.setCellWidget(row, 4, self.create_delete_button(row))
        
        self._style_row(row)
        self.table.scrollToBottom()

    def complete_episode(self, duration_str):
        row = self.table.rowCount() - 1
        if row >= 0:
            self.table.setItem(row, 2, self._create_table_item(duration_str))
            self.table.setItem(row, 3, self._create_table_item("COMPLETADO"))
            self._style_row(row)

    def create_delete_button(self, row):
        button = QPushButton("🗑️")
        button.setCursor(Qt.PointingHandCursor)
        button.setStyleSheet("""
            QPushButton {
                border: 2px solid red;
                border-radius: 6px;
                color: red;
                background-color: transparent;
                font-size: 14px;
                padding: 2px 6px;
            }
            QPushButton:hover {
                background-color: red;
                color: white;
            }
        """)
        button.clicked.connect(lambda _, r=row: self.delete_row(r))
        return button



    def toggle_camera(self):
        if self.camera_handler and self.camera_handler.connected:
            self.disconnect_camera()
        else:
            self.connect_camera()

    def connect_camera(self):
        self.set_camera_status("Conectando")
        index = self.camera_selector.currentIndex()
        self.camera_handler = CameraHandler(index)
        self.camera_display.setText("")  # Limpia el texto cuando inicia la cámara
        if self.camera_handler.connect():
            self.set_camera_status("CONECTADO")
            self.connect_button.setText("🔌 DESCONECTAR")
            self.frame_timer.start(30)  # ~30 FPS
        else:
            self.set_camera_status("DESCONECTADO")
            self.camera_handler = None

    def disconnect_camera(self):
        self.frame_timer.stop()
        if self.camera_handler:
            self.camera_handler.release()
            self.camera_handler = None
        self.camera_display.setText("📷 Conectar cámara")
        self.camera_display.setPixmap(QPixmap())
        self.connect_button.setText("🔌 CONECTAR")
        self.set_camera_status("DESCONECTADO")

    def update_frame(self):
        if self.camera_handler:
            frame = self.camera_handler.read_frame()
            if frame is not None:
                self.last_frame = frame  # Guarda el último frame
                self.display_frame(frame)

      
    def display_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.camera_display.setPixmap(QPixmap.fromImage(qt_image))

    def export_table_to_excel(self):
        rows = self.table.rowCount()
        if rows == 0:
            QMessageBox.warning(self, "Advertencia", "No hay datos para exportar.")
            return

        data = []
        for i in range(rows):
            episodio = self.table.item(i, 0).text()
            tiempo = self.table.item(i, 1).text()
            duracion = self.table.item(i, 2).text()
            estado = self.table.item(i, 3).text()
            data.append([episodio, tiempo, duracion, estado])

        df = pd.DataFrame(data, columns=["Episodio", "Inicio", "Duración", "Estado"])

        # Diálogo para guardar
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar archivo",
            "episodios_dolor.xlsx",
            "Archivos de Excel (*.xlsx)"
        )

        if filepath:
            df.to_excel(filepath, index=False)
            QMessageBox.information(self, "Éxito", "Datos exportados correctamente.")
            self.show_analysis(df)

    def parse_duration(self, dur_str):
        try:
            t = datetime.strptime(dur_str, "%H:%M:%S")
            return timedelta(hours=t.hour, minutes=t.minute, seconds=t.second).total_seconds()
        except:
            return 0


    def show_analysis(self, df):
        # Conversión a tiempos
        df["Inicio_dt"] = pd.to_datetime(df["Inicio"], format="%H:%M:%S")
        df["Duración_seg"] = df["Duración"].apply(self.parse_duration)

        # 1. Estadística descriptiva
        promedio = df["Duración_seg"].mean()
        frecuencia = len(df)

        # 2. Intervalos entre episodios
        df = df.sort_values("Inicio_dt")
        df["Intervalo"] = df["Inicio_dt"].diff().dt.total_seconds()

        # Ventana de análisis
        analysis_window = QWidget()
        analysis_window.setWindowTitle("Análisis de los episodios")
        layout = QVBoxLayout(analysis_window)

        stats_text = f"""
        <b>Cantidad de episodios:</b> {frecuencia}<br>
        <b>Duración promedio:</b> {round(promedio, 2)} segundos<br>
        <b>Intervalo promedio entre episodios:</b> {round(df['Intervalo'].mean(), 2)} segundos
        """
        label = QLabel(stats_text)
        label.setWordWrap(True)
        layout.addWidget(label)

        # 3. Gráfica de duración en línea de tiempo
        fig1, ax1 = plt.subplots()
        ax1.plot(df["Inicio_dt"], df["Duración_seg"], marker="o", label="Duración")
        ax1.set_title("Evolución de la duración de episodios")
        ax1.set_xlabel("Hora de inicio")
        ax1.set_ylabel("Duración (s)")
        ax1.grid(True)

        # 4. Gráfica de separación
        fig2, ax2 = plt.subplots()
        ax2.bar(range(1, len(df)), df["Intervalo"].iloc[1:], color="orange")
        ax2.set_title("Separación entre episodios")
        ax2.set_xlabel("Episodio #")
        ax2.set_ylabel("Intervalo (s)")
        ax2.grid(True)

        # Mostrar gráficas en Qt (convertimos con canvas)
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
        canvas1 = FigureCanvas(fig1)
        canvas2 = FigureCanvas(fig2)
        layout.addWidget(canvas1)
        layout.addWidget(canvas2)

        analysis_window.setLayout(layout)
        analysis_window.resize(800, 600)
        analysis_window.show()
        self.analysis_window = analysis_window  # mantener referencia


