# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(966, 578)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ptn_open = QtWidgets.QPushButton(self.centralwidget)
        self.ptn_open.setGeometry(QtCore.QRect(10, 20, 93, 28))
        self.ptn_open.setObjectName("ptn_open")
        self.ptn_translation = QtWidgets.QPushButton(self.centralwidget)
        self.ptn_translation.setGeometry(QtCore.QRect(660, 450, 93, 28))
        self.ptn_translation.setObjectName("ptn_translation")
        self.treeWidget_language = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget_language.setGeometry(QtCore.QRect(10, 60, 271, 441))
        self.treeWidget_language.setObjectName("treeWidget_language")
        self.lineEdit_word = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_word.setGeometry(QtCore.QRect(330, 50, 201, 31))
        self.lineEdit_word.setObjectName("lineEdit_word")
        self.lineEdit_language = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_language.setGeometry(QtCore.QRect(740, 50, 131, 31))
        self.lineEdit_language.setObjectName("lineEdit_language")
        self.textEdit_ouput = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_ouput.setGeometry(QtCore.QRect(330, 110, 301, 391))
        self.textEdit_ouput.setObjectName("textEdit_ouput")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(330, 20, 72, 15))
        self.label.setObjectName("label")
        self.lineEdit_word_ch = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_word_ch.setGeometry(QtCore.QRect(550, 50, 171, 31))
        self.lineEdit_word_ch.setObjectName("lineEdit_word_ch")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(560, 20, 72, 15))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(750, 20, 72, 15))
        self.label_3.setObjectName("label_3")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(650, 110, 211, 80))
        self.groupBox.setObjectName("groupBox")
        self.radioButton_word = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_word.setGeometry(QtCore.QRect(10, 20, 115, 19))
        self.radioButton_word.setChecked(True)
        self.radioButton_word.setObjectName("radioButton_word")
        self.radioButton_all = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_all.setGeometry(QtCore.QRect(10, 50, 161, 19))
        self.radioButton_all.setObjectName("radioButton_all")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(650, 200, 271, 231))
        self.groupBox_2.setObjectName("groupBox_2")
        self.radioButton_shield = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_shield.setGeometry(QtCore.QRect(10, 20, 115, 19))
        self.radioButton_shield.setChecked(True)
        self.radioButton_shield.setObjectName("radioButton_shield")
        self.radioButton_customer = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_customer.setGeometry(QtCore.QRect(20, 150, 115, 19))
        self.radioButton_customer.setObjectName("radioButton_customer")
        self.radioButton_google = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_google.setGeometry(QtCore.QRect(20, 190, 115, 19))
        self.radioButton_google.setObjectName("radioButton_google")
        self.ptn_open_customer = QtWidgets.QPushButton(self.groupBox_2)
        self.ptn_open_customer.setGeometry(QtCore.QRect(120, 140, 93, 31))
        self.ptn_open_customer.setObjectName("ptn_open_customer")
        self.checkBox_shield_0 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_shield_0.setGeometry(QtCore.QRect(30, 50, 81, 19))
        self.checkBox_shield_0.setChecked(True)
        self.checkBox_shield_0.setObjectName("checkBox_shield_0")
        self.checkBox_shield_1 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_shield_1.setGeometry(QtCore.QRect(30, 70, 111, 19))
        self.checkBox_shield_1.setObjectName("checkBox_shield_1")
        self.checkBox_shield_2 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_shield_2.setGeometry(QtCore.QRect(30, 90, 81, 19))
        self.checkBox_shield_2.setObjectName("checkBox_shield_2")
        self.checkBox_shield_3 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_shield_3.setGeometry(QtCore.QRect(30, 110, 81, 19))
        self.checkBox_shield_3.setObjectName("checkBox_shield_3")
        self.checkBox_shield_4 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_shield_4.setGeometry(QtCore.QRect(140, 50, 121, 19))
        self.checkBox_shield_4.setObjectName("checkBox_shield_4")
        self.checkBox_shield_5 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_shield_5.setGeometry(QtCore.QRect(140, 70, 121, 19))
        self.checkBox_shield_5.setObjectName("checkBox_shield_5")
        self.checkBox_shield_6 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_shield_6.setGeometry(QtCore.QRect(140, 90, 121, 19))
        self.checkBox_shield_6.setObjectName("checkBox_shield_6")
        self.radioButton_google_youdao = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_google_youdao.setGeometry(QtCore.QRect(140, 190, 121, 21))
        self.radioButton_google_youdao.setObjectName("radioButton_google_youdao")
        self.ptn_check = QtWidgets.QPushButton(self.centralwidget)
        self.ptn_check.setGeometry(QtCore.QRect(770, 450, 101, 28))
        self.ptn_check.setObjectName("ptn_check")
        self.ptn_export = QtWidgets.QPushButton(self.centralwidget)
        self.ptn_export.setGeometry(QtCore.QRect(660, 490, 211, 28))
        self.ptn_export.setObjectName("ptn_export")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 966, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.ptn_open.setText(_translate("MainWindow", "打开"))
        self.ptn_translation.setText(_translate("MainWindow", "翻译并输出"))
        self.treeWidget_language.headerItem().setText(0, _translate("MainWindow", "请选择要翻译的语言"))
        self.label.setText(_translate("MainWindow", "英语"))
        self.label_2.setText(_translate("MainWindow", "中文"))
        self.label_3.setText(_translate("MainWindow", "翻译语言"))
        self.groupBox.setTitle(_translate("MainWindow", "选择翻译模式"))
        self.radioButton_word.setText(_translate("MainWindow", "翻译单个字串"))
        self.radioButton_all.setText(_translate("MainWindow", "翻译excel文件"))
        self.groupBox_2.setTitle(_translate("MainWindow", "选择翻译途径"))
        self.radioButton_shield.setText(_translate("MainWindow", "翻译库翻译"))
        self.radioButton_customer.setText(_translate("MainWindow", "客户翻译"))
        self.radioButton_google.setText(_translate("MainWindow", "google翻译"))
        self.ptn_open_customer.setText(_translate("MainWindow", "打开翻译"))
        self.checkBox_shield_0.setText(_translate("MainWindow", "CVTE"))
        self.checkBox_shield_1.setText(_translate("MainWindow", "newoldtran"))
        self.checkBox_shield_2.setText(_translate("MainWindow", "cnpd"))
        self.checkBox_shield_3.setText(_translate("MainWindow", "faepv"))
        self.checkBox_shield_4.setText(_translate("MainWindow", "hisense"))
        self.checkBox_shield_5.setText(_translate("MainWindow", "tcl"))
        self.checkBox_shield_6.setText(_translate("MainWindow", "caixun"))
        self.radioButton_google_youdao.setText(_translate("MainWindow", "google+有道"))
        self.ptn_check.setText(_translate("MainWindow", "刷新进度"))
        self.ptn_export.setText(_translate("MainWindow", "导出未翻译字符串"))
