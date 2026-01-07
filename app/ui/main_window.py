from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLineEdit, QLabel, QListWidget, 
    QFileDialog, QProgressBar, QTextEdit, QSplitter,
    QAbstractItemView, QListWidgetItem, QGridLayout,
    QScrollArea, QFrame, QMessageBox, QDialog, QComboBox,
    QAction, QToolBar, QApplication, QStyleFactory, QSizePolicy
)
from PyQt5.QtCore import Qt, QThreadPool, QSize, QUrl, QSettings
from PyQt5.QtGui import (
    QPixmap, QDragEnterEvent, QDropEvent, QImage, QIcon, 
    QPalette, QColor, QDesktopServices
)
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
import os

from app.core.metadata import MetadataEngine
from app.ui.workers import SearchWorker, DownloadWorker, EmbedWorker, AutoEmbedWorker

class SongDetailsDialog(QDialog):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Song Details")
        self.setFixedSize(500, 300)
        self.layout = QHBoxLayout(self)

        # Get Data
        data = MetadataEngine.get_details(file_path)
        if not data:
            self.layout.addWidget(QLabel("Failed to load metadata."))
            return

        # Left: Image
        self.img_lbl = QLabel()
        self.img_lbl.setFixedSize(250, 250)
        self.img_lbl.setScaledContents(True)
        self.img_lbl.setStyleSheet("border: 1px solid #ccc; background-color: #eee;")
        
        if data.get('artwork'):
            pixmap = QPixmap()
            pixmap.loadFromData(data['artwork'])
            self.img_lbl.setPixmap(pixmap)
        else:
            self.img_lbl.setText("No Artwork")
            self.img_lbl.setAlignment(Qt.AlignCenter)

        # Right: Info
        info_layout = QVBoxLayout()
        info_layout.setAlignment(Qt.AlignTop)
        
        def add_field(label, value):
            lbl = QLabel(f"<b>{label}:</b> {value}")
            lbl.setWordWrap(True)
            info_layout.addWidget(lbl)

        add_field("Title", data['title'])
        add_field("Artist", data['artist'])
        add_field("Album", data['album'])
        add_field("File", os.path.basename(file_path))

        self.layout.addWidget(self.img_lbl)
        self.layout.addLayout(info_layout)


class FileListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.file_set = set()

    def clear(self):
        super().clear()
        self.file_set.clear()

    def takeItem(self, row):
        item = self.item(row)
        if item:
            self.file_set.discard(item.text())
        return super().takeItem(row)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            urls = event.mimeData().urls()
            
            # Optimization: Disable updates while adding many files
            self.setUpdatesEnabled(False)
            try:
                for url in urls:
                    path = str(url.toLocalFile())
                    if os.path.isfile(path):
                        if path.lower().endswith(('.mp3', '.flac', '.m4a', '.mp4', '.aac')):
                            self.add_file(path)
                    elif os.path.isdir(path):
                        self.add_folder(path)
            finally:
                self.setUpdatesEnabled(True)
        else:
            event.ignore()

    def add_file(self, path):
        # O(1) duplicate check
        if path not in self.file_set:
            self.file_set.add(path)
            self.addItem(path)

    def add_folder(self, folder_path):
        # Recursively find files
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('.mp3', '.flac', '.m4a', '.mp4', '.aac')):
                    self.add_file(os.path.join(root, file))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ArtEmbedder")
        self.resize(1100, 750)
        self.setWindowIcon(QIcon("assets/music.png"))
        
        self.settings = QSettings("ArtEmbedder", "AppSettings")
        self.threadpool = QThreadPool()
        print(f"Multithreading with maximum {self.threadpool.maxThreadCount()} threads")
        
        self.current_image_data = None
        self.network_manager = QNetworkAccessManager()
        self.network_manager.finished.connect(self.on_network_image_loaded)

        self.init_toolbar()
        self.init_ui()
        
        # Load theme
        if self.settings.value("dark_mode", False, type=bool):
            self.apply_dark_theme()
            self.dark_mode_action.setChecked(True)
            self.dark_mode_action.setIcon(QIcon("assets/lightmode.png"))
            self.github_action.setIcon(QIcon("assets/github_light.png"))
        else:
            self.dark_mode_action.setIcon(QIcon("assets/darkmode.png"))
            self.github_action.setIcon(QIcon("assets/github.png"))

    def init_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.addToolBar(toolbar)

        # Left Side: App Logo & Title
        title_widget = QWidget()
        title_layout = QHBoxLayout(title_widget)
        title_layout.setContentsMargins(10, 0, 10, 0)
        
        app_logo = QLabel()
        app_logo.setPixmap(QPixmap("assets/music.png").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        app_title = QLabel("ArtEmbedder")
        app_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        title_layout.addWidget(app_logo)
        title_layout.addWidget(app_title)
        toolbar.addWidget(title_widget)

        # Flexbox Spacer (pushes remaining items to the right)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)

        # Right Side: Actions
        # Dark Mode Toggle
        self.dark_mode_action = QAction(QIcon("assets/darkmode.png"), "", self)
        self.dark_mode_action.setToolTip("Toggle Dark/Light Mode")
        self.dark_mode_action.setCheckable(True)
        self.dark_mode_action.toggled.connect(self.toggle_theme)
        toolbar.addAction(self.dark_mode_action)

        # GitHub Button
        self.github_action = QAction(QIcon("assets/github.png"), "GitHub", self)
        self.github_action.setToolTip("Visit Developer's GitHub")
        self.github_action.triggered.connect(self.open_github)
        toolbar.addAction(self.github_action)

    def open_github(self):
        QDesktopServices.openUrl(QUrl("https://github.com/HARAJIT05"))

    def toggle_theme(self, checked):
        if checked:
            self.apply_dark_theme()
            self.settings.setValue("dark_mode", True)
            self.dark_mode_action.setIcon(QIcon("assets/lightmode.png"))
            self.github_action.setIcon(QIcon("assets/github_light.png"))
        else:
            self.apply_light_theme()
            self.settings.setValue("dark_mode", False)
            self.dark_mode_action.setIcon(QIcon("assets/darkmode.png"))
            self.github_action.setIcon(QIcon("assets/github.png"))

    def apply_dark_theme(self):
        app = QApplication.instance()
        app.setStyle(QStyleFactory.create("Fusion"))
        
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        
        app.setPalette(dark_palette)
        app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
        
        # Specific fixes
        self.file_list.setStyleSheet("QListWidget { color: white; background-color: #2b2b2b; }")
        self.results_area.setStyleSheet("QListWidget { color: white; background-color: #2b2b2b; }")

    def apply_light_theme(self):
        app = QApplication.instance()
        app.setStyle(QStyleFactory.create("Fusion"))
        app.setPalette(QPalette()) # Default
        app.setStyleSheet("")
        
        self.file_list.setStyleSheet("")
        self.results_area.setStyleSheet("")

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # LEFT PANEL: File Selection
        left_layout = QVBoxLayout()
        
        lbl_files = QLabel("<b>1. Input Files / Folder</b>")
        self.file_list = FileListWidget()
        self.file_list.itemSelectionChanged.connect(self.on_file_selection_changed)
        self.file_list.itemDoubleClicked.connect(self.open_song_details)
        
        # File Action Buttons
        btn_layout_top = QHBoxLayout()
        btn_open_folder = QPushButton("Open Folder")
        btn_open_folder.clicked.connect(self.open_folder_dialog)
        btn_layout_top.addWidget(btn_open_folder)

        btn_layout_btm = QHBoxLayout()
        btn_select_all = QPushButton("Select All")
        btn_select_all.clicked.connect(self.file_list.selectAll)
        btn_clear = QPushButton("Clear List")
        btn_clear.clicked.connect(self.file_list.clear)
        btn_remove = QPushButton("Remove Selected")
        btn_remove.clicked.connect(self.remove_selected_files)
        
        btn_layout_btm.addWidget(btn_select_all)
        btn_layout_btm.addWidget(btn_clear)
        btn_layout_btm.addWidget(btn_remove)

        # Auto Process Button
        self.btn_auto_process = QPushButton("⚡ Auto-Match & Embed All")
        self.btn_auto_process.setToolTip("Automatically finds and embeds artwork for all listed files based on their metadata.")
        self.btn_auto_process.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 10px;")
        self.btn_auto_process.clicked.connect(self.start_auto_process)

        left_layout.addWidget(lbl_files)
        left_layout.addLayout(btn_layout_top)
        left_layout.addWidget(self.file_list)
        left_layout.addLayout(btn_layout_btm)
        left_layout.addSpacing(10)
        left_layout.addWidget(self.btn_auto_process)

        # MIDDLE PANEL: Search & Results
        mid_layout = QVBoxLayout()
        
        lbl_search = QLabel("<b>2. Artwork Search</b>")
        
        # Source Selection
        self.source_combo = QComboBox()
        self.source_combo.addItems(["iTunes", "MusicBrainz"])
        self.source_combo.setToolTip("Select the artwork provider")

        search_input_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Artist - Album")
        self.search_bar.returnPressed.connect(self.start_search)
        btn_search = QPushButton("Search")
        btn_search.clicked.connect(self.start_search)
        search_input_layout.addWidget(self.search_bar)
        search_input_layout.addWidget(btn_search)

        self.results_area = QListWidget()
        self.results_area.setIconSize(QSize(100, 100))
        self.results_area.itemClicked.connect(self.on_result_clicked)

        mid_layout.addWidget(lbl_search)
        mid_layout.addWidget(QLabel("Source:"))
        mid_layout.addWidget(self.source_combo)
        mid_layout.addLayout(search_input_layout)
        mid_layout.addWidget(self.results_area)

        # RIGHT PANEL: Preview & Action
        right_layout = QVBoxLayout()
        
        lbl_preview = QLabel("<b>3. Preview & Embed</b>")
        self.preview_lbl = QLabel("No Image Selected")
        self.preview_lbl.setAlignment(Qt.AlignCenter)
        self.preview_lbl.setMinimumSize(250, 250)
        self.preview_lbl.setStyleSheet("border: 2px dashed #aaa;")
        self.preview_lbl.setScaledContents(True)

        self.embed_info_lbl = QLabel("") # Details about the image source
        self.embed_info_lbl.setWordWrap(True)

        self.embed_btn = QPushButton("Embed Selected Image")
        self.embed_btn.setFixedHeight(40)
        self.embed_btn.setEnabled(False)
        self.embed_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        self.embed_btn.clicked.connect(self.start_embedding)

        self.progress_bar = QProgressBar()
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMaximumHeight(150)

        right_layout.addWidget(lbl_preview)
        right_layout.addWidget(self.embed_info_lbl)
        right_layout.addWidget(self.embed_btn)
        right_layout.addSpacing(20)
        right_layout.addWidget(QLabel("<b>Log / Progress</b>"))
        right_layout.addWidget(self.progress_bar)
        right_layout.addWidget(self.log_output)

        # Combine Layouts via Splitter
        splitter = QSplitter(Qt.Horizontal)
        
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        
        mid_widget = QWidget()
        mid_widget.setLayout(mid_layout)
        
        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        splitter.addWidget(left_widget)
        splitter.addWidget(mid_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 3)
        splitter.setStretchFactor(2, 2)

        main_layout.addWidget(splitter)

    def on_file_selection_changed(self):
        items = self.file_list.selectedItems()
        if len(items) == 1:
            file_path = items[0].text()
            # Run metadata fetch in background if needed, but for now blocking is okay for single file metadata read
            details = MetadataEngine.get_details(file_path)
            if details and details.get('artwork'):
                pixmap = QPixmap()
                pixmap.loadFromData(details['artwork'])
                self.preview_lbl.setPixmap(pixmap)
                self.embed_info_lbl.setText(f"Current Artwork: {details['title']} ({len(details['artwork'])/1024:.1f} KB)")
            else:
                self.preview_lbl.clear()
                self.preview_lbl.setText("No Embedded Artwork")
                self.embed_info_lbl.setText("Selected file has no artwork.")
            
            if not self.current_image_data:
                self.embed_btn.setEnabled(False)
        else:
            if not self.current_image_data:
                self.preview_lbl.clear()
                self.preview_lbl.setText(f"{len(items)} Files Selected")
                self.embed_info_lbl.setText("")

    def open_song_details(self, item):
        file_path = item.text()
        dialog = SongDetailsDialog(file_path, self)
        dialog.exec_()

    def open_folder_dialog(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Music Directory")
        if folder:
            self.file_list.setUpdatesEnabled(False)
            try:
                self.file_list.add_folder(folder)
            finally:
                self.file_list.setUpdatesEnabled(True)
            self.log(f"Added folder: {folder}")

    def remove_selected_files(self):
        for item in self.file_list.selectedItems():
            self.file_list.takeItem(self.file_list.row(item))

    def log(self, message):
        self.log_output.append(message)
        # Scroll to bottom
        sb = self.log_output.verticalScrollBar()
        sb.setValue(sb.maximum())

    # --- Search Logic ---
    def start_search(self):
        term = self.search_bar.text().strip()
        if not term:
            return
        
        source = self.source_combo.currentText()
        self.results_area.clear()
        self.log(f"Searching ({source}) for: {term}...")
        
        worker = SearchWorker(term, source=source)
        worker.signals.result.connect(self.display_search_results)
        worker.signals.error.connect(self.on_worker_error)
        self.threadpool.start(worker)

    def display_search_results(self, results):
        self.results_area.clear()
        if not results:
            self.log("No results found.")
            return

        for item in results:
            display_text = f"{item['artist']} - {item['album']} ({item['year']})"
            list_item = QListWidgetItem(display_text)
            list_item.setData(Qt.UserRole, item['artwork_url'])
            self.results_area.addItem(list_item)
            
            # Optionally trigger thumbnail download here
            self.load_thumbnail(list_item, item['thumbnail_url'])
            
        self.log(f"Found {len(results)} results.")

    def load_thumbnail(self, item, url):
        req = QNetworkRequest(QUrl(url))
        req.setRawHeader(b"User-Agent", b"ArtEmbedder/1.0")
        reply = self.network_manager.get(req)
        reply.setProperty("list_item", item)

    def on_network_image_loaded(self, reply):
        item = reply.property("list_item")
        if not reply.error():
            data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            if item:
                # We need QIcon import in main_window which we added
                item.setIcon(QIcon(pixmap))
        reply.deleteLater()
        
    def on_result_clicked(self, item):
        high_res_url = item.data(Qt.UserRole)
        self.log("Downloading high-res image...")
        
        worker = DownloadWorker(high_res_url)
        worker.signals.result.connect(self.set_preview_image)
        worker.signals.error.connect(self.on_worker_error)
        self.threadpool.start(worker)

    def set_preview_image(self, data):
        self.current_image_data = data
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.preview_lbl.setPixmap(pixmap)
        self.preview_lbl.setStyleSheet("border: none;")
        self.embed_info_lbl.setText(f"New Image Size: {len(data)/1024:.1f} KB")
        self.embed_btn.setEnabled(True)
        self.log(f"Image loaded. Size: {len(data)} bytes.")

    # --- Embedding Logic ---
    def start_embedding(self):
        files = [self.file_list.item(i).text() for i in range(self.file_list.count())]
        
        if not files:
            QMessageBox.warning(self, "No Files", "Please add music files to the list.")
            return
        
        # If user selected specific files in the list, only embed to those?
        # Current logic (from prev turn) embeds to ALL files in the list.
        # But if user made a selection, maybe they only want those?
        # Let's support selected-only if selection exists.
        selected_items = self.file_list.selectedItems()
        if selected_items:
            files = [item.text() for item in selected_items]
            self.log(f"Embedding into {len(files)} selected files...")
        
        if not self.current_image_data:
            QMessageBox.warning(self, "No Image", "Please select an image first.")
            return

        self.embed_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        
        worker = EmbedWorker(files, self.current_image_data)
        worker.signals.progress.connect(self.update_progress)
        worker.signals.log.connect(self.log)
        worker.signals.result.connect(self.on_embed_finished)
        worker.signals.error.connect(self.on_worker_error)
        
        self.threadpool.start(worker)

    def update_progress(self, val):
        self.progress_bar.setValue(val)

    def on_embed_finished(self, msg):
        self.log(msg)
        self.embed_btn.setEnabled(True)
        QMessageBox.information(self, "Done", msg)

    def on_worker_error(self, err_tuple):
        exctype, value, tb_str = err_tuple
        self.log(f"Error: {value}")
        print(tb_str)
        self.embed_btn.setEnabled(True)

    # --- Auto Process Logic ---
    def start_auto_process(self):
        count = self.file_list.count()
        if count == 0:
            QMessageBox.warning(self, "No Files", "Please add files or a folder first.")
            return

        source = self.source_combo.currentText()
        confirm = QMessageBox.question(
            self, "Start Auto-Batch?",
            f"This will search {source} and OVERWRITE artwork for {count} files.\n"
            "Are you sure you want to proceed?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return

        files = [self.file_list.item(i).text() for i in range(count)]
        
        self.btn_auto_process.setEnabled(False)
        self.embed_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.log(f"Starting batch processing using {source}...")
        
        worker = AutoEmbedWorker(files, source=source)
        worker.signals.log.connect(self.log)
        worker.signals.progress.connect(self.update_progress)
        worker.signals.result.connect(self.on_auto_process_finished)
        worker.signals.finished.connect(self.on_worker_finished)
        
        self.threadpool.start(worker)

    def on_auto_process_finished(self, msg):
        QMessageBox.information(self, "Batch Complete", msg)

    def on_worker_finished(self):
        self.btn_auto_process.setEnabled(True)
        if self.current_image_data:
            self.embed_btn.setEnabled(True)