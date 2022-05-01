from PySide6 import QtCore, QtWidgets, QtGui 

import refactor
import sys
import random

stock = QtGui.QColor(238,238,238)
myBlue = QtGui.QColor(32,188,203)
myRed = QtGui.QColor(247,74,74)
myGreen = QtGui.QColor(89,208,87)

main_widget = None

def gui_color(to_color: str):
    lines = str.split(to_color, '\n')
    main_widget.bottom.setText("")
    for l in lines:
        if (len(l.split("GUIBLUE")) > 1):
            main_widget.bottom.setTextColor(myBlue)
            main_widget.bottom.append(l.split("GUIBLUE")[1])
        elif (len(l.split("GUIGREEN")) > 1):
            main_widget.bottom.setTextColor(myGreen)
            main_widget.bottom.append(l.split("GUIGREEN")[1])
            main_widget.bottom.append('\n')
        elif (len(l.split("GUIRED")) > 1):
            main_widget.bottom.setTextColor(myRed)
            main_widget.bottom.append(l.split("GUIRED")[1])
        else:
            main_widget.bottom.append(l)
        main_widget.bottom.setTextColor(stock)

def set_inputs_for_run():
    refactor.base_dir = main_widget.inputs.base_dir.text()
    refactor.infile_markers = []
    refactor.infile_markers.append(main_widget.inputs.search_for.text())
    refactor.new_chunk = main_widget.inputs.replace_with.text()
    refactor.filetypes = main_widget.inputs.file_types_to_search.text().split()
    refactor.ignore_markers = main_widget.inputs.dirs_to_ignore.text().split()

# Input for what to search for
class Inputs(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.base_dir = QtWidgets.QLineEdit(self)

        self.search_for = QtWidgets.QLineEdit(self)
        self.replace_with = QtWidgets.QLineEdit(self)
        self.file_types_to_search = QtWidgets.QLineEdit(self)
        self.dirs_to_ignore = QtWidgets.QLineEdit(self)

        self.column = QtWidgets.QVBoxLayout(self)

        # Active searches
        self.column.addWidget(QtWidgets.QLabel("Directory to use as root for search"))
        self.column.addWidget(self.base_dir)
        self.column.addWidget(QtWidgets.QLabel("Blob to search for in files"))
        self.column.addWidget(self.search_for)
        self.column.addWidget(QtWidgets.QLabel(
            "Blob to replace found blobs with"))
        self.column.addWidget(self.replace_with)
        self.column.addWidget(QtWidgets.QLabel(
            "Add file type to check (include the .)"))
        self.column.addWidget(self.file_types_to_search)

        # Extra settings
        self.column.addWidget(QtWidgets.QLabel("A directory to ignore in search (such as .git)"))
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
        set_inputs_for_run()
        result = refactor.get_cur_comparison(refactor.base_dir, True)
        print("Tree report")
        gui_color(result)

    @QtCore.Slot()
    def clean_report_run(self):
        set_inputs_for_run()
        result = refactor.get_cur_comparison_clean(refactor.base_dir, True)
        print("Clean report")
        gui_color(result)

    @QtCore.Slot()
    def execute_run(self):
        print("Execute")
        set_inputs_for_run()
        result = refactor.execute_replacement(refactor.base_dir)
        gui_color(result)
        main_widget.bottom.append("...Replacement complete.")


# App container
class Contain(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # Setup top section
        self.top = QtWidgets.QHBoxLayout(self)
        self.inputs = Inputs()
        self.actions = Actions()
        self.top.addWidget(self.inputs)
        self.top.addWidget(self.actions)
        topWidget = QtWidgets.QWidget()
        topWidget.setLayout(self.top)

        # Setup bottom section
        self.bottom = QtWidgets.QTextEdit(self)
        self.bottom.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.bottom.setReadOnly(True)

        # arrange both sections
        self.all = QtWidgets.QVBoxLayout(self)
        self.all.addWidget(topWidget)
        self.all.addWidget(QtWidgets.QLabel("Staged Changes"))
        self.all.addWidget(self.bottom)

        # Set texts to defaults for examples
        self.inputs.base_dir.setText(refactor.base_dir)
        self.inputs.search_for.setText(refactor.infile_markers[0])
        self.inputs.replace_with.setText(refactor.new_chunk)
        self.inputs.file_types_to_search.setText(refactor.filetypes[0])
        self.inputs.dirs_to_ignore.setText(refactor.ignore_markers[0])


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    main_widget = Contain()
    main_widget.bottom.setTextColor(myBlue)
    main_widget.bottom.append("Results will appear here")

    main_widget.resize(800, 600)
    main_widget.show()

    sys.exit(app.exec())
