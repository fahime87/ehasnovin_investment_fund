from msilib.schema import Error
from PyQt5.QtWidgets import (QWidget, QDialog,QHBoxLayout,QPushButton,QTableWidgetItem,
                             QTableWidget,QVBoxLayout,QApplication,QLabel)
from PyQt5.QtCore import pyqtSignal,QSize
from tools import FormControl,FormGroup,ComboBoxControl
from dataBase import Sql_DB
from messageBox import messageBoxDialog
from period import getperiodNamesById
from functools import partial
import mysql.connector as mc

class WalletChargeForm(QDialog):
    createNewOne=pyqtSignal(bool)
    def __init__(self,customer_id):
        super(WalletChargeForm,self).__init__()
        # setting window title
        self.setWindowTitle("Charging Wallet")
        # setting geometry to the window
        self.setGeometry(700, 150, 400, 400)
        self.formGroupBox = FormGroup()
        self.formGroupBox.groupValidation.connect(self.formValidation)
        content=getTotal(customer_id)
        self.chargePrice=FormControl('charge Price')
        self.chargePrice.required=True
        self.chargePrice.number=True
        self.formGroupBox.addControl(self.chargePrice)
        self.customer_id=customer_id

        self.buttonBox = QHBoxLayout()
        self.saveButton=QPushButton('save')
        self.saveButton.setDisabled(True)
        self.cancleButton=QPushButton('cancle')
        self.buttonBox.addWidget(self.saveButton)
        self.buttonBox.addWidget(self.cancleButton)
        self.content_lable=QLabel(F"The wallet has {content} Tooman")
        # creating a vertical layout
        mainLayout = QVBoxLayout()
        # adding form group box to the layout
        mainLayout.addWidget(self.content_lable)
        mainLayout.addWidget(self.formGroupBox)
        # adding button box to the layout
        mainLayout.addLayout(self.buttonBox)
        # setting lay out
        self.setLayout(mainLayout)
        self.saveButton.clicked.connect(self.accept)
        self.cancleButton.clicked.connect(self.reject)

    def formValidation(self, is_valid):
        if is_valid:
            self.saveButton.setEnabled(True)
        else:
            self.saveButton.setDisabled(True)
    def accept(self):
        self.saveCharging()
        self.close()
    def saveCharging(self):
        try:
            mydb =Sql_DB()
            myConnection=mydb.db_connect()
            mycursor = myConnection.cursor()
            charge_price=self.chargePrice.form_control.text()
            sql = """INSERT INTO wallet (type,customerId,amount) 
                     VALUES (%s,%s,%s)"""
            val = (True,self.customer_id,charge_price)
            mycursor.execute(sql, val)
            myConnection.commit()
            messageBoxDialog.show_info_messagebox("the wallet has been charged successfully")
            self.createNewOne.emit(True)
        except mc.Error as e:
            print(e)   
class WalletListForInvestor(QWidget)   :
    update_tabel=pyqtSignal(bool)
    def __init__(self,investor_id):
        super().__init__()
        self.setMinimumSize(QSize(400, 700))
        self.setWindowTitle("Content of This Wallet")
        self.superLayout=QVBoxLayout(self)
        charge_wal_btn=QPushButton("Charge this wallet")
        charge_wal_btn.clicked.connect(partial(self.chargeWallet,investor_id))
        trns_wal_btn=QPushButton("Transfer the content of wallet")
        trns_wal_btn.clicked.connect(partial(self.transferWalletContent,investor_id))
        self.button_layout=QHBoxLayout()
        self.button_layout.addWidget(charge_wal_btn)
        self.button_layout.addWidget(trns_wal_btn)
        self.wallet_table=self.walletTable(investor_id)
        self.superLayout.addLayout(self.button_layout)
        self.superLayout.addWidget(self.wallet_table)
    def chargeWallet(self,inv_id):
        form=WalletChargeForm(inv_id)
        form.createNewOne.connect(partial(self.updateTable,inv_id))
        form.exec_()
    def transferWalletContent(self,inv_id):
        form=WalletTransitionForm(inv_id)
        form.createNewOne.connect(partial(self.updateTable,inv_id))
        form.exec_()
    def updateTable(self,investor_id):
        data=self.getWallets(investor_id)      
        table=self.wallet_table
        table.setColumnCount(4)
        table.setRowCount(len(data))
        table.setMinimumWidth(1000)
        table.setMinimumHeight(500)
        table.setHorizontalHeaderLabels(["Date","Amount","Type","content"])
        content=0
        for n,rec in enumerate(data):
                date_item=QTableWidgetItem(str(rec[0]))
                amount_item=QTableWidgetItem(str(rec[1]))
                type="charged" if rec[2] else "Dischared"
                type_item=QTableWidgetItem(type)
                content=content+rec[1] if rec[2] else content-rec[1] 
                content_item=QTableWidgetItem(str(content))
                table.setItem(n,0,date_item)
                table.setItem(n,1,amount_item)
                table.setItem(n,2,type_item)
                table.setItem(n,3,content_item)
        table.resizeColumnsToContents()
        table.resizeRowsToContents()     
    def walletTable(self,investor_id):
        data=self.getWallets(investor_id)      
        table=QTableWidget()
        table.setColumnCount(4)
        table.setRowCount(len(data))
        table.setMinimumWidth(1000)
        table.setMinimumHeight(500)
        table.setHorizontalHeaderLabels(["Date","Amount","Type","content"])
        content=0
        for n,rec in enumerate(data):
                date_item=QTableWidgetItem(str(rec[0]))
                amount_item=QTableWidgetItem(str(rec[1]))
                type="charged" if rec[2] else "Dischared"
                type_item=QTableWidgetItem(type)
                content=content+rec[1] if rec[2] else content-rec[1] 
                content_item=QTableWidgetItem(str(content))
                table.setItem(n,0,date_item)
                table.setItem(n,1,amount_item)
                table.setItem(n,2,type_item)
                table.setItem(n,3,content_item)
        table.resizeColumnsToContents()
        table.resizeRowsToContents()     
        return table
    def getWallets(self,inv_id):
        try:
            connection=Sql_DB().db_connect()
            my_cursor=connection.cursor()
            wallet_query=F"""SELECT createDate,
                            amount,type
                            FROM wallet
                            WHERE customerId='{inv_id}'
                            """
            my_cursor.execute(wallet_query)
            wallet_content=my_cursor.fetchall()
            return wallet_content
        except mc.Error as e:
            messageBoxDialog.show_critical_messagebox(F"{e}")                                 
class WalletTransitionForm(QDialog):
    createNewOne=pyqtSignal(bool)
    def __init__(self,customer_id):
        super(WalletTransitionForm,self).__init__()
        # setting window title
        self.setWindowTitle("Wallet Content Transition")
        # setting geometry to the window
        self.setGeometry(700, 150, 400, 400)
        self.formGroupBox = FormGroup()
        self.formGroupBox.groupValidation.connect(self.formValidation)
        self.customer_id=customer_id
        content=getTotal(customer_id)
        self.transition_amount=FormControl('Transition Amount')
        self.transition_amount.required=True
        self.transition_amount.number=True
        self.transition_amount.range(0,content)

        self.periodNameDict,temp=getperiodNamesById()
        self.target_period=ComboBoxControl(self,list(self.periodNameDict.keys()),"Target Period")
        self.target_period.required=True

        self.formGroupBox.addControl(self.transition_amount)
        self.buttonBox = QHBoxLayout()
        self.saveButton=QPushButton('save')
        self.saveButton.setDisabled(True)
        self.cancleButton=QPushButton('cancle')
        self.buttonBox.addWidget(self.saveButton)
        self.buttonBox.addWidget(self.cancleButton)
        self.content_lable=QLabel(F"The wallet has {content} Tooman")
        # creating a vertical layout
        mainLayout = QVBoxLayout()
        # adding form group box to the layout
        mainLayout.addWidget(self.content_lable)
        mainLayout.addWidget(self.target_period)
        mainLayout.addWidget(self.formGroupBox)
        # adding button box to the layout
        mainLayout.addLayout(self.buttonBox)
        # setting lay out
        self.setLayout(mainLayout)
        self.saveButton.clicked.connect(self.accept)
        self.cancleButton.clicked.connect(self.reject)

    def formValidation(self, is_valid):
        if is_valid:
            self.saveButton.setEnabled(True)
        else:
            self.saveButton.setDisabled(True)
    def accept(self):
        self.saveTransition()
        self.close()
    def saveTransition(self):
        try:
            mydb =Sql_DB()
            myConnection=mydb.db_connect()
            mycursor = myConnection.cursor()

            amount=int(self.transition_amount.form_control.text())
            target_period=self.periodNameDict.get(self.target_period.form_control.currentText())
            
            discharge_sql = """INSERT INTO wallet (type,customerId,amount) 
                     VALUES (%s,%s,%s)"""
            val = (False,self.customer_id,amount)
            mycursor.execute(discharge_sql, val)
            myConnection.commit()
            check_query=F"""SELECT Id,Amount 
                           FROM payments
                           WHERE CustomerId='{self.customer_id}' and PeriodId='{target_period}'"""
            mycursor.execute(check_query)
            isExist=mycursor.fetchone()
            if isExist:
                update_query=F"""UPDATE payments set amount='{isExist[1]+amount}' 
                                WHERE Id='{isExist[0]}'"""
                mycursor.execute(update_query)
                myConnection.commit()    
                messageBoxDialog.show_info_messagebox("the money has been transmited to payment successfully")            
                return
            payment_sql=""" INSERT INTO payments (status,customerId,PeriodId,amount) VALUES (%s,%s,%s,%s)"""
            val=(1,self.customer_id,target_period,amount)
            mycursor.execute(payment_sql,val)
            myConnection.commit()
            messageBoxDialog.show_info_messagebox("the money has been transmited successfully")
            self.createNewOne.emit(True)
        except mc.Error as e:
            messageBoxDialog.show_critical_messagebox(f"{e}")
class WalletList(QWidget):
    update_tabel=pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(400, 700))
        self.setWindowTitle("List Of Wallets")
        self.superLayout=QVBoxLayout(self)
        self.wallet_table=self.walletTable()
        self.superLayout.addWidget(self.wallet_table)

    def updateTable(self):
        print("")
    def walletTable(self):
        data=self.getWallets()      
        table=QTableWidget()
        table.setColumnCount(2)
        table.setRowCount(len(data))
        table.setMinimumWidth(1000)
        table.setMinimumHeight(500)
        table.setHorizontalHeaderLabels(["customer","content"])
        n=0
        for key in data:
                tableItem=QTableWidgetItem(str(key))
                tableItem1=QTableWidgetItem(str(data[key]))
                table.setItem(n,0,tableItem)
                table.setItem(n,1,tableItem1)
                n+=1
        table.resizeColumnsToContents()
        table.resizeRowsToContents()     
        return table
    def getWallets(self):
        try:
            print("")
            connection=Sql_DB().db_connect()
            my_cursor=connection.cursor()
            wallet_query="""SELECT content,
                            TYPE , customerId, name, family
                            FROM customers
                            JOIN (

                            SELECT SUM( amount ) AS content,
                            TYPE , customerId
                            FROM wallet
                            GROUP BY customerId,
                            TYPE
                            )W ON customers.id = W.customerId"""
            my_cursor.execute(wallet_query)
            wallets=my_cursor.fetchall()
            wal_dic={}
            for rec in wallets:
                if not wal_dic.get(F"{rec[3]} {rec[4]} ({rec[2]})"):
                    wal_dic[F"{rec[3]} {rec[4]} ({rec[2]})"]=0
                if rec[1]:#type of wallet record is charged
                    wal_dic[F"{rec[3]} {rec[4]} ({rec[2]})"]+=rec[0]
                else: #type of wallet record is discharged
                    wal_dic[F"{rec[3]} {rec[4]} ({rec[2]})"]-=rec[0]
            return wal_dic

        except mc.Error as e:
            messageBoxDialog.show_critical_messagebox(F"{e}")          
def getTotal(customer_id):
    total_charge=0
    total_discharge=0
    try:
        connection=Sql_DB().db_connect()
        mycursor=connection.cursor()
        query=F"""SELECT SUM(amount),Type   
        FROM wallet   
        WHERE customerId='{customer_id}'         
        GROUP BY Type
        """
        mycursor.execute(query)
        res=mycursor.fetchall()
        for rec in res:
            if rec[1]:
               total_charge=rec[0]
            else:
                total_discharge=rec[0]
        wallet_content=total_charge-total_discharge
        return wallet_content
    except mc.Error as e:
        messageBoxDialog.show_critical_messagebox(f"{e}") 

if __name__=="__main__":
    import sys
    app=QApplication(sys.argv)
    #ui=WalletList()
    ui=WalletTransitionForm(1001)
    ui.show()
    sys.exit(app.exec_())
