import sys
from PyQt5.QtCore import pyqtSignal, QRegularExpression
from PyQt5.QtWidgets import ( QLabel, QLineEdit,
                             QHBoxLayout, QVBoxLayout, QWidget,QTableWidget,QTableWidgetItem,QComboBox)

class FormGroup(QWidget):
    groupValidation = pyqtSignal(bool)
    def __init__(self, orientation='vertical'):
        super().__init__()

        self.form_controls = []        
        self.main_layout = QVBoxLayout() if orientation == 'vertical' else QHBoxLayout()
        self.setLayout(self.main_layout)
        
    def addControl(self, control):
        if not isinstance(self, FormControl):
            self.form_controls.append(control)
            self.main_layout.addWidget(control)
            control.inputValidation.connect(self.validateGroup)
        else:
            raise ValueError('could not add object of type {}'.format(type(control)))
            

    def validateGroup(self, _):
        for control in self.form_controls:
            if not control.valid:
                self.groupValidation.emit(False)
                return
        
        self.groupValidation.emit(True)

class FormControl(QWidget):
    inputValidation = pyqtSignal(bool)
    def __init__(self, title=''):
        super().__init__()

        control_layout = QVBoxLayout()

        self.form_label = QLabel()
        self.form_control = QLineEdit()
        self.validation_label = QLabel()
        self.validation_label.setStyleSheet('color: red')
        
        control_layout.addWidget(self.form_label)
        control_layout.addWidget(self.form_control)
        control_layout.addWidget(self.validation_label)
        control_layout.addStretch(1)

        self.setLayout(control_layout)

        self.title = title
        self.required = False
        self.required_error_message = '{} is required.'

        self.email = False
        self.email_error_message = 'The value should be an email.'
        self.email_regex = QRegularExpression("\\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,4}\\b",
                          QRegularExpression.CaseInsensitiveOption)

        self.number = False
        self.number_error_message = '{} should be a number.'
        self._minimum = None
        self.min_error_message = '{} should be higher than {}.'
        self._maximum = None
        self.max_error_message = '{} should be lower than {}.'
        self.Lenght=None
        self.Lenght_error_message='{} lenght should be equial to {}'
        
        
        self.valid = False

        self.form_control.textChanged.connect(self.validate)

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, title):
        self._title = title
        self.form_label.setText('{}:'.format(self._title))
    
    @property
    def maximum(self):
        return self._maximum
    
    @maximum.setter
    def maximum(self, value):
        self._maximum = value
        self.number = True
    
    @property
    def minimum(self):
        return self._minimum
    
    @minimum.setter
    def minimum(self, value):
        self._minimum = value
        self.number = True
    
    def range(self, minimum, maximum):
        self._minimum = minimum
        self._maximum = maximum
        self.number = True

    def validate(self, input_text):
        text = input_text.strip()
        if self.required and not text:
            self.onInvalid(self.required_error_message.format(self.title))
            return
        if self.email and not self.email_regex.match(text).hasMatch():
            self.onInvalid(self.email_error_message)
            return
        if self.number:
            value, ok = self.isNumber(text)
            if not ok:              
                self.onInvalid(self.number_error_message.format(self.title))
                return
            if self._maximum is not None and value > self._maximum:
                self.onInvalid(self.max_error_message.format(self.title, self._maximum))
                return
            if self._minimum is not None and value < self._minimum:
                self.onInvalid(self.min_error_message.format(self.title, self._minimum))
                return
        if self.Lenght and not    len(text)==self.Lenght:
            self.onInvalid(self.Lenght_error_message.format(self.title,self.Lenght))
            return        
        self.onValid()

    def onValid(self):
        self.form_control.setStyleSheet('')
        self.validation_label.setText('')
        self.valid = True
        self.inputValidation.emit(True)

    def onInvalid(self, error_message):
        self.form_control.setStyleSheet('border: 1px solid red;')
        self.validation_label.setText(error_message)
        self.valid = False
        self.inputValidation.emit(False)
    
    def isNumber(self, value):
        try:
            return float(value), True
        except ValueError:
            return None, False

class ComboBoxControl(QWidget):
    inputValidation = pyqtSignal(bool)
    changeValue=pyqtSignal(bool)
    def __init__(self, source,items,title='',):
        super().__init__()

        control_layout = QVBoxLayout()

        self.form_label = QLabel()
        self.form_control = QComboBox(source)
        self.form_control.addItems(items)
        self.validation_label = QLabel()
        self.validation_label.setStyleSheet('color: red')
        
        control_layout.addWidget(self.form_label)
        control_layout.addWidget(self.form_control)
        control_layout.addWidget(self.validation_label)
        control_layout.addStretch(1)

        self.setLayout(control_layout)

        self.title = title
        self.required = False
        self.required_error_message = '{} is required.'

        self.valid = False

        self.form_control.activated[str].connect(self.validate)

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, title):
        self._title = title
        self.form_label.setText('{}:'.format(self._title))
    


    def validate(self, input_text):
        text = input_text.strip()
        if text:
            self.changeValue.emit(True)
        else:
            self.changeValue.emit(False)    
        if self.required and not text:
            self.onInvalid(self.required_error_message.format(self.title))
            return
        self.onValid()

    def onValid(self):
        self.form_control.setStyleSheet('')
        self.validation_label.setText('')
        self.valid = True
        self.inputValidation.emit(True)

    def onInvalid(self, error_message):
        self.form_control.setStyleSheet('border: 1px solid red;')
        self.validation_label.setText(error_message)
        self.valid = False
        self.inputValidation.emit(False)
    
class CreateTable(QTableWidget):
    def __init__(self,header,data,*args):
        super().__init__()
        self.setColumnCount(len(header))
        self.setRowCount(len(data))
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)
        self.setHorizontalHeaderLabels(header)
        self.setData(data)

    def setData(self,tableData):  
        for n,row in enumerate(tableData):
            for m,item in enumerate(row):
                tableItem=QTableWidgetItem(str(item))
                self.setItem(n,m,tableItem)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()        


