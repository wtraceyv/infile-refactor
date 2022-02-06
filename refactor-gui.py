from PySide6 import QtCore, QtWidgets, QtGui
from colorama import Fore, Style, init

import refactor
import sys
import random


# Input for what to search for
class Inputs(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.search_for = QtWidgets.QLineEdit(self)
        self.replace_with = QtWidgets.QLineEdit(self)
        self.file_types_to_search = QtWidgets.QLineEdit(self)
        self.dirs_to_ignore = QtWidgets.QLineEdit(self)

        self.column = QtWidgets.QVBoxLayout(self)

        # Active searches
        self.column.addWidget(QtWidgets.QLabel("Blob to search for in files"))
        self.column.addWidget(self.search_for)
        self.column.addWidget(QtWidgets.QLabel(
            "Blob to replace found blobs with"))
        self.column.addWidget(self.replace_with)
        self.column.addWidget(QtWidgets.QLabel(
            "Add file type to check (include the .)"))
        self.column.addWidget(self.file_types_to_search)

        # Extra settings
        self.column.addWidget(QtWidgets.QLabel("Blob to search for in files"))
        self.column.addWidget(self.dirs_to_ignore)


# Buttons to run and see results, or execute
class Actions(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # Make buttons
        self.tree_report = QtWidgets.QPushButton(
            "See results in directory context", self)
        self.clean_report = QtWidgets.QPushButton(
            "See current file changes", self)
        self.execute = QtWidgets.QPushButton("Execute Changes", self)

        # Connect buttons to actions
        self.tree_report.clicked.connect(self.tree_report_run)
        self.clean_report.clicked.connect(self.clean_report_run)
        self.execute.clicked.connect(self.execute_run)

        # Add buttons to own layout
        self.column = QtWidgets.QVBoxLayout(self)
        self.column.addWidget(self.tree_report)
        self.column.addWidget(self.clean_report)
        self.column.addWidget(self.execute)

    @QtCore.Slot()
    def tree_report_run(self):
        print("Tree report")

    @QtCore.Slot()
    def clean_report_run(self):
        print("Clean report")

    @QtCore.Slot()
    def execute_run(self):
        print("Execute")


# Display outputs (in color hopefully)
class Report(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.text_block = QtWidgets.QPlainTextEdit(self)
        self.text_block.setReadOnly(True)
        self.text_block.setPlainText("Hey there. You should not be able to type here")

# App container


class Contain(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.top = QtWidgets.QHBoxLayout(self)
        self.inputs = Inputs()
        self.actions = Actions()
        self.top.addWidget(self.inputs)
        self.top.addWidget(self.actions)
        topWidget = QtWidgets.QWidget()
        topWidget.setLayout(self.top)

        self.bottom = Report()

        self.all = QtWidgets.QVBoxLayout(self)
        self.all.addWidget(topWidget)
        self.all.addWidget(self.bottom)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    widget = Contain()
    widget.resize(800, 300)
    widget.show()

    sys.exit(app.exec())
