# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test1.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(600, 578)
        Form.setStyleSheet(_fromUtf8("background-color: rgb(166, 166, 166);\n"
"background-color: rgb(189, 189, 189);"))
        self.frame = QtGui.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(0, 140, 581, 361))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.pushButton = QtGui.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(110, 10, 111, 111))
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setStyleSheet(_fromUtf8("image: url(:/Images/Webp.net-resizeimage (11).png);"))
        self.pushButton.setText(_fromUtf8(""))
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 120, 111, 111))
        self.pushButton_2.setStyleSheet(_fromUtf8("image: url(:/Images/Webp.net-resizeimage (14).png);"))
        self.pushButton_2.setText(_fromUtf8(""))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_4 = QtGui.QPushButton(self.frame)
        self.pushButton_4.setGeometry(QtCore.QRect(220, 120, 111, 111))
        self.pushButton_4.setStyleSheet(_fromUtf8("image: url(:/Images/Webp.net-resizeimage (12).png);"))
        self.pushButton_4.setText(_fromUtf8(""))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_3 = QtGui.QPushButton(self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(110, 230, 111, 111))
        self.pushButton_3.setStyleSheet(_fromUtf8("image: url(:/Images/Webp.net-resizeimage (13).png);\n"
""))
        self.pushButton_3.setText(_fromUtf8(""))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.toolButton = QtGui.QToolButton(self.frame)
        self.toolButton.setGeometry(QtCore.QRect(480, 180, 101, 71))
        self.toolButton.setStyleSheet(_fromUtf8("image: url(:/Images/Webp.net-resizeimage (9).png);"))
        self.toolButton.setText(_fromUtf8(""))
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.toolButton_2 = QtGui.QToolButton(self.frame)
        self.toolButton_2.setGeometry(QtCore.QRect(480, 270, 101, 71))
        self.toolButton_2.setStyleSheet(_fromUtf8("image: url(:/Images/46482116_1169052599948086_2306507513668829184_n.png);"))
        self.toolButton_2.setText(_fromUtf8(""))
        self.toolButton_2.setObjectName(_fromUtf8("toolButton_2"))
        self.textEdit = QtGui.QTextEdit(self.frame)
        self.textEdit.setGeometry(QtCore.QRect(430, 0, 141, 31))
        self.textEdit.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);\n"
"color: rgb(255, 255, 255);"))
        self.textEdit.setFrameShape(QtGui.QFrame.StyledPanel)
        self.textEdit.setFrameShadow(QtGui.QFrame.Sunken)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.label_7 = QtGui.QLabel(self.frame)
        self.label_7.setGeometry(QtCore.QRect(280, 0, 151, 31))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.pushButton_5 = QtGui.QPushButton(self.frame)
        self.pushButton_5.setGeometry(QtCore.QRect(480, 80, 101, 81))
        self.pushButton_5.setStyleSheet(_fromUtf8("image: url(:/Images/Webp.net-resizeimage (8).png);"))
        self.pushButton_5.setText(_fromUtf8(""))
        self.pushButton_5.setAutoDefault(False)
        self.pushButton_5.setDefault(False)
        self.pushButton_5.setFlat(False)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.frame_2 = QtGui.QFrame(Form)
        self.frame_2.setGeometry(QtCore.QRect(0, 490, 581, 81))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.label_4 = QtGui.QLabel(self.frame_2)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 71, 51))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_6 = QtGui.QLabel(self.frame_2)
        self.label_6.setGeometry(QtCore.QRect(80, 30, 281, 31))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.frame_3 = QtGui.QFrame(Form)
        self.frame_3.setGeometry(QtCore.QRect(0, -1, 591, 141))
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.label_2 = QtGui.QLabel(self.frame_3)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 261, 61))
        self.label_2.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label = QtGui.QLabel(self.frame_3)
        self.label.setGeometry(QtCore.QRect(480, 0, 101, 101))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_5 = QtGui.QLabel(self.frame_3)
        self.label_5.setGeometry(QtCore.QRect(160, 70, 191, 71))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_3 = QtGui.QLabel(self.frame_3)
        self.label_3.setGeometry(QtCore.QRect(480, 100, 101, 21))
        self.label_3.setStyleSheet(_fromUtf8("background-color: rgb(189, 189, 189);"))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.frame_3.raise_()
        self.frame_2.raise_()
        self.frame.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_7.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600; color:#003264;\">Current Mode:</span></p></body></html>", None))
        self.label_4.setText(_translate("Form", "<html><head/><body><p><img src=\":/Images/Webp.net-resizeimage (5).png\"/></p></body></html>", None))
        self.label_6.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; color:#003264;\">Graphical user interface driving the car</span></p></body></html>", None))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><img src=\":/Images/Webp.net-resizeimage (3).png\"/></p></body></html>", None))
        self.label.setText(_translate("Form", "<html><head/><body><p><img src=\":/Images/Webp.net-resizeimage.jpg\"/></p></body></html>", None))
        self.label_5.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600; color:#003264;\">BrakeOrDie Project</span></p></body></html>", None))
        self.label_3.setText(_translate("Form", "<html><head/><body><p><a href=\"https://sites.google.com/site/projetsecinsa/projets-2018-2019/project-moscou\"><span style=\" font-size:10pt; text-decoration: underline; color:#0000ff;\">@TeamMoscou</span></a></p></body></html>", None))

import frame2_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

