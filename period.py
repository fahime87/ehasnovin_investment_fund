from msilib.schema import Error
import re
from PyQt5.QtWidgets import QDialog,QVBoxLayout,QHBoxLayout,QPushButton,QWidget,QTableWidget,QTableWidgetItem
from PyQt5 import QtWidgets
from tools import ComboBoxControl,FormGroup,FormControl
from dataBase import Sql_DB
from messageBox import messageBoxDialog
import mysql.connector as mc
from PyQt5.QtCore import QSize,pyqtSignal
from functools import partial

class PeriodForm(QDialog):
    createNewOne=pyqtSignal(bool)
    def __init__(self):
        super(PeriodForm,self).__init__()
        # setting window title
        self.setWindowTitle("Asset Period Form")
  
        # setting geometry to the window
        self.setGeometry(700, 300, 400, 400)
 
        self.formGroupBox = FormGroup()
        self.formGroupBox.groupValidation.connect(self.formValidation)

        self.name=FormControl("Name")
        self.name.form_control.setText('period_name')
        #self.name.form_control.setStyleSheet("background-color: yellow")
        self.name.form_control.setEnabled(False)

        self.year=ComboBoxControl(self,[None,'1400','1401','1402','1403','1404','1405'],"year")
        self.year.required=True
        self.year.changeValue.connect(self.periodName)

        self.month=ComboBoxControl(self,[None,'farvardin','ordibehesht','khrdad','Tir','mordad','sharivar','mehr','aban','azar','day','bahman','esfand'],"Month")
        self.month.required=True
        self.month.changeValue.connect(self.periodName)

        self.formGroupBox.addControl(self.name)
        self.formGroupBox.addControl(self.year)
        self.formGroupBox.addControl(self.month)

        self.buttonBox = QHBoxLayout()
        self.saveButton=QPushButton('save')
        self.saveButton.setDisabled(True)
        self.cancleButton=QPushButton('cancle')
        self.buttonBox.addWidget(self.saveButton)
        self.buttonBox.addWidget(self.cancleButton)
    
        # creating a vertical layout
        mainLayout = QVBoxLayout()
        # adding form group box to the layout
        mainLayout.addWidget(self.formGroupBox)
        # adding button box to the layout
        mainLayout.addLayout(self.buttonBox)
        # setting lay out
        self.setLayout(mainLayout)
        #self.retranslateUi(userCreator)
        self.saveButton.clicked.connect(self.accept)
        self.cancleButton.clicked.connect(self.reject)

    def formValidation(self, is_valid):
        if is_valid:
            self.saveButton.setEnabled(True)
        else:
            self.saveButton.setDisabled(True)
    def accept(self):
        self.savePeriod()
        self.close()
    def savePeriod(self):
        try:
            mydb =Sql_DB()
            myConnection=mydb.db_connect()
            mycursor = myConnection.cursor()
 
            name=self.name.form_control.text()  
            year=self.year.form_control.currentText()
            month=self.month.form_control.currentIndex()
            sql = "INSERT INTO assetperiod (Name,Year,Month) VALUES (%s, %s,%s)"
            val = (name,year,month)
            mycursor.execute(sql, val)
            myConnection.commit()
            self.createNewOne.emit(True)
            messageBoxDialog.show_info_messagebox("created successfully")
        except mc.Error as e:
            print(e)
            #self.show_info_messagebox(e)            
    def periodName(self,is_valid):
        if is_valid:
            year=self.year.form_control.currentText()
            month=self.month.form_control.currentText()
            self.name.form_control.setText(year+"_"+month)
            self.name.form_control.setStyleSheet("background-color: yellow")
class PeriodList(QWidget):
    update_tabel=pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(400, 700))
        self.setWindowTitle("List of Ehsan Novin Periods")
        self.superLayout=QVBoxLayout(self)
        
        self.create_new_period=QPushButton("Create New Period")
        self.period_table=self.periodTable()
        self.create_new_period.clicked.connect(self.periodForm)
        
         # Display the table and pushbutton
        self.superLayout.addWidget(self.create_new_period)
        self.superLayout.addWidget(self.period_table)

    def periodForm(self): 
        ui=PeriodForm()
        ui.createNewOne.connect(self.updateTable)
        ui.exec_()  
    def updateTable(self):
        header,data=self.getPeriods()      
        self.period_table.setColumnCount(len(header))
        self.period_table.setRowCount(len(data))
        self.period_table.setHorizontalHeaderLabels(header)
        for n,row in enumerate(data):
            for m,item in enumerate(row):
                tableItem=QTableWidgetItem(str(item))
                self.period_table.setItem(n,m,tableItem)
                rmv_btn=QPushButton("remove period") 
                rmv_btn.clicked.connect(partial(self.removePeriod,row[0]))
                finalize_btn=QPushButton("finalize")
                finalize_btn.clicked.connect(partial(self.checkPeriod,row[0]))
                self.period_table.setCellWidget(n,5, rmv_btn)
                self.period_table.setCellWidget(n,6,finalize_btn)
    def periodTable(self):
        header,data=self.getPeriods()      
        table=QTableWidget()
        table.setColumnCount(len(header))
        table.setRowCount(len(data))
        table.setMinimumWidth(1000)
        table.setMinimumHeight(500)
        table.setHorizontalHeaderLabels(header)
        for n,row in enumerate(data):
            for m,item in enumerate(row):
                tableItem=QTableWidgetItem(str(item))
                table.setItem(n,m,tableItem)
                rmv_btn=QPushButton("remove period") 
                rmv_btn.clicked.connect(partial(self.removePeriod,row[0]))
                finalize_btn=QPushButton("finalize")
                finalize_btn.clicked.connect(partial(self.checkPeriod,row[0]))
                table.setCellWidget(n,5, rmv_btn)
                table.setCellWidget(n,6,finalize_btn)
        table.resizeColumnsToContents()
        table.resizeRowsToContents()     
        return table  

    def checkPeriod(self,period_id):
        try:
            db=Sql_DB()
            connection=db.db_connect()
            mycursor=connection.cursor()
            payment_query=F"""SELECT SUM(amount) FROM payments WHERE periodId='{period_id}'"""
            mycursor.execute(payment_query)
            sum_payments=mycursor.fetchone()[0]
            investment_query=F"""SELECT SUM(shareInvestment) FROM assets WHERE periodId='{period_id}'"""
            mycursor.execute(investment_query)
            sum_inv=mycursor.fetchone()[0]
            if sum_inv==sum_payments :
                finalize_query=F"""UPDATE assetperiod 
                                   SET status=1
                                   WHERE id='{period_id}'"""
                mycursor.execute(finalize_query)
                connection.commit()                   
                messageBoxDialog.show_info_messagebox(F"you finalize the periodsuccesfully")
            elif sum_inv>sum_payments:
                messageBoxDialog.show_critical_messagebox("the assets you buy for this period is more than investor payment")
            elif sum_payments>sum_inv:
                messageBoxDialog.show_critical_messagebox("the investors payments is more than assets you buy")
        except mc.Error as e:  
            messageBoxDialog.show_critical_messagebox(F"{e}")
    def getPeriods(self):
        try:      
                mydb=Sql_DB()
                myConnection=mydb.db_connect()
                myCursor=myConnection.cursor()

                #header of table
                myColumnQuery="""SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = N'assetperiod'"""
                myCursor.execute(myColumnQuery)
                columnName=myCursor.fetchall()
                #print(columnName)
                header=list(map(lambda x:x[0],columnName))
                header.append("")
                header.append("")
                #data of table

                myDataQuery="SELECT * FROM assetperiod"
                myCursor.execute(myDataQuery)
                data=myCursor.fetchall()
                #print(data)
                return header,data

        except mc.Error as e:
                messageBoxDialog.show_critical_messagebox("{0} :geting periods from db was not successfully".format(e))
    def removePeriod(self,period_id):
        try:
            mydb=Sql_DB()
            myconnection=mydb.db_connect()
            mycursor=myconnection.cursor()
            checkquery=F"SELECT status FROM assetperiod WHERE Id='{period_id}'"
            mycursor.execute(checkquery)
            period_status=mycursor.fetchone()[0]
            if not(period_status):
                query=F"DELETE FROM assetperiod WHERE Id='{period_id}'"
                mycursor.execute(query)
                myconnection.commit()
                messageBoxDialog.show_info_messagebox("Deleting Period Was Successfully")
            else:
                messageBoxDialog.show_critical_messagebox("The Finalized Period Cant Be Deleted!")    
        except mc.Error as e:
            messageBoxDialog.show_critical_messagebox(F"{e}:deleting Period was not successfully")                
def getTotalPayment(period_id): 
    try:
        db=Sql_DB()
        connection=db.db_connect()
        mycursor=connection.cursor()
        payment_query=F"""SELECT SUM(amount) FROM payments WHERE periodId='{period_id}'"""
        mycursor.execute(payment_query)
        total_payments=mycursor.fetchone()[0]
        return total_payments
    except mc.Error as e:
        messageBoxDialog.show_critical_messagebox(f"{e}")     
def getCurrentPeriod():
    try:
        print ("")
        connection=Sql_DB().db_connect()
        mycursor=connection.cursor()
        query="""SELECT id
               FROM  assetperiod
               ORDER BY year,month
               WHERE status=0
               LIMIT 0,1"""
        mycursor.execute(query)
        current_period_id=mycursor.fetchone()[0]
        return current_period_id       
    except mc.Error as e:
        messageBoxDialog.show_critical_messagebox(f"{e}")                                
def getperiodNamesById():
        mydb=Sql_DB()
        myConnection=mydb.db_connect()
        myCursor=myConnection.cursor()
        query="SELECT Name,Id FROM assetPeriod"
        myCursor.execute(query)
        periodNames=myCursor.fetchall()
        id_dict_by_name=dict(periodNames)
        name_dict_by_id={key:value for value,key in periodNames}          
        return id_dict_by_name,name_dict_by_id
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = PeriodList()
    #ui=PeriodForm()
    ui.show()
    sys.exit(app.exec_())
