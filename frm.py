#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, time
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QCheckBox, QDialog, QAction, QWidget, QPushButton, QRadioButton, QGroupBox, QGridLayout, QVBoxLayout, QLabel, QComboBox, QButtonGroup
from PyQt5.QtGui import QIcon, QPixmap, QPainter
import pandas as pd
#from PyQt5.QtCore import pyqtSlot


class App(QMainWindow):
    
    def __init__(self):
        super().__init__()
        #self.title = 'PyQt5 menu - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 400
        self.questions = {0: 'qbank', 'answers': dict()}
        self.initUI()

    def initUI(self):
        #self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        
        setupButton = QAction('Setup', self)
        setupButton.triggered.connect(self.properties)
        fileMenu.addAction(setupButton)
        
        exitButton = QAction('Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)
        
        self.workflow = Workflow(self)
        self.setCentralWidget(self.workflow)
        
        self.show()
    
    def properties(self):
        self.prop_popup = Properties(self)
        self.prop_popup.show()  
    

class Workflow(QWidget):
    def __init__(self, parent):
        
        super().__init__()
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
                
        self.initUI(parent)
        
    def initUI(self, parent):
        self.setGeometry(self.left, self.top, self.width, self.height)
            
        self.createGridLayout(parent)
            
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
    
    def createGridLayout(self, parent):
        
        self.horizontalGroupBox = QGroupBox()
        layout = QGridLayout()
        
        self.picture = QLabel(self)
        layout.addWidget(self.picture, 0, 0, 1, 5)
        
        self.buttonGroup = QButtonGroup(self)
        
        self.bA = QRadioButton('A')
        self.bA.toggled.connect(lambda:self.btnstate(self.bA))
        self.buttonGroup.addButton(self.bA)
        layout.addWidget(self.bA, 1, 0)
        
        self.bB = QRadioButton('B')
        self.bB.toggled.connect(lambda:self.btnstate(self.bB))
        self.buttonGroup.addButton(self.bB)
        layout.addWidget(self.bB, 2, 0)
        
        self.bC = QRadioButton('C')
        self.bC.toggled.connect(lambda:self.btnstate(self.bC))
        self.buttonGroup.addButton(self.bC)
        layout.addWidget(self.bC, 3, 0)
        
        self.bD = QRadioButton('D')
        self.bD.toggled.connect(lambda:self.btnstate(self.bD))
        self.buttonGroup.addButton(self.bD)
        layout.addWidget(self.bD, 4, 0)
        
        
        self.bstart = QPushButton('Start', self)
        self.bstart.clicked.connect(lambda: self.run_test(parent))
        layout.addWidget(self.bstart, 5, 2)
                
        self.bprev = QPushButton('Prev', self)
        self.bprev.clicked.connect(lambda: self.move_prev(parent))
        self.bprev.setEnabled(False)
        layout.addWidget(self.bprev, 5, 3)
        
        self.bnext = QPushButton('Next', self)
        self.bnext.clicked.connect(lambda: self.move_next(parent))
        self.bnext.setEnabled(False)
        layout.addWidget(self.bnext, 5, 4)
                
        self.horizontalGroupBox.setLayout(layout)
    
    def move_prev(self, parent):
        parent.questions['answers'].update({self.picpos : self.answ.text()})
        self.picpos = max(self.picpos - 1, 0)
        
        if parent.questions['answers'].get(self.picpos):
            _answer = parent.questions['answers'].get(self.picpos)
            if _answer == 'A': self.bA.setChecked(True)
            if _answer == 'B': self.bB.setChecked(True)
            if _answer == 'C': self.bC.setChecked(True)
            if _answer == 'D': self.bD.setChecked(True)
        else:
            self.currb.setChecked(False)
        self.show_image(self.picpos, parent)
        
        if 'FINISH' in self.bnext.text():
            self.bnext.setText('Next')
        #print(parent.questions)
        
    def move_next(self, parent):
        
        #import ipdb; ipdb.set_trace()
        
        parent.questions['answers'].update({self.picpos : self.answ.text()})
        self.picpos = min(self.picpos + 1, len(parent.questions.get('questions')) - 1)
        #self.picpos = min(self.picpos + 1, len(parent.questions.get('questions')))
               
        
        if 'FINISH' in self.bnext.text():
            self.generate_result(parent)
        
        else:
            if self.picpos == len(parent.questions.get('questions')) - 1:
                self.bnext.setText('FINISH')

            if parent.questions['answers'].get(self.picpos):
                _answer = parent.questions['answers'].get(self.picpos)
                if _answer == 'A': self.bA.setChecked(True)
                if _answer == 'B': self.bB.setChecked(True)
                if _answer == 'C': self.bC.setChecked(True)
                if _answer == 'D': self.bD.setChecked(True)
            else:
                self.buttonGroup.setExclusive(False)
                self.currb.setChecked(False)
                self.buttonGroup.setExclusive(True)
                self.bnext.setEnabled(False)
                
            self.show_image(self.picpos, parent)
            #print(parent.questions)

    def btnstate(self, btn):
        self.currb = btn
        if btn.isChecked():
            self.answ = btn
            self.bnext.setEnabled(True)
            self.bprev.setEnabled(True)
    
    def show_image(self, img, parent):
        pixmap = QPixmap(parent.questions['questions'][int(img)])
        self.picture.setPixmap(pixmap)
    
    def run_test(self, parent):
        if 'Start' in self.bstart.text():
            self.bstart.setText('Interrupt')
            self.picpos = 0       
            self.show_image(self.picpos, parent)
        else:
            self.bstart.setText('Start')
        
        self.time_start = time.time()
    
    def generate_result(self, parent):
        
        results = pd.DataFrame(
            zip(
                [q.split('\\')[-1].split('.')[0] for q in parent.questions.get('questions')], 
                parent.questions.get('answers').values()
            ),
            columns=['question', 'answer']
        )
        checker = pd.read_csv(
            os.path.join(*parent.questions.get('questions')[0].split('\\')[:2], '.checker'), 
            delimiter=';',
            names=['question', 'checker']
        )
        
        results = pd.merge(results, checker, how='left', on='question')
        
        results = results.assign(result = results.answer == results.checker)
        
        print(results)
        
        elapsed = time.time() - self.time_start
        
        print(elapsed)
        

class Properties(QWidget):

    def __init__(self, parent):
        
        super().__init__()
        self.title = 'Setup'
        self.left = 10
        self.top = 10
        self.width = 200  
        self.height = 300
        self.questions = {0:parent.questions.get(0)}
    
        parent.choice = dict(
            source=None,
            part=None,
            book=None,
            topic=None
            )
                
        self.initUI(parent)
        
    def initUI(self, parent):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        layout = QGridLayout()
        
        self.stext = QLabel(self)
        self.stext.setText('Source:\t')
        layout.addWidget(self.stext, 0, 0)
        self.source = QComboBox(self)
        self.source.addItem(None)
        self.source.addItems(
            [f for f in os.listdir(self.questions.get(0)) if not f.startswith('.')]
            )
        self.source.activated.connect(lambda:\
            self.clicks(1, self.source.currentText(), None, self.part)
            )
        layout.addWidget(self.source, 0, 1)
        
        self.ptext = QLabel(self)
        self.ptext.setText('Part:\t')
        layout.addWidget(self.ptext, 1, 0)
        self.part = QComboBox(self)
        self.part.setEnabled(False)
        self.part.activated.connect(lambda:\
            self.clicks(2, self.part.currentText(), self.source, self.book)
            )
        layout.addWidget(self.part, 1, 1)
        
        self.btext = QLabel(self)
        self.btext.setText('Book:\t')
        layout.addWidget(self.btext, 2, 0)
        self.book = QComboBox(self)
        self.book.setEnabled(False)
        self.book.activated.connect(lambda:\
            self.clicks(3, self.book.currentText(), self.part, self.topic)
            )
        layout.addWidget(self.book, 2, 1)
        
        self.ttext = QLabel(self)
        self.ttext.setText('Topic:\t')
        layout.addWidget(self.ttext, 3, 0)
        self.topic = QComboBox(self)
        self.topic.setEnabled(False)
        self.topic.activated.connect(lambda:\
            self.clicks(4, self.topic.currentText(), self.book, self.bgen))
        layout.addWidget(self.topic, 3, 1)
        
        self.rtext = QLabel(self)
        self.rtext.setText('100q/4h:\t')
        layout.addWidget(self.rtext, 4, 0)
        
        self.chbox = QCheckBox(self)
        layout.addWidget(self.chbox, 4, 1)
        
        self.bgen = QPushButton('Generate', self)
        self.bgen.clicked.connect(lambda: self.list_generate(parent))
        self.bgen.setEnabled(False)
        layout.addWidget(self.bgen, 5, 1)

        self.setLayout(layout)

    def clicks(self, index, value, parent, child):
        if value:
            self.questions[index] = value
            if isinstance(child, QComboBox):
                child.setEnabled(True)
                self.update_combobox(child)
            if isinstance(child, QPushButton):
                child.setEnabled(True)
            if isinstance(parent, QComboBox):
                parent.setEnabled(False)

        else:
            if self.questions.get(index): self.questions.pop(index)
            if isinstance(child, QComboBox):
                child.clear()
                child.setEnabled(False)
            if isinstance(child, QPushButton):
                child.setEnabled(False)
            if isinstance(parent, QComboBox):
                parent.setEnabled(True)
    
    def update_combobox(self, combobox):
        _flist = os.listdir(os.path.join(*self.questions.values()))
        if _flist:
            combobox.clear()
            combobox.addItem(None)
            combobox.addItems([f for f in _flist if not f.startswith('.')])
        else:
            combobox.clear()
            
    
    def list_generate(self, parent):
        
        parent.question = dict()
        
        if self.chbox.isChecked():
            for topic in [p for p in os.walk('qbank') if p[-1]]:
               for question in topic[2]:
                   parent.question.update(os.path.join(topic, question))
    
        else:
            _questions = list()
            _fpath = os.path.join(*self.questions.values())
            for question in os.listdir(_fpath):
                if not question.startswith('.'):
                    _questions.append(os.path.join(_fpath, question))
            parent.questions.update(questions=_questions)
            
        self.close()

    
            

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = App()
    sys.exit(app.exec_())
