# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'admin.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QStatusBar, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(955, 713)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.menuFrame = QFrame(self.centralwidget)
        self.menuFrame.setObjectName(u"menuFrame")
        self.menuFrame.setMaximumSize(QSize(220, 16777215))
        self.menuFrame.setFrameShape(QFrame.StyledPanel)
        self.menuFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.menuFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_3 = QLabel(self.menuFrame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 70))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_3)

        self.line = QFrame(self.menuFrame)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.btnHome = QPushButton(self.menuFrame)
        self.btnHome.setObjectName(u"btnHome")

        self.verticalLayout.addWidget(self.btnHome)

        self.btnStudent = QPushButton(self.menuFrame)
        self.btnStudent.setObjectName(u"btnStudent")

        self.verticalLayout.addWidget(self.btnStudent)

        self.btnScore = QPushButton(self.menuFrame)
        self.btnScore.setObjectName(u"btnScore")

        self.verticalLayout.addWidget(self.btnScore)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.btnLogout = QPushButton(self.menuFrame)
        self.btnLogout.setObjectName(u"btnLogout")

        self.verticalLayout.addWidget(self.btnLogout)


        self.horizontalLayout.addWidget(self.menuFrame)

        self.contentFrame = QFrame(self.centralwidget)
        self.contentFrame.setObjectName(u"contentFrame")
        self.contentFrame.setFrameShape(QFrame.StyledPanel)
        self.contentFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.contentFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.mainStack = QStackedWidget(self.contentFrame)
        self.mainStack.setObjectName(u"mainStack")
        self.pageHome = QWidget()
        self.pageHome.setObjectName(u"pageHome")
        self.horizontalLayout_2 = QHBoxLayout(self.pageHome)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.pageHome)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(30)
        font1.setBold(True)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label)

        self.mainStack.addWidget(self.pageHome)
        self.pageStudents = QWidget()
        self.pageStudents.setObjectName(u"pageStudents")
        self.verticalLayout_3 = QVBoxLayout(self.pageStudents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(self.pageStudents)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.verticalLayout_3.addWidget(self.label_2)

        self.widget = QWidget(self.pageStudents)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_7 = QHBoxLayout(self.widget)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_7 = QLabel(self.widget)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_7.addWidget(self.label_7)

        self.txtSearch = QLineEdit(self.widget)
        self.txtSearch.setObjectName(u"txtSearch")
        self.txtSearch.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_7.addWidget(self.txtSearch)

        self.btnSearch = QPushButton(self.widget)
        self.btnSearch.setObjectName(u"btnSearch")

        self.horizontalLayout_7.addWidget(self.btnSearch)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_5)


        self.verticalLayout_3.addWidget(self.widget)

        self.frame = QFrame(self.pageStudents)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(16777215, 16777215))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.btnAddStudent = QPushButton(self.frame)
        self.btnAddStudent.setObjectName(u"btnAddStudent")

        self.horizontalLayout_3.addWidget(self.btnAddStudent)

        self.btnEditStudent = QPushButton(self.frame)
        self.btnEditStudent.setObjectName(u"btnEditStudent")

        self.horizontalLayout_3.addWidget(self.btnEditStudent)

        self.btnDeleteStudent = QPushButton(self.frame)
        self.btnDeleteStudent.setObjectName(u"btnDeleteStudent")

        self.horizontalLayout_3.addWidget(self.btnDeleteStudent)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addWidget(self.frame)

        self.tablesStudent = QTableWidget(self.pageStudents)
        self.tablesStudent.setObjectName(u"tablesStudent")

        self.verticalLayout_3.addWidget(self.tablesStudent)

        self.mainStack.addWidget(self.pageStudents)
        self.pageScores = QWidget()
        self.pageScores.setObjectName(u"pageScores")
        self.verticalLayout_4 = QVBoxLayout(self.pageScores)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_4 = QLabel(self.pageScores)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)

        self.verticalLayout_4.addWidget(self.label_4)

        self.frame_2 = QFrame(self.pageScores)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_5 = QLabel(self.frame_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(70, 0))
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_5)

        self.cboClassSelect = QComboBox(self.frame_2)
        self.cboClassSelect.setObjectName(u"cboClassSelect")
        self.cboClassSelect.setMinimumSize(QSize(130, 0))

        self.horizontalLayout_4.addWidget(self.cboClassSelect)

        self.label_6 = QLabel(self.frame_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(70, 0))
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_6)

        self.cbSubject = QComboBox(self.frame_2)
        self.cbSubject.setObjectName(u"cbSubject")
        self.cbSubject.setMinimumSize(QSize(130, 0))

        self.horizontalLayout_4.addWidget(self.cbSubject)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.btnLoadScores = QPushButton(self.frame_2)
        self.btnLoadScores.setObjectName(u"btnLoadScores")

        self.horizontalLayout_4.addWidget(self.btnLoadScores)


        self.verticalLayout_4.addWidget(self.frame_2)

        self.widgetChart = QWidget(self.pageScores)
        self.widgetChart.setObjectName(u"widgetChart")
        self.widgetChart.setMinimumSize(QSize(400, 300))

        self.verticalLayout_4.addWidget(self.widgetChart)

        self.tableScores = QTableWidget(self.pageScores)
        if (self.tableScores.columnCount() < 6):
            self.tableScores.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableScores.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableScores.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableScores.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableScores.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableScores.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableScores.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        self.tableScores.setObjectName(u"tableScores")

        self.verticalLayout_4.addWidget(self.tableScores)

        self.mainStack.addWidget(self.pageScores)

        self.verticalLayout_2.addWidget(self.mainStack)

        self.frame_3 = QFrame(self.contentFrame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.btnSaveScore = QPushButton(self.frame_3)
        self.btnSaveScore.setObjectName(u"btnSaveScore")

        self.horizontalLayout_5.addWidget(self.btnSaveScore)

        self.btnExportExcel = QPushButton(self.frame_3)
        self.btnExportExcel.setObjectName(u"btnExportExcel")

        self.horizontalLayout_5.addWidget(self.btnExportExcel)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)


        self.verticalLayout_2.addWidget(self.frame_3)


        self.horizontalLayout.addWidget(self.contentFrame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.mainStack.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"ADMIN", None))
        self.btnHome.setText(QCoreApplication.translate("MainWindow", u"Trang ch\u1ee7", None))
        self.btnStudent.setText(QCoreApplication.translate("MainWindow", u"H\u1ecdc vi\u00ean", None))
        self.btnScore.setText(QCoreApplication.translate("MainWindow", u"\u0110i\u1ec3m s\u1ed1", None))
        self.btnLogout.setText(QCoreApplication.translate("MainWindow", u"\u0110\u0103ng xu\u1ea5t", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"WELCOME ADMIN", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"-- H\u1ecdc Sinh --", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"T\u00ecm h\u1ecdc sinh", None))
        self.btnSearch.setText(QCoreApplication.translate("MainWindow", u"T\u00ecm ki\u1ebfm", None))
        self.btnAddStudent.setText(QCoreApplication.translate("MainWindow", u"Th\u00eam", None))
        self.btnEditStudent.setText(QCoreApplication.translate("MainWindow", u"S\u1eeda", None))
        self.btnDeleteStudent.setText(QCoreApplication.translate("MainWindow", u"X\u00f3a", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"-- \u0110i\u1ec3m --", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Ch\u1ecdn L\u1edbp", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"M\u00f4n h\u1ecdc", None))
        self.btnLoadScores.setText(QCoreApplication.translate("MainWindow", u"T\u1ea3i danh s\u00e1ch", None))
        ___qtablewidgetitem = self.tableScores.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"M\u00e3 HS", None));
        ___qtablewidgetitem1 = self.tableScores.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"H\u1ecd T\u00ean", None));
        ___qtablewidgetitem2 = self.tableScores.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\u0110i\u1ec3m 15p", None));
        ___qtablewidgetitem3 = self.tableScores.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"\u0110i\u1ec3m 1 ti\u1ebft", None));
        ___qtablewidgetitem4 = self.tableScores.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Thi HK", None));
        ___qtablewidgetitem5 = self.tableScores.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"\u0110i\u1ec3m TB", None));
        self.btnSaveScore.setText(QCoreApplication.translate("MainWindow", u"L\u01b0u b\u1ea3ng \u0111i\u1ec3m", None))
        self.btnExportExcel.setText(QCoreApplication.translate("MainWindow", u"Xu\u1ea5t Excel", None))
    # retranslateUi

