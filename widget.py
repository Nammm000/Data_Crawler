from tkinter import Label
from PySide6.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QTextEdit, QSizePolicy,  QRadioButton, QGroupBox
class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Data Crawler")
        self.text_edit = QTextEdit()

        answers = QGroupBox("Choose Answer")
        answer_a = QRadioButton("A")
        answer_b = QRadioButton("B")
        answer_c = QRadioButton("C")
        answer_a.setChecked(True)

        answers_layout = QHBoxLayout()
        answers_layout.addWidget(answer_a)
        answers_layout.addWidget(answer_b)
        answers_layout.addWidget(answer_c)
        answers.setLayout(answers_layout)

        #A set of signals we can connect to
        label = QLabel("Link : ")
        self.line_edit = QLineEdit()
        
        self.line_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.line_edit.returnPressed.connect(self.button_clicked)
        #self.line_edit.selectionChanged.connect(self.selection_changed)
        self.line_edit.textEdited.connect(self.text_edited)


        button = QPushButton("Grab data")
        button.clicked.connect(self.button_clicked)

        h_layout = QHBoxLayout()
        h_layout.addWidget(label)
        h_layout.addWidget(self.line_edit)

        v_layout = QVBoxLayout()
        v_layout.addWidget(answers)
        v_layout.addLayout(h_layout)
        v_layout.addWidget(button)
        v_layout.addWidget(self.text_edit)


        self.setLayout(v_layout)

    #Slots
    def button_clicked(self):
        self.text_edit.setPlainText(self.line_edit.text() + " AM HERE")


    def cursor_position_changed(self,old,new):
        print("cursor old position : ", old, " -new position : ",new)

    def editing_finished(self) : 
        print("Editing finished")

    def return_pressed(self):
        print("Return pressed")

    def selection_changed(self):
        print("Selection Changed : ", self.line_edit.selectedText())

    def text_edited(self,new_text) : 
        print("Text edited. New text : ", new_text)