"""Determininant calculator GUI."""

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QGridLayout, QTextEdit,QPushButton
from PyQt5.uic import loadUi
import numpy as np
from math import sqrt

class SetMatrix(QDialog):
    def __init__(self):
        super(SetMatrix,self).__init__()
        loadUi("first_window.ui",self) # load first window

        self.setMatrixButton.clicked.connect(self.goSecondWindow)

    def goSecondWindow(self):
        dimension=self.selectDomainBox.currentText() 
        second_window=InputValues(int(dimension)) 
        widget.addWidget(second_window)
        widget.setCurrentIndex(widget.currentIndex()+1)

class InputValues(QDialog): # second window
    def __init__(self,dimension):
        super(InputValues,self).__init__()
        loadUi("second_window.ui",self)

        self.initGrid(dimension)
        self.calculateButton.clicked.connect(self.checkInput)
        
        # create matrix 
    def initGrid(self,dimension):
        grid = QGridLayout()
        self.setLayout(grid)
        
        # add rows columns ("cells")     
        cells_pos = [(i,j) for i in range (dimension) for j in range (dimension)]
        self.cells = []
        for cell_pos in cells_pos:
            
            cell_content=QTextEdit()
            # stylizing content of the cell
            cell_content.setStyleSheet(
            	"""QTextEdit {background-color: rgb(255,255,255);
            				  font: 15pt;
            				  font-family: Courier;}""")

            grid.addWidget(cell_content,*cell_pos) 
            self.cells.append(cell_content)

        # place calculate button
        grid.addWidget(self.calculateButton) 

    def checkInput(self):
        # function getContent serve two things: it gets 
        try: 
            self.getContent()
            self.reshapeCells()
            self.goThirdWindow()

        except:
            print("Matrix has to be fully filled with only integers")
        	
    def reshapeCells(self):
        dimensions = int(sqrt(len(self.cells)) ) #! why I have to calculate it when I know already have the value
        self.cells = np.array(self.cells).reshape(dimensions,dimensions)

    def getContent(self): # get text from cells
        self.cells = [int(cell.toPlainText()) for cell in self.cells]

    def goThirdWindow(self):
        third_window=Solution(self.cells)
        widget.addWidget(third_window)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
class Solution(QDialog):
    def __init__(self,cells):
        super(Solution,self).__init__()
        loadUi("third_window.ui",self)

        # calculate
        solution = int(np.linalg.det(cells))
        # output solution
        self.outputLabel.setText(str(solution))
        # new calculation
        self.newMatrixButton.clicked.connect(self.goFirstWindow)
        
    def goFirstWindow(self):
        first_window=SetMatrix()
        widget.addWidget(first_window)
        widget.setCurrentIndex(widget.currentIndex()+1) 

app=QApplication(sys.argv)
mainwindow=SetMatrix()
widget=QtWidgets.QStackedWidget()
widget.setWindowTitle("Determinant calculator")
widget.addWidget(mainwindow)
widget.setMinimumWidth(500)
widget.setMinimumHeight(500)
widget.show()
app.exec_()        