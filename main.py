from fbs_runtime.application_context.PyQt6 import ApplicationContext
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication, 
    QFileDialog,
    QMainWindow, 
    QPushButton, 
    QComboBox, 
    QLabel,
    QGridLayout, 
    QVBoxLayout, 
    QWidget, 
    QLineEdit,
    QTabWidget
)
import polars as pl
import os
from os.path import isfile, join, realpath
import duckdb
import re
from datetime import datetime
import sys

class DesktopDB(QWidget):
    def __init__(self):
        super().__init__()
        self.file_paths = []
        self.fld = ''

        self.setWindowTitle('DesktopDB')
        self.resize(500, 350)

        layout = QGridLayout()
        self.setLayout(layout)

        ## Widgets
        # Selection Buttons
        directory_button = QPushButton('Select Database Directory', clicked=self.directory_select)
        flat_file_button = QPushButton('Select Flat File(s)', clicked=self.file_select)
        
        # Input Field
        input_label = QLabel('Enter Desired Database Name:')
        self.inputField = QLineEdit()

        # Combo Box
        self.cb = QComboBox()
        self.options = ('Create Single New Table from File(s)', 'Create New Table per File', 'Append File(s) to Existing Table')
        self.cb.addItems(self.options)
        self.cb.currentIndexChanged.connect(self.selection_change)
		
        # Workflow Buttons
        execute_workflow_button = QPushButton('Execute Workflow', clicked=self.run_workflow)

        ## Layout Structure
        # Selection Button Layout
        layout.addWidget(directory_button, 0, 0, 1, 3)
        layout.addWidget(flat_file_button, 1, 0, 1, 3)
        # Input Field Layout
        layout.addWidget(input_label, 2, 0, 1,1)
        layout.addWidget(self.inputField, 2, 1, 1, 2)
        # Combo Box Layout
        layout.addWidget(self.cb, 3, 0, 1, 3)
        # Workflow Button Layout
        layout.addWidget(execute_workflow_button, 4, 0, 1, 3)

    # Combo Box Selection Change
    def selection_change(self, i):
        print("Items in the list are :")
		
        for count in range(self.cb.count()):
            print(self.cb.itemText(count))
        print("Current index", i,"selection changed ", self.cb.currentText())

	# Select the File Directory
    def directory_select(self):
        fld = QFileDialog.getExistingDirectory(
            self,
            caption = 'Select Database Directory'
        )
        self.fld = fld
        return self.fld

    def file_select(self):
        files = QFileDialog.getOpenFileNames(
            parent=self,
            caption = 'Select File(s)',
            directory=os.getcwd(),
            filter = 'Data File (*.xlsx *.csv *.txt);; Excel File (*.xlsx)',
            initialFilter='Data File (*.xlsx *.csv *.txt)'
        )
        self.file_paths = files[0]
        return self.file_paths
    
    def run_workflow(self):
        input_text = self.inputField.text()
        combo_selection = self.cb.currentText()

        # Check if inputted table name has extension
        if input_text.endswith('.parquet'):
            tbl_name = input_text
        elif not input_text.endswith('.parquet'):
            tbl_name = f"{input_text}.parquet"

            # Determine file type to import
            def file_type(f):
                if os.path.splitext(f)[1] == '.xlsx':
                    df = pl.read_excel(f)
                elif os.path.splitext(f)[1] in ['.csv', '.txt']:
                    df = pl.read_csv(f)
                return df
            
            # Helpder Function to Concatenate Files - Called as Needed
            def file_concat():
                if len(self.file_paths) > 1:
                    dfo = pl.DataFrame()
                    for f in self.file_paths:
                        df = file_type(f)
                        dfo = pl.concat([dfo, df], how = 'diagonal')
                elif len(self.file_paths) == 1:
                    dfo = file_type(self.file_paths[0])
                return dfo
            
            # Evaluate Drop Down Options
            if combo_selection == 'Create Single New Table from File(s)':
                df = file_concat()
                df.write_parquet(f"{self.fld}/{tbl_name}", compression = 'zstd')
            
            elif combo_selection == 'Create New Table per File':
                for f in self.file_paths:
                    df = file_type(f)
                    df.write_parquet(f"{self.fld}/{os.path.splitext(os.path.basename(f))[0]}.parquet")

            elif combo_selection == 'Append File(s) to Existing Table':
                pfile = QFileDialog.getOpenFileName(
                    parent=self,
                    caption = 'Select Parquet File to Append To',
                    directory=os.getcwd(),
                    filter = 'Data File (*.parquet)',
                    initialFilter= 'Data File (*.parquet)'
                )
                
                df = file_concat()
                dfp = pl.read_parquet(pfile[0])
                dfp = pl.concat([dfp, df],  how = 'diagonal')
                dfp.write_parquet(pfile)
                print(pfile)

import sys

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    
    app = QApplication([])
    app.setStyleSheet(
        '''
        QWidget{
            font-size: 20px;
        }

        QPushButton{
            font-size: 20px;
        }
        '''
    )

    DesktopDB = DesktopDB()
    DesktopDB.show()
    
    
    exit_code = appctxt.app.exec()      # 2. Invoke appctxt.app.exec()
    sys.exit(exit_code)