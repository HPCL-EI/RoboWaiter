# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(895, 980)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(100)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(14)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_2.addWidget(self.label_10)
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(14)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_2.addWidget(self.label_11)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.list_customer = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_customer.sizePolicy().hasHeightForWidth())
        self.list_customer.setSizePolicy(sizePolicy)
        self.list_customer.setMinimumSize(QtCore.QSize(50, 250))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.list_customer.setFont(font)
        self.list_customer.setObjectName("list_customer")
        item = QtWidgets.QListWidgetItem()
        self.list_customer.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.list_customer.addItem(item)
        self.horizontalLayout.addWidget(self.list_customer)
        self.edit_local_history = QtWidgets.QTextEdit(self.centralwidget)
        self.edit_local_history.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edit_local_history.sizePolicy().hasHeightForWidth())
        self.edit_local_history.setSizePolicy(sizePolicy)
        self.edit_local_history.setMinimumSize(QtCore.QSize(340, 0))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.edit_local_history.setFont(font)
        self.edit_local_history.setReadOnly(True)
        self.edit_local_history.setObjectName("edit_local_history")
        self.horizontalLayout.addWidget(self.edit_local_history)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout_4, 1, 1, 5, 2)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.img_view_bt = QtWidgets.QGraphicsView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.img_view_bt.sizePolicy().hasHeightForWidth())
        self.img_view_bt.setSizePolicy(sizePolicy)
        self.img_view_bt.setMinimumSize(QtCore.QSize(0, 240))
        self.img_view_bt.setObjectName("img_view_bt")
        self.verticalLayout_2.addWidget(self.img_view_bt)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 1, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QtCore.QSize(355, 0))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(14)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(14)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_4.addWidget(self.label_8)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.img_label_map = QtWidgets.QLabel(self.centralwidget)
        self.img_label_map.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.img_label_map.sizePolicy().hasHeightForWidth())
        self.img_label_map.setSizePolicy(sizePolicy)
        self.img_label_map.setMinimumSize(QtCore.QSize(345, 200))
        self.img_label_map.setStyleSheet("border: 2px solid black;")
        self.img_label_map.setText("")
        self.img_label_map.setObjectName("img_label_map")
        self.horizontalLayout_5.addWidget(self.img_label_map)
        self.img_label_seg = QtWidgets.QLabel(self.centralwidget)
        self.img_label_seg.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.img_label_seg.sizePolicy().hasHeightForWidth())
        self.img_label_seg.setSizePolicy(sizePolicy)
        self.img_label_seg.setMinimumSize(QtCore.QSize(250, 200))
        self.img_label_seg.setStyleSheet("border: 2px solid black;")
        self.img_label_seg.setText("")
        self.img_label_seg.setObjectName("img_label_seg")
        self.horizontalLayout_5.addWidget(self.img_label_seg)
        self.img_label_obj = QtWidgets.QLabel(self.centralwidget)
        self.img_label_obj.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.img_label_obj.sizePolicy().hasHeightForWidth())
        self.img_label_obj.setSizePolicy(sizePolicy)
        self.img_label_obj.setMinimumSize(QtCore.QSize(250, 200))
        self.img_label_obj.setStyleSheet("border: 2px solid black;")
        self.img_label_obj.setText("")
        self.img_label_obj.setObjectName("img_label_obj")
        self.horizontalLayout_5.addWidget(self.img_label_obj)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 1, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 6, 0, 1, 3)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.textBrowser_5 = QtWidgets.QTextBrowser(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.textBrowser_5.setFont(font)
        self.textBrowser_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.textBrowser_5.setStyleSheet("text-align:center;")
        self.textBrowser_5.setMarkdown("")
        self.textBrowser_5.setObjectName("textBrowser_5")
        self.verticalLayout_3.addWidget(self.textBrowser_5)
        self.gridLayout.addLayout(self.verticalLayout_3, 5, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)
        self.btn_say = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(14)
        self.btn_say.setFont(font)
        self.btn_say.setObjectName("btn_say")
        self.gridLayout.addWidget(self.btn_say, 0, 2, 1, 1)
        self.edit_say = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.edit_say.setFont(font)
        self.edit_say.setObjectName("edit_say")
        self.gridLayout.addWidget(self.edit_say, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_reset = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(14)
        self.btn_reset.setFont(font)
        self.btn_reset.setObjectName("btn_reset")
        self.verticalLayout.addWidget(self.btn_reset)
        self.btn_AEM = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(14)
        self.btn_AEM.setFont(font)
        self.btn_AEM.setObjectName("btn_AEM")
        self.verticalLayout.addWidget(self.btn_AEM)
        self.btn_VLN = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(14)
        self.btn_VLN.setFont(font)
        self.btn_VLN.setObjectName("btn_VLN")
        self.verticalLayout.addWidget(self.btn_VLN)
        self.btn_VLM = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(14)
        self.btn_VLM.setFont(font)
        self.btn_VLM.setObjectName("btn_VLM")
        self.verticalLayout.addWidget(self.btn_VLM)
        self.btn_GQA = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(14)
        self.btn_GQA.setFont(font)
        self.btn_GQA.setObjectName("btn_GQA")
        self.verticalLayout.addWidget(self.btn_GQA)
        self.btn_OT = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(14)
        self.btn_OT.setFont(font)
        self.btn_OT.setObjectName("btn_OT")
        self.verticalLayout.addWidget(self.btn_OT)
        self.btn_AT = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(14)
        self.btn_AT.setFont(font)
        self.btn_AT.setObjectName("btn_AT")
        self.verticalLayout.addWidget(self.btn_AT)
        self.cb_task = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_task.sizePolicy().hasHeightForWidth())
        self.cb_task.setSizePolicy(sizePolicy)
        self.cb_task.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(14)
        self.cb_task.setFont(font)
        self.cb_task.setEditable(False)
        self.cb_task.setCurrentText("")
        self.cb_task.setInsertPolicy(QtWidgets.QComboBox.InsertAtBottom)
        self.cb_task.setObjectName("cb_task")
        self.verticalLayout.addWidget(self.cb_task)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.cb_task.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RoboWatier"))
        self.label_10.setText(_translate("MainWindow", "Customer List"))
        self.label_11.setText(_translate("MainWindow", "History of Conversations"))
        __sortingEnabled = self.list_customer.isSortingEnabled()
        self.list_customer.setSortingEnabled(False)
        item = self.list_customer.item(0)
        item.setText(_translate("MainWindow", "Global"))
        item = self.list_customer.item(1)
        item.setText(_translate("MainWindow", "System"))
        self.list_customer.setSortingEnabled(__sortingEnabled)
        self.label_5.setText(_translate("MainWindow", "Current Behavior Tree"))
        self.label_6.setText(_translate("MainWindow", "Accessibility Map"))
        self.label_7.setText(_translate("MainWindow", "Instance Segmentation"))
        self.label_8.setText(_translate("MainWindow", "Object Detection"))
        self.textBrowser_5.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'黑体\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p></body></html>"))
        self.label_9.setText(_translate("MainWindow", "Task Demo: (Wait for animation to finish before resetting scene.)"))
        self.btn_say.setText(_translate("MainWindow", "Speak"))
        self.edit_say.setText(_translate("MainWindow", "Is(AC,On)"))
        self.label.setText(_translate("MainWindow", "Semantic Information"))
        self.btn_reset.setText(_translate("MainWindow", "Reset Scene"))
        self.btn_AEM.setText(_translate("MainWindow", "Environment Exploration"))
        self.btn_VLN.setText(_translate("MainWindow", "Visual Language Navigation"))
        self.btn_VLM.setText(_translate("MainWindow", "Visual Language Manipulation"))
        self.btn_GQA.setText(_translate("MainWindow", "Embodied Multi-turn Dialogue"))
        self.btn_OT.setText(_translate("MainWindow", "Complex Embodied Tasks"))
        self.btn_AT.setText(_translate("MainWindow", "Autonomous Embodied Tasks"))
        self.cb_task.setProperty("placeholderText", _translate("MainWindow", "其他任务"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

