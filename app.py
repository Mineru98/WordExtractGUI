import sys
import requests
import platform
from PyInstaller.utils.hooks import collect_data_files
from bs4 import BeautifulSoup
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtGui import QGuiApplication, QIcon, QAction
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QHBoxLayout, QVBoxLayout, QMessageBox, QLineEdit, QMainWindow

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_btn = None
        self.load_input = None
        self.url = ""
        self.count = None
        self.noun_list = []
        self.load_lbl = None
        self.load_input_send_btn = None
        self.extract_excel_btn = None
        self.extract_image_btn = None
        self.central_widget = None
        self.last_mode = "file"
        self.setAcceptDrops(True)

        exitAction = QAction(QIcon(), '종료', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('프로그램 종료')
        exitAction.triggered.connect(QCoreApplication.instance().quit)
        
        loadAction = QAction(QIcon(), '파일 업로드', self)
        loadAction.setShortcut('Ctrl+O')
        loadAction.setStatusTip('파일 업로드')
        loadAction.triggered.connect(self.btn_fun_file_load)

        fileLoadModeAction = QAction(QIcon(), '파일 업로드 모드', self)
        fileLoadModeAction.setShortcut('Ctrl+F')
        fileLoadModeAction.setStatusTip('파일 업로드 모드')
        fileLoadModeAction.triggered.connect(self.change_file_mode)

        urlLoadModeAction = QAction(QIcon(), 'URL 업로드 모드', self)
        urlLoadModeAction.setShortcut('Ctrl+U')
        urlLoadModeAction.setStatusTip('URL 업로드 모드')
        urlLoadModeAction.triggered.connect(self.change_url_mode)

        self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(True)
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(loadAction)
        file_menu.addAction(exitAction)
        mode_menu = menubar.addMenu('&Mode')
        mode_menu.addAction(fileLoadModeAction)
        mode_menu.addAction(urlLoadModeAction)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('단어 빈도수 추출기')
        self.setFixedWidth(720)
        self.setFixedHeight(240)
        self.center()
        self.setup_ui()

    def center(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setup_ui(self):
        self.central_widget = QWidget()

        self.load_btn = QPushButton("문서를 드래그 하거나 클릭하여 이곳에 넣어주세요.")
        self.load_btn.clicked.connect(self.btn_fun_file_load)
        self.load_btn.setStyleSheet("color: #000;"
                                    "background-color: #fff;"
                                    "width: 580px;"
                                    "height: 120px;"
                                    "border-style: dashed;"
                                    "border-width: 2px;"
                                    "border-color: gray;")

        self.load_input = QLineEdit(self)
        self.load_input.setFixedWidth(560)
        self.load_input.setFixedHeight(32)
        self.load_input.textChanged[str].connect(self.onChangedInput)
        self.load_input.setVisible(False)

        self.load_input_send_btn = QPushButton("추출하기")
        self.load_input_send_btn.setFixedHeight(32)
        self.load_input_send_btn.clicked.connect(self.btn_fun_crawling)
        self.load_input_send_btn.setVisible(False)

        self.extract_excel_btn = QPushButton("엑셀로 다운받기")
        self.extract_excel_btn.setStyleSheet("width: 128px;"
                                    "height: 32px;")
        self.extract_excel_btn.clicked.connect(self.btn_fun_extract_excel)
        self.extract_excel_btn.setVisible(False)

        self.extract_image_btn = QPushButton("이미지로 다운받기")
        self.extract_image_btn.setStyleSheet("width: 128px;"
                                    "height: 32px;")
        self.extract_image_btn.clicked.connect(self.btn_fun_extract_image)
        self.extract_image_btn.setVisible(False)

        h_box_1 = QHBoxLayout()
        h_box_1.addStretch(1)
        h_box_1.addWidget(self.extract_excel_btn)
        h_box_1.addWidget(self.extract_image_btn)
        h_box_1.addStretch(1)

        h_box_input = QHBoxLayout()
        h_box_input.addStretch(1)
        h_box_input.addWidget(self.load_input)
        h_box_input.addWidget(self.load_input_send_btn)
        h_box_input.addStretch(1)

        h_box_2 = QHBoxLayout()
        h_box_2.addStretch(1)
        h_box_2.addWidget(self.load_btn)
        h_box_2.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(3)
        vbox.addLayout(h_box_2)
        vbox.addLayout(h_box_input)
        vbox.addStretch(3)
        vbox.addLayout(h_box_1)
        vbox.addStretch(1)

        self.central_widget.setLayout(vbox)
        self.setCentralWidget(self.central_widget)

    def onChangedInput(self, text):
        self.url = text

    def btn_fun_file_load(self):
        path, _ = QFileDialog.getOpenFileName(self)
        if not (path == ''):
            if str(path).endswith(".txt"):
                self.load_btn.setVisible(False)
                self.extract_image_btn.setVisible(True)
                self.extract_excel_btn.setVisible(True)
                with open(path, 'r') as f:
                    self.last_mode = "file"
                    self.textAnalysis(f.read())
                    if len(self.noun_list) > 0 and len(self.count) > 0:
                        self.load_btn.setVisible(False)
                        self.load_input.setVisible(False)
                        self.load_input_send_btn.setVisible(False)
                        self.extract_image_btn.setVisible(True)
                        self.extract_excel_btn.setVisible(True)
                    else:
                        QMessageBox.warning(self, '경고', '내용이 너무 부족합니다.')
                        if self.last_mode == 'file':
                            self.load_btn.setVisible(True)
                            self.load_input.setVisible(False)
                            self.load_input_send_btn.setVisible(False)
                        else:
                            self.load_btn.setVisible(False)
                            self.load_input.setVisible(True)
                            self.load_input_send_btn.setVisible(True)
                        self.extract_image_btn.setVisible(False)
                        self.extract_excel_btn.setVisible(False)
            else:
                QMessageBox.warning(self, '경고', '지원하지 않는 파일 형식입니다.\n txt 파일만 지원합니다.')

    def btn_fun_crawling(self):
        if (self.url.startswith("http://") or self.url.startswith("https://")) and "blog.naver.com" in self.url and "m.blog.naver.com" not in self.url:
            res = requests.get(self.url)
            if res.status_code == 200:
                soup = BeautifulSoup(res.content, "lxml")
                url = soup.find("iframe").get("src")
                res = requests.get("https://blog.naver.com" + url)
                if res.status_code == 200:
                    soup = BeautifulSoup(res.content, "lxml")
                    text = soup.find(id="post-view" + self.url.split("/")[-1]).text
                    self.last_mode = "url"
                    self.textAnalysis(text)
                    if len(self.noun_list) > 0 and len(self.count) > 0:
                        self.load_btn.setVisible(False)
                        self.load_input.setVisible(False)
                        self.load_input_send_btn.setVisible(False)
                        self.extract_image_btn.setVisible(True)
                        self.extract_excel_btn.setVisible(True)
                    else:
                        QMessageBox.warning(self, '경고', '내용이 너무 부족합니다.')
                        if self.last_mode == 'file':
                            self.load_btn.setVisible(True)
                            self.load_input.setVisible(False)
                            self.load_input_send_btn.setVisible(False)
                        else:
                            self.load_btn.setVisible(False)
                            self.load_input.setVisible(True)
                            self.load_input_send_btn.setVisible(True)
                        self.extract_image_btn.setVisible(False)
                        self.extract_excel_btn.setVisible(False)
        else:
            if self.url in "blog.naver.com":
                QMessageBox.warning(self, '경고', 'https:// 나 https://로 시작해야 합니다.')
            elif self.url in "m.blog.naver.com":
                QMessageBox.warning(self, '경고', '현재는 모바일 네이버 블로그는 지원하지 않습니다.')
            else:
                QMessageBox.warning(self, '경고', '현재는 네이버 블로그만 지원합니다.')

    def btn_fun_extract_excel(self):
        if self.last_mode == "file":
            self.load_btn.setVisible(True)
        else:
            self.load_input.setVisible(True)
            self.load_input_send_btn.setVisible(True)

        self.extract_image_btn.setVisible(False)
        self.extract_excel_btn.setVisible(False)
        
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        ws.append(["단어", "빈도수"])
        for row in self.noun_list:
            ws.append(row)
        wb.save("내 글 빈도수.xlsx")


    def btn_fun_extract_image(self):
        if self.last_mode == "file":
            self.load_btn.setVisible(True)
        else:
            self.load_input.setVisible(True)
            self.load_input_send_btn.setVisible(True)

        self.extract_image_btn.setVisible(False)
        self.extract_excel_btn.setVisible(False)

        from wordcloud import WordCloud
        if platform.system() == "Windows":
            wc = WordCloud(font_path='C:\Windows\Fonts\malgun.ttf', width=400, height=400, scale=2.0, max_font_size=240)
        else:
            wc = WordCloud(font_path='/Users/mineru/Library/Fonts/NanumBarunGothic.ttf', width=400, height=400, scale=2.0, max_font_size=240)
        wc.generate_from_frequencies(self.count)
        wc.to_file('내 글 빈도수.png')

    def change_file_mode(self):
        self.load_btn.setVisible(True)
        self.load_input.setVisible(False)
        self.load_input_send_btn.setVisible(False)
        self.extract_image_btn.setVisible(False)
        self.extract_excel_btn.setVisible(False)

    def change_url_mode(self):
        self.load_btn.setVisible(False)
        self.load_input.setVisible(True)
        self.load_input_send_btn.setVisible(True)
        self.extract_image_btn.setVisible(False)
        self.extract_excel_btn.setVisible(False)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if len(files) == 1:
            for path in files:
                if str(path).endswith(".txt"):
                    with open(path, 'r') as f:
                        self.last_mode = "file"
                        self.textAnalysis(f.read())
                        if len(self.noun_list) > 0 and len(self.count) > 0:
                            self.load_btn.setVisible(False)
                            self.load_input.setVisible(False)
                            self.load_input_send_btn.setVisible(False)
                            self.extract_image_btn.setVisible(True)
                            self.extract_excel_btn.setVisible(True)
                        else:
                            QMessageBox.warning(self, '경고', '내용이 너무 부족합니다.')
                            if self.last_mode == 'file':
                                self.load_btn.setVisible(True)
                                self.load_input.setVisible(False)
                                self.load_input_send_btn.setVisible(False)
                            else:
                                self.load_btn.setVisible(False)
                                self.load_input.setVisible(True)
                                self.load_input_send_btn.setVisible(True)
                            self.extract_image_btn.setVisible(False)
                            self.extract_excel_btn.setVisible(False)
                else:
                    QMessageBox.warning(self, '경고', '지원하지 않는 파일 형식입니다.\n txt 파일만 지원합니다.')
        else:
            QMessageBox.warning(self, '경고', '파일은 하나만 올릴 수 있습니다.')

    def textAnalysis(self, text):
        from jpype._jvmfinder import JVMNotFoundException
        try:
            from konlpy.tag import Okt
            from collections import Counter
            if platform.system() == "Windows":
                noun = Okt().nouns(text)
            else:
                noun = Okt(jvmpath="/Library/Java/JavaVirtualMachines/zulu-15.jdk/Contents/Home/lib/server/libjvm.dylib").nouns(text)
            for i, v in enumerate(noun):
                if len(v) < 2:
                    noun.pop(i)
            self.count = Counter(noun)
            self.noun_list = self.count.most_common(100)
        except JVMNotFoundException:
            QMessageBox.warning(self, '경고', '시스템 환경변수로 JAVA_HOME 설정이 되어 있지 않습니다.')

if __name__ == '__main__':
   app = QApplication(sys.argv)
   window = MyApp()
   window.show()
   sys.exit(app.exec())
