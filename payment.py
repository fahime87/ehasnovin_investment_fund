from turtle import width
from PyQt5.QtWidgets import (QDialog,QWidget,QHBoxLayout,QMenu,
QVBoxLayout,QPushButton,QTableWidget,QTableWidgetItem,QApplication,QFrame,QLabel,QCheckBox,QRadioButton)
from tools import  ComboBoxControl,FormGroup,FormControl
import period
from messageBox import messageBoxDialog
from dataBase import Sql_DB
import mysql.connector as mc
from PyQt5.QtCore import pyqtSignal ,QSize,Qt,QRect,QVariant
from functools import partial
from sqlalchemy import null
from PyQt5.QtGui import QColor,QCursor
import ehsanStyle 


class PaymentForm(QDialog):
    createNewOne=pyqtSignal(bool)
    def __init__(self,customerId):
        super(PaymentForm,self).__init__()
         # setting window title
        investor_info=getInvestorInfo(customerId) 
        self.setWindowTitle(F"Payment  Form For {investor_info.get('name')} {investor_info.get('family')}")
        # setting geometry to the window
        self.setGeometry(700, 150, 400, 400)
        
        self.customerId=customerId
        
        self.formGroupBox = FormGroup()
        self.formGroupBox.groupValidation.connect(self.formValidation)

        self.periodNameDict,temp=period.getperiodNamesById()
        self.period=ComboBoxControl(self,list(self.periodNameDict.keys()),"Payment Period")
        self.period.required=True

        self.amount=FormControl('Amount')
        self.amount.required=True
        self.amount.number=True

        self.payment_status=ComboBoxControl(self,[None,'final','reserved'],"payment status")
        self.payment_status.required=True

        #self.formGroupBox.addControl(self.date)
        self.formGroupBox.addControl(self.period)
        self.formGroupBox.addControl(self.amount)
        self.formGroupBox.addControl(self.payment_status)

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
        self.savePayment()
        self.close()
    def savePayment(self):
        try:
            mydb =Sql_DB()
            myConnection=mydb.db_connect()
            mycursor = myConnection.cursor()

            customerId=self.customerId
            period=self.periodNameDict.get(self.period.form_control.currentText())
            amount=self.amount.form_control.text()    
            status=self.payment_status.form_control.currentIndex()
            if status==1:
                stat=True
            elif status==2:
                stat=False    
            check_query=F"""SELECT Id,Amount 
                           FROM payments
                           WHERE CustomerId='{customerId}' and PeriodId='{period}'"""
            mycursor.execute(check_query)
            isExist=mycursor.fetchone()
            if isExist:
                investor_info=getInvestorInfo(customerId) 
                messageBoxDialog.show_critical_messagebox(F"""{investor_info['name']} {investor_info['family']}
                                                              has paid {isExist[1]} Tooman For this mount
                                                              if you want to change this payment,
                                                              you shoud use edition form""")               
                return                                                  
            sql = """INSERT INTO payments (CustomerId,PeriodId,Amount,status) 
            VALUES (%s,%s, %s,%s)"""
            val = (customerId,period,amount,stat)
            print(val)
            mycursor.execute(sql, val)
            myConnection.commit()
            messageBoxDialog.show_info_messagebox("created successfully")
            self.createNewOne.emit(True)
        except mc.Error as e:
            print(e) 
class PaymentEditionForm(QDialog):
    createNewOne=pyqtSignal(bool)
    def __init__(self,customer_id,period_id):
        super(PaymentEditionForm,self).__init__()
        self.lastamount,laststat=getInvestorPaymentInPeriod(customer_id,period_id)
         # setting window title
        investor_info=getInvestorInfo(customer_id) 
        self.setWindowTitle(F"Payment  Form For {investor_info.get('name')} {investor_info.get('family')} _ {investor_info.get('senior')}")
        # setting geometry to the window
        self.setGeometry(700, 150, 600, 400)
        
        self.customerId=customer_id
        self.period=period_id
        temp,period_name_dict=period.getperiodNamesById()
        period_name=period_name_dict.get(period_id)
        
        self.formGroupBox = FormGroup()
        self.formGroupBox.groupValidation.connect(self.formValidation)

        self.name_lable=QLabel(F"{investor_info.get('name')} {investor_info.get('family')}")
        self.period_lable=QLabel(period_name)

        self.amount=FormControl('Amount')
        self.amount.required=True
        self.amount.number=True
        if self.lastamount:
            self.amount.form_control.setText(str(self.lastamount))

        self.payment_status=ComboBoxControl(self,[None,'final','reserved'],"payment status")
        self.payment_status.required=True

        self.formGroupBox.addControl(self.amount)
        self.formGroupBox.addControl(self.payment_status)

        self.buttonBox = QHBoxLayout()
        self.saveButton=QPushButton('Edit')
        self.saveButton.setDisabled(True)
        self.cancleButton=QPushButton('cancle')
        self.buttonBox.addWidget(self.saveButton)
        self.buttonBox.addWidget(self.cancleButton)
    
        # creating a vertical layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.name_lable)
        mainLayout.addWidget(self.period_lable)
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
        self.savePayment()
        self.close()   
    def savePayment(self):
            customerId=self.customerId
            period=self.period
            amount=self.amount.form_control.text()  
            status=self.payment_status.form_control.currentIndex()  
            if status==1:
                stat=1
            elif status==2:
                stat=0    
            if savePaymentForInvestor(customerId,period,stat,amount):
                self.createNewOne.emit=True
           
class PaymentListForCurrentPeriod(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(1200, 800))
        self.setWindowTitle("List of Ehsan Novin Investors Payments")
        self.superLayout=QVBoxLayout(self)
        self.main_table=self.mainTable()
        self.superLayout.addWidget(self.main_table,alignment=Qt.AlignCenter)
        
    def mainTable(self):
        payments=getCurrentPayments()
        columns=["investor name","payment amount","status"]
        table=QTableWidget()
        table.setColumnCount(3)
        table.setRowCount(len(payments))
        table.setMinimumWidth(700)
        table.setMinimumHeight(700)
        table.setStyleSheet(ehsanStyle.TableCSS.tableStyle1())
        table.setHorizontalHeaderLabels(columns)
        total=0
        for i,rec in enumerate(payments):
            tableItem=QTableWidgetItem(F"{rec[0]} {rec[1]}")
            am="" if not rec[2] else str(rec[2])
            tableItem_=QTableWidgetItem(am)
            st="" if not rec[3] else str(rec[3])
            tablestatItem_=QTableWidgetItem(st)
            table.setItem(i,0,tableItem)
            table.setItem(i,1,tableItem_)
            table.setItem(i,2,tablestatItem_)
            if rec[2]:
              total=total+rec[2]
        table.resizeColumnsToContents()
        table.resizeRowsToContents()  
        return table          
class PaymentListForAll(QWidget):
    def __init__(self):
        self.status=False
        self.year=1400
        super().__init__()
        self.setMinimumSize(QSize(1700, 800))
        self.setWindowTitle("List of Ehsan Novin Investors Payment")

        self.superLayout=QVBoxLayout(self)
        period_layout=QHBoxLayout(self)

        self.period_lable=QLabel("Payment Period:")
        self.period_radio=QRadioButton("1400",self)
        self.period_radio.toggled.connect(partial(self.changePeriod,1400))
        self.period_radio1=QRadioButton("1401",self)
        self.period_radio1.toggled.connect(partial(self.changePeriod,1401))
        self.period_radio2=QRadioButton("1402",self)
        self.period_radio2.toggled.connect(partial(self.changePeriod,1402))

        self.stat_checkbox=QCheckBox("Just Final Payment",self)
        self.stat_checkbox.stateChanged.connect(self.filterState)

        self.filter_btn=QPushButton("Filter Result")
        self.filter_btn.clicked.connect(self.updateTable)
        self.filter_btn.setStyleSheet("""
                background-color: #e0f777;
                border-radius: 10px;
                font-size: 10pt;
                font:bold;
                padding: 2px;
                width: 90px;
                height: 50px;

            """)
        
        period_layout.addWidget(self.period_lable)
        period_layout.addWidget(self.period_radio)
        period_layout.addWidget(self.period_radio1)
        period_layout.addWidget(self.period_radio2)
        period_layout.addWidget(self.stat_checkbox)
        period_layout.addWidget(self.filter_btn)
         
        self.frame1 = QFrame()
        self.frame1.setFixedSize(1600,50)
        self.frame1.setStyleSheet("background-color:#eeffcc;border-radius: 10px;")
        self.frame1.setLayout(period_layout)

        self.main_table=self.mainTable(self.year,self.status)
        
        self.superLayout.addWidget(self.frame1)
        self.superLayout.addWidget(self.main_table,alignment=Qt.AlignCenter)

    def filterState(self,state):
        if state==Qt.Checked:
            self.status=True
        else:
            self.status=False
    def changePeriod(self,year):
        self.year= year         
    def mainTable(self,year,stat):
        print("this is main table")
        periods,investors,payments=getInvestorsPayment(null,year,stat)
        header=[]
        header_counter={}
        period_total={}
        customer_counter={}
        names=[]
        total=[]
        table=QTableWidget()
        table.setColumnCount(len(periods)+1)
        table.setRowCount(len(investors)+1)
        table.setStyleSheet( ehsanStyle.TableCSS.tableStyle1() )
        for i,value in enumerate(periods):
            header_counter[value[1]]=i
            period_total[value[1]]=0
            header.append(value[0])
        self.period_id_finder={value:key for key,value in header_counter.items()}
        for j,value in enumerate(investors):
            customer_counter[value[2]]=j
            names.append(F"{value[0]} {value[1]}")
            total.append(0)
        self.investor_id_finder={value:key for key,value in customer_counter.items()}     
        names.append("period total payment")    
        header.append("Total")        
        table.setHorizontalHeaderLabels(header)
        table.setVerticalHeaderLabels(names)
        for rec in payments:
            tableItem=QTableWidgetItem(F"{rec[0]}")
            if rec[3]==0:
                tableItem.setBackground(QColor(24,0,33))#check by ameri
            line=customer_counter[F"{rec[2]}"]
            period_total[rec[1]]+=rec[0]
            total[line]+=rec[0]
            col=header_counter[rec[1]]
            table.setItem(line,col,tableItem)
        total_col=len(header)-1    
        for i,pay in enumerate(total):
            tableItem=QTableWidgetItem(F"{pay}")
            table.setItem(i,total_col,tableItem)
        total_row=len(names)-1
        for key in period_total:
            col=header_counter[key]
            table_item=QTableWidgetItem(F"{period_total[key]}")
            table.setItem(total_row,col,table_item)
  
        table.resizeColumnsToContents()
        table.resizeRowsToContents() 
        width=0  
        for i in range (table.columnCount()+1):
            width+=table.horizontalHeader().sectionSize(i)   
        t=table.verticalHeader().sizeHint().width()
        table.setMinimumWidth(width+t) 
        table.setMinimumHeight(700)  
        table.itemChanged.connect(self.editTable) 
        table.keyPressEvent=self.tableKeyPressedEvent
        table.contextMenuEvent=self.tableContextMenuEvent
        return table
    def tableKeyPressedEvent(self,event):
        if event.key()== Qt.Key_Enter or event.key()==Qt.Key_Return:
            current = self.main_table.currentIndex()
            nextIndex = current.sibling(current.row() + 1, current.column())
            if nextIndex.isValid():
                self.main_table.setCurrentIndex(nextIndex)
                self.main_table.edit(nextIndex)
   
        return
        
    def tableContextMenuEvent(self, event):
        row = self.main_table.rowAt(event.pos().y())
        col = self.main_table.columnAt(event.pos().x())
        if row == self.main_table.rowCount()-1 or col>= self.main_table.columnCount()-1:
            return 
        contextMenu = QMenu(self)
        finalizeAct = contextMenu.addAction("Finalize")
        reserveAct = contextMenu.addAction("Reserve")
        contextMenu.popup(QCursor.pos())
        finalizeAct.triggered.connect(partial(self.finalize,row,col))
        reserveAct.triggered.connect(partial(self.reserve,row,col))
    def finalize(self,row,col): 
        amount=self.main_table.item(row,col)
        if amount==None: return   
        if row == self.main_table.rowCount()-1 or col>= self.main_table.columnCount()-1:
            return 
        period_id=self.period_id_finder[col]
        inv_id=self.investor_id_finder[row]
        stat=1
        savePaymentForInvestor(inv_id,period_id,stat,int(amount.text()))
        
    def reserve(self,row,col): 
        amount=self.main_table.item(row,col)
        if amount==None: return   
        if row == self.main_table.rowCount()-1 or col>= self.main_table.columnCount()-1:
            return 
        period_id=self.period_id_finder[col]
        inv_id=self.investor_id_finder[row]
        stat=0
        savePaymentForInvestor(inv_id,period_id,stat,int(amount.text()))
    
    def editTable(self,item):
        row=item.row()
        col=item.column()
        print()
        if row == self.main_table.rowCount()-1 or col== self.main_table.columnCount()-1:
            return 
        period_id=self.period_id_finder[col]
        inv_id=self.investor_id_finder[row]
        amount=item.text()
        if amount.isnumeric()==False:
            item.setText("")
            return
        stat=1
        if amount=="" :
            deletePaymentForInvestor(inv_id,period_id)
        else :savePaymentForInvestor(inv_id,period_id,stat,int(amount))
 
    def updateTable(self):
        print("this is update")
        periods,investors,payments=getInvestorsPayment(null,self.year,self.status)
        header=[]
        header_counter={}
        period_total={}
        customer_counter={}
        names=[]
        total=[]
        table=self.main_table
        table.itemChanged.disconnect(self.editTable)
        while (table.rowCount() > 0):
        
            table.removeRow(0)
        
        table.setColumnCount(len(periods)+1)
        table.setRowCount(len(investors)+1)
        table.setStyleSheet( self.tableStyle() )
        for i,value in enumerate(periods):
            header_counter[value[1]]=i
            period_total[value[1]]=0
            header.append(value[0])
        self.period_id_finder={value:key for key,value in header_counter.items()}
        for j,value in enumerate(investors):
            customer_counter[value[2]]=j
            names.append(F"{value[0]} {value[1]}")
            total.append(0)
        self.investor_id_finder={value:key for key,value in customer_counter.items()}     
        names.append("period total payment")    
        header.append("Total")        
        table.setHorizontalHeaderLabels(header)
        table.setVerticalHeaderLabels(names)
        for rec in payments:
            tableItem=QTableWidgetItem(F"{rec[0]}")
            if rec[3]:
                tableItem.setBackground(QColor(255,240,255))    
            line=customer_counter[F"{rec[2]}"]
            period_total[rec[1]]+=rec[0]
            total[line]+=rec[0]
            col=header_counter[rec[1]]
            table.setItem(line,col,tableItem)
        total_col=len(header)-1    
        for i,pay in enumerate(total):
            tableItem=QTableWidgetItem(F"{pay}")
            table.setItem(i,total_col,tableItem)
        total_row=len(names)-1
        for key in period_total:
            col=header_counter[key]
            table_item=QTableWidgetItem(F"{period_total[key]}")
            table.setItem(total_row,col,table_item)  
  
        table.resizeColumnsToContents()
        table.resizeRowsToContents() 
        width=0  
        for i in range (table.columnCount()+1):
            width+=table.horizontalHeader().sectionSize(i)   
        t=table.verticalHeader().sizeHint().width()   
        table.setMinimumWidth(width+t) 
        table.setMinimumHeight(700)  
        table.itemChanged.connect(self.editTable) 
        
class PaymentListForInvestor(QWidget):
    def __init__(self,investor_id):
        super().__init__()
        self.setMinimumSize(QSize(800, 750))
        self.setWindowTitle("List of Ehsan Novin Investor Payment")
        self.superLayout=QVBoxLayout(self)
        self.add_payment_for_investor=QPushButton("Add Payment")
        self.add_payment_for_investor.setStyleSheet(ehsanStyle.BtnCss.btnStyle())
        self.add_payment_for_investor.clicked.connect(partial(self.addPaymentInvestor,investor_id))
        self.main_table=self.mainTable(investor_id)
        self.superLayout.addWidget(self.add_payment_for_investor)
        self.superLayout.addWidget(self.main_table,alignment=Qt.AlignCenter)
        
    def mainTable(self,investor_id):
        periods,investors,payments=getInvestorsPayment(investor_id)
        period_dict_by_id={key:value for value,key in periods}
        header=['payment period','payment amount','Payment Status']
        total=0        
        table=QTableWidget()
        table.setRowCount(len(payments)+1)
        table.setColumnCount(3)
        table.setMinimumWidth(700)
        table.setMinimumHeight(700)
        table.setHorizontalHeaderLabels(header)
        table.setStyleSheet(ehsanStyle.TableCSS.tableStyle1())    
        for line,rec in enumerate(payments):
            tableItem_amount=QTableWidgetItem(F"{rec[0]}")
            tableItem_period=QTableWidgetItem(period_dict_by_id[rec[1]])
            tableItem_status=QTableWidgetItem(F"{rec[2]}")
            total+=rec[0]
            
            table.setItem(line,0,tableItem_period)
            table.setItem(line,1,tableItem_amount)
            table.setItem(line,2,tableItem_status)

        tableItem=QTableWidgetItem("Total payment") 
        table.setItem(len(payments),0,tableItem)
        tableItem=QTableWidgetItem(F"{total}")
        table.setItem(len(payments),1,tableItem)
        table.resizeColumnsToContents()
        table.resizeRowsToContents()     
        return table
    def updateTable(self,investor_id):    
        periods,investors,payments=getInvestorsPayment(investor_id)
        header=['payment amount']
        rows=[]
        rows_counter={}
        total=0
        for i,value in enumerate(periods):
            rows_counter[value[1]]=i
            rows.append(value[0])

        rows.append("Total")        
        table=self.main_table
        table.setRowCount(len(rows))
        table.setColumnCount(1)
        table.setMinimumWidth(400)
        table.setMinimumHeight(500)
        table.setHorizontalHeaderLabels(header)
        table.setVerticalHeaderLabels(rows)
        for rec in payments:
            tableItem=QTableWidgetItem(F"{rec[0]}")
            total+=rec[0]
            line=rows_counter[rec[1]]
            table.setItem(line,0,tableItem)

           
        tableItem=QTableWidgetItem(F"{total}")
        table.setItem(len(rows)-1,0,tableItem)
        table.resizeColumnsToContents()
        table.resizeRowsToContents()     
    def addPaymentInvestor(self,investor_id):
         addPayment_investor=PaymentForm(investor_id) 
         addPayment_investor.createNewOne.connect(partial(self.updateTable,investor_id))
         addPayment_investor.exec()              
        
def getTotalPayment():
    try:
        conection=Sql_DB().db_connect()
        myCursor=conection.cursor()
        query="SELECT SUM(amount) FROM payments"
        myCursor.execute(query)
        total_payment=myCursor.fetchone()[0]
        return total_payment
    except mc.Error as e:
        print(f"{e}")
def getCurrentPayments():
    try:
        connection=Sql_DB().db_connect()
        mycursor=connection.cursor()
        query="""
        SELECT name,family , amount ,status
        FROM customers 
        LEFT JOIN
        (   SELECT customerid,amount,status 
            FROM payments
            WHERE periodId=(SELECT Id 
                            FROM assetperiod 
                            ORDER BY year,month 
                            LIMIT 0,1)
        )PA
        ON customers.id=PA.customerId"""
        mycursor.execute(query)
        current_payment=mycursor.fetchall()
        return current_payment
    except mc.Error as e:  
        messageBoxDialog.show_critical_messagebox(F"{e}")  
def getInvestorsPayment(investor_id=null,year=1400,isfinal=False):
    where=""
    if isfinal:
        where="AND status=1" 
    try:      
        mydb=Sql_DB()
        myConnection=mydb.db_connect()
        myCursor=myConnection.cursor()        
    
        #header of table
        my_period_query=F"""SELECT name,id
                            FROM assetperiod
                            WHERE year={year}
                            ORDER BY year,month"""
        myCursor.execute(my_period_query)
        period_list=myCursor.fetchall()        
        period_id_list=[p[1] for p in period_list]
        investor_list=[]
        payment_list=[]
        if investor_id==null:
            #each investor payments in every period
            paymet_query=f"""SELECT  payments.amount, payments.PeriodId, payments.customerId,payments.status
                            FROM payments 
                            WHERE payments.periodId in {tuple(period_id_list)} {where}
                            ORDER BY PeriodId"""
            myCursor.execute(paymet_query)
            payment_list= myCursor.fetchall() 
                        
            #investor_names by id
            my_investor_name_query="""SELECT name,family,id
                                        FROM Customers
                                        ORDER BY Id"""
            myCursor.execute(my_investor_name_query)
            investor_list=myCursor.fetchall()   
        else:
            #payments for spcified investor in every period
            paymet_query=F"""SELECT  payments.amount, payments.PeriodId,status
                            FROM payments 
                            WHERE customerId='{investor_id}' 
                            ORDER BY PeriodId"""
            myCursor.execute(paymet_query)
            payment_list= myCursor.fetchall()  

        return period_list,investor_list,payment_list

    except mc.Error as e:
        messageBoxDialog.show_critical_messagebox("{0} :geting investor from db was not successfully".format(e))    
def getInvestorInfo(inv_id):
    try:      
        mydb=Sql_DB()
        myConnection=mydb.db_connect()
        myCursor=myConnection.cursor()


        myDataQuery=F"""SELECT Name,Family,WhatsApp,NationCode,senior 
                       FROM Customers
                       WHERE Id='{inv_id}'"""
        myCursor.execute(myDataQuery)
        data=myCursor.fetchone()
        inv={}
        inv['name']=data[0]
        inv['family']=data[1]
        inv['whatsapp']=data[2]
        inv['nationcode']=data[3]
        inv['senior']=data[4]
        return inv

    except mc.Error as e:
            messageBoxDialog.show_critical_messagebox(F"{e}")
def getInvestorPaymentInPeriod(invId,periodId):
    try:
        connection=Sql_DB().db_connect()
        my_cursor=connection.cursor()
        query=f""" SELECT amount,status
                   FROM payments
                   WHERE CustomerId='{invId}' AND PeriodId='{periodId}'
        """
        my_cursor.execute(query)
        rec=my_cursor.fetchone()
        if rec:
            return rec[0],rec[1]
        return 0,False   
    except mc.Error as e:
        messageBoxDialog.show_critical_messagebox(f"{e}")  
def savePaymentForInvestor(invId,periodId,stat,amount):
    try:
            mydb =Sql_DB()
            myConnection=mydb.db_connect()
            mycursor = myConnection.cursor()
            lastamount,laststat=getInvestorPaymentInPeriod(invId,periodId)
            if lastamount:            
                sql = F"""UPDATE payments 
                SET Amount='{amount}' , Status='{stat}' 
                WHERE periodId='{periodId}' AND customerId='{invId}'"""
            else:
                sql = F"""INSERT INTO payments (CustomerId,PeriodId,Amount,status) 
                VALUES ('{invId}','{periodId}','{amount}','{stat}')"""
                
            mycursor.execute(sql)
            myConnection.commit()
            return True
    except mc.Error as e:
            messageBoxDialog.show_critical_messagebox(F"{e}") 
            return False  
def deletePaymentForInvestor(invId,periodId):
    try:
        connection=Sql_DB().db_connect()
        cursor=connection.cursor()
        query=F"""DELETE FROM payments 
                  WHERE periodId='{periodId}' 
                  AND customerId='{invId}' """
        cursor.execute(query)
        connection.commit()
    except mc.Error as e:
        messageBoxDialog.show_critical_messagebox(F"{e}")
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = PaymentListForAll()
    #ui=PaymentForm(1020)
    ui.show()
    sys.exit(app.exec_())
