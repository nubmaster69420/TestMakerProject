import sys
from typing import Union

from PyQt5 import uic
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QFileDialog
from PyQt5.QtWidgets import QMessageBox, QShortcut, QApplication
from pprint import pprint

# Exporting own-made functions from other files
from ExcelCSVformating import getdata
from MakeVariants import make_variants
from WordWrite import write_doxc


class MainWindow(QMainWindow):
    tasks_data: Union[None, dict, int]

    def __init__(self):
        super().__init__()
        uic.loadUi('TestMaker.ui', self)

        # Initialization of global vars
        self.quit_allow = True
        self.tasks_data = []
        self.total_variants = []
        self.save_file_path = ('', '')
        self.total_rows = 0

        # Disabling action buttons "Save" and "Save as"
        self.actionSave_as.setEnabled(False)
        self.actionSave.setEnabled(False)

        # Setting up events
        self.createButton.clicked.connect(self.make_variants)
        self.actionOpen.triggered.connect(self.get_file)
        self.actionSave_as.triggered.connect(self.save_file_as)
        self.actionSave.triggered.connect(self.save_file)

        # Setting up shortcuts
        self.quitSc = QShortcut(QKeySequence('Ctrl+R'), self)
        self.quitSc.activated.connect(self.make_variants)

        self.quitSc = QShortcut(QKeySequence('Ctrl+Q'), self)
        self.quitSc.activated.connect(self.app_quit)

    # Display a message box with an error.
    @staticmethod
    def error_window(exitcode):
        msg_box = QMessageBox()  # QMessage box class
        msg_box.setIcon(QMessageBox.Critical)  # Setting up an icon
        msg_box.setWindowTitle("Error")  # Setting up a title

        # Processing exit code and showing which error was that
        if exitcode == -1:
            msg_box.setText("Invalid format \n .xlsx .csv only")
            choice_buttons = True
        elif exitcode == -2:
            msg_box.setText("Empty file")
            choice_buttons = True
        elif exitcode == -3:
            msg_box.setText("The number of variants must be more than 0")
            choice_buttons = False
        elif exitcode == -4:
            msg_box.setText("Incorrect numbers for the tasks")
            choice_buttons = False
        elif exitcode == -5:
            msg_box.setText(
                "Please make sure that you use ',' as a delimiter and ';' as a quotechar in the CSV file"
            )
            choice_buttons = True
        else:
            return False

        if choice_buttons:
            # Adding "Ok" and "Cancel" push buttons.
            msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        else:
            # If a problem cannot be passed, the message box shows only "Ok" button.
            msg_box.setStandardButtons(QMessageBox.Ok)

        # Receiving a value which button was pressed.
        return_value: int = msg_box.exec()

        # If the pressed button is "Ok", the function returns True.
        return QMessageBox.Ok == return_value

    # Display a message box with a warning.
    @staticmethod
    def warning_window(function_warnings):
        msg_box = QMessageBox()  # QMessage box class.
        msg_box.setIcon(QMessageBox.Warning)  # Setting up an icon.

        # Setting up a title.
        # Showing user how many warnings the function has got.
        if len(function_warnings) == 1:
            msg_box.setWindowTitle("1 warning!")
        elif len(function_warnings) >= 2:
            msg_box.setWindowTitle(f"{len(function_warnings)} warnings!")

        text_warning = 'Warning!\n' + '\n'.join(function_warnings)
        msg_box.setText(text_warning)

        # Adding "Ok" and "Cancel" push buttons.
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        # Receiving a value which button was pressed.
        return_value = msg_box.exec()

        # If the pressed button is "Ok", the function returns True.
        return QMessageBox.Ok == return_value

    # Display a message box with a warning.
    @staticmethod
    def success_window():
        msg_box = QMessageBox()  # QMessage box class.
        msg_box.setIcon(QMessageBox.Information)  # Setting up an icon.

        msg_box.setWindowTitle("Success")  # Setting up a title.

        msg_box.setText("The file has been saved successfully!")

        # Adding "Ok" and "Cancel" push buttons.
        msg_box.setStandardButtons(QMessageBox.Ok)

        # Waiting until a user press "Ok"
        msg_box.exec()

    # Opening file using a path
    def open_file_from_path(self, table_name):
        tasks_file = getdata(table_name)  # Getting data from a file.

        ok_pressed = False

        if tasks_file == -1:
            ok_pressed = self.error_window(-1)  # Call of error message box with exit status -1: Invalid format.
        elif tasks_file:
            self.tasks_data = tasks_file  # Valid file format, so the function returns opened tasks.
        else:
            ok_pressed = self.error_window(-2)  # Call of error message box with exit status -2: Empty file.
        if ok_pressed:
            self.get_file()  # Repeats file opening dialog.

    # A function, which loads a dict array to QTable.
    def load_table(self, tasks_dict_data):
        if tasks_dict_data:
            self.tasksTable.clear()

            title = tasks_dict_data[0]  # Setting up a title.

            # Setting up QTable's columns
            self.tasksTable.setColumnCount(len(title))
            self.tasksTable.setHorizontalHeaderLabels(list(title.keys()))

            # Stretching a QTable.
            header = self.tasksTable.horizontalHeader()
            header.setSectionResizeMode(1)

            # Setting a row count
            self.tasksTable.setRowCount(
                len(tasks_dict_data)
            )

            # Running over the list of tasks
            for i, row in enumerate(tasks_dict_data):
                for j, elem in enumerate(row.values()):
                    # Entering values into cells
                    self.tasksTable.setItem(
                        i, j, QTableWidgetItem(str(elem))
                    )

    '''
    I didn't expect that type of data, I thought the function load_table could display this.
    I had two ways to solve this problem: 
    The first one is rewriting a function that making a list of variants
    And the second one is just writing a new function which displays data like self.total_variants
    '''

    # A function, which loads a dict of lists of dicts which contain tasks to QTable
    def load_variants_table(self, tasks_dict_data, total_rows):
        self.tasksTable.clear()
        self.tasksTable.setColumnCount(4)
        self.tasksTable.setHorizontalHeaderLabels(('номер', 'задача', 'ответ', 'вариант'))
        header = self.tasksTable.horizontalHeader()
        header.setSectionResizeMode(1)
        self.tasksTable.setRowCount(total_rows)
        for _i, row in enumerate(tasks_dict_data.keys()):
            variant_index = _i * 3
            for _index_task, elem in enumerate(tasks_dict_data[row]):
                if row == 0:
                    self.tasksTable.setItem(
                        variant_index + _index_task, 3, QTableWidgetItem('Вариант для пересдачи'))
                else:
                    self.tasksTable.setItem(
                        variant_index + _index_task, 3, QTableWidgetItem(f'{row} Вариант')
                    )

                self.tasksTable.setItem(
                    variant_index + _index_task, 0, QTableWidgetItem(f'{elem["number"]}')
                )

                self.tasksTable.setItem(
                    variant_index + _index_task, 1, QTableWidgetItem(f'{elem["task"]}')
                )

                self.tasksTable.setItem(
                    variant_index + _index_task, 2, QTableWidgetItem(f'{elem["answer"]}')
                )

    def get_file(self):
        # Opening file choosing dialog
        # Getting file path
        table_file_path = QFileDialog.getOpenFileName(
            self, 'Choose a file with tasks', 'Open File',
            'Excel file(*.xlsx);;CSV file (*.csv);;All files (*)'
        )[0]
        if table_file_path == '':
            # If user presses cancel, the path will be empty, so the program may crash
            return
        else:
            # If the path is valid, the program loads a dict from csv or excel file
            self.actionSave_as.setEnabled(True)
            self.actionSave.setEnabled(True)
            try:
                # Opening file using a path that program got
                self.open_file_from_path(table_file_path)
                self.spinBox_numVar.setValue(1)  # Setting the minimum value
                self.load_table(self.tasks_data)  # And loads a table from a dict
                # pprint(self.tasks_data) # Just to check if the data is correct
            except KeyError:
                button_ok_pressed = self.error_window(-5)
                self.tasks_data = []
                if button_ok_pressed:
                    self.get_file()
                else:
                    return

    def make_variants(self):
        retake = self.retakeButton.isChecked()
        number_of_variants = self.spinBox_numVar.value()

        if not self.tasks_data:
            pprint(self.tasks_data)
            print('Empty')
            return

        # Creating variants, also the function will return warnings if they appear:
        total_variants_and_warnings = make_variants(self.tasks_data, number_of_variants, retake)

        if total_variants_and_warnings == -1:
            self.error_window(-4)  # Sending status -3 which means incorrect number of tasks
            return

        if total_variants_and_warnings == -2:
            self.error_window(-3)  # Sending status -3 which means incorrect number of variants
            return

        # Unpacking and processing values from dict
        function_warnings = total_variants_and_warnings['warnings']  # Unpacking a tuple of warnings
        if function_warnings:
            ok_button_pressed = self.warning_window(function_warnings)
            self.actionSave_as.setEnabled(True)
            self.actionSave.setEnabled(True)
            if not ok_button_pressed:
                return

        self.total_rows = total_variants_and_warnings['total_rows']  # Unpacking a number of rows in a table

        self.total_variants = total_variants_and_warnings['tasks']  # Unpacking a list of variants also packed in dicts

        self.load_variants_table(self.total_variants, self.total_rows)  # Loading total variants to a table

    def app_quit(self):
        if self.quit_allow:
            QApplication.instance().quit()
        else:
            QMessageBox.information(
                self, 'Warning', ''
            )

    def save_file_as(self):
        self.save_file_path = QFileDialog.getSaveFileName(
            self, 'Choose a file with tasks', '',
            'Word file(*.docx);;Excel file(*.xlsx);;CSV file (*.csv)'
        )

        if self.save_file_path == ('', ''):
            return
        else:
            self.save_file()

    def save_file(self):
        if self.save_file_path == ('', ''):
            self.save_file_as()
        else:
            path, file_format = self.save_file_path
            if file_format == 'Word file(*.docx)':
                write_doxc(self.total_variants, path)

            # Showing a message box
            self.success_window()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
