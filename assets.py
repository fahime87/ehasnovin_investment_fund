from PyQt5.QtWidgets import QDialog,QVBoxLayout,QHBoxLayout,QPushButton,QCalendarWidget,QCheckBox,QTableWidget,QTableWidgetItem,QWidget
from PyQt5 import QtWidgets
from tools import ComboBoxControl,FormGroup,FormControl
from dataBase import Sql_DB
from messageBox import messageBoxDialog
import mysql.connector as mc
from period import *
from PyQt5.QtCore import QSize,Qt
import sys

class AssetForm(QDialog):
    createNewOne=pyqtSignal(bool)
    def __init__(self):
        super(AssetForm,self).__init__()
        # setting window title
        self.setWindowTitle("Asset  Form")
        # setting geometry to the window
        self.setGeometry(700, 150, 400, 400)
        self.formGroupBox = FormGroup()
        self.formGroupBox.groupValidation.connect(self.formValidation)
        self.date=QCalendarWidget(self)
        # setting cursor
        self.date.setCursor(Qt.PointingHandCursor)
        # setting properties
        self.date.setProperty("Blocked", 0)
        # setting properties
        self.date.setProperty("Highlighted dates : ", 0)
        self.periodNameDict,temp=getperiodNamesById()
        self.period=ComboBoxControl(self,list(self.periodNameDict.keys()),"AssetPeriod")

        self.assetNameDict,id_dict=getAssetBasketcontentById()
        assetNameList=[None,]
        assetNameList=[None]+list(self.assetNameDict.keys())
        self.assetName=ComboBoxControl(self,assetNameList,"AssetName")
        self.assetName.changeValue.connect(self.assetUnit)
        self.assetName.required=True
        self.assetName.form_control.setStyleSheet("background-color: yellow")

        self.sharePrice=FormControl('Share Price')
        self.sharePrice.required=True
        self.sharePrice.number=True

        self.shareInvestment=FormControl('Share Investment')
        self.shareInvestment.required=True
        self.shareInvestment.number=True

        self.shareBought=FormControl('Share Bought')
        self.shareBought.required=True
        self.shareBought.number=True

        self.unit=""

        self.fee=FormControl('Fee')
        self.fee.required=True
        self.fee.number=True
        
        #self.formGroupBox.addControl(self.date)
        self.formGroupBox.addControl(self.period)
        self.formGroupBox.addControl(self.assetName)
        self.formGroupBox.addControl(self.sharePrice)
        self.formGroupBox.addControl(self.shareInvestment)
        self.formGroupBox.addControl(self.shareBought)
        #self.formGroupBox.addControl(self.unit)
        self.formGroupBox.addControl(self.fee)

        self.buttonBox = QHBoxLayout()
        self.saveButton=QPushButton('save')
        self.saveButton.setDisabled(True)
        self.cancleButton=QPushButton('cancle')
        self.buttonBox.addWidget(self.saveButton)
        self.buttonBox.addWidget(self.cancleButton)
    
        # creating a vertical layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.date)
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
        self.saveAssets()
        self.close()
    def saveAssets(self):
        try:
            mydb =Sql_DB()
            myConnection=mydb.db_connect()
            mycursor = myConnection.cursor()

            date=self.date.selectedDate().toPyDate().isoformat()
            period=self.periodNameDict.get(self.period.form_control.currentText())
            name=self.assetNameDict.get(self.assetName.form_control.currentText())  
            shareInvestment=self.shareInvestment.form_control.text()
            sharePrice=self.sharePrice.form_control.text()
            shareBought=self.shareBought.form_control.text()
            unit=self.unit#.form_control.currentText()
            fee=self.fee.form_control.text()
            
            sql = """INSERT INTO assets (AssetDate,PeriodId,AssetId,ShareInvestment,SharePrice,ShareBought,Unit,Fee) 
            VALUES (%s,%s, %s,%s,%s,%s,%s,%s)"""
            val = (date,period,name,shareInvestment,shareBought,sharePrice,unit,fee)
            mycursor.execute(sql, val)
            myConnection.commit()
            messageBoxDialog.show_info_messagebox("created successfully")
            self.createNewOne.emit(True)
        except mc.Error as e:
            print(e)
            #self.show_info_messagebox(e)            
    def assetUnit(self):
        if not self.assetName.form_control.currentText():
            self.unit=""
        else:
            myAssetName=self.assetName.form_control.currentText()
            myAssetId=(self.assetNameDict[myAssetName])
            mydb=Sql_DB()
            myConnection=mydb.db_connect()
            myCursor=myConnection.cursor()
            query=f"SELECT SecondUnit FROM assetbasket WHERE Id='{myAssetId}'"
            myCursor.execute(query)
            self.unit=myCursor.fetchone()[0]
class AssetList(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(800, 500))
        self.setWindowTitle("Simple Table with Static Data")
        self.superLayout=QVBoxLayout(self)
        
        mydb=Sql_DB()
        myConnection=mydb.db_connect()
        myCursor=myConnection.cursor()

        self.table=self.assetTable()
        self.createNewAsset=QPushButton("create new asset")
        self.createNewAsset.clicked.connect(self.assetForm)
        self.superLayout.addWidget(self.table)
        self.superLayout.addWidget(self.createNewAsset)
        #self.setLayout(self.superLayout)
    def getAssets(self):    
        try:
            mydb=Sql_DB()
            myConnection=mydb.db_connect()
            myCursor=myConnection.cursor()

            #header of table
            myColumnQuery="""SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = N'assets'"""
            myCursor.execute(myColumnQuery)
            columnName=myCursor.fetchall()
            header=list(map(lambda x:x[0],columnName))

            #data of table
            myDataQuery="SELECT * FROM assets"
            myCursor.execute(myDataQuery)
            data=myCursor.fetchall()
            return header,data
        except mc.Error as e:
            messageBoxDialog.show_critical_messagebox(F"{e}")    
    def assetTable(self): 
        header,data=self.getAssets() 
        name_dict,asset_basket=getAssetBasketcontentById() 
        period_dict,period_id=getperiodNamesById()
        table=QTableWidget()
        table.setColumnCount(len(header)) 
        table.setRowCount(len(data))
        table.setMidLineWidth(500)
        table.setMinimumHeight(500)
        table.setHorizontalHeaderLabels(header)
        for i,row in enumerate(data):
            for j,value in enumerate(row):
                if j==2:
                    value=asset_basket.get(value)
                elif j==1:
                    value=period_id.get(value)    
                table_item=QTableWidgetItem(str(value))
                table.setItem(i,j,table_item)
        table.resizeRowsToContents()
        table.resizeColumnsToContents()
        return table
    def updateTable(self):
        header,data=self.getAssets() 
        name_dict,asset_basket=getAssetBasketcontentById() 
        period_dict,period_id=getperiodNamesById()
        table=self.table
        table.setColumnCount(len(header)) 
        table.setRowCount(len(data))
        table.setMidLineWidth(500)
        table.setMinimumHeight(500)
        table.setHorizontalHeaderLabels(header)
        for i,row in enumerate(data):
            for j,value in enumerate(row):
                if j==2:
                    value=asset_basket.get(value)
                elif j==1:
                    value=period_id.get(value)    
                table_item=QTableWidgetItem(str(value))
                table.setItem(i,j,table_item)
        table.resizeRowsToContents()
        table.resizeColumnsToContents()

    def assetForm(self):
        Form = AssetForm()
        Form.createNewOne.connect(self.updateTable)
        Form.exec_()
    def configureTable(self, table):
        rowf = 3
        table.setColumnCount(3)
        table.setRowCount(rowf)
        table.setHorizontalHeaderItem(0, QTableWidgetItem("col1"))
        table.setHorizontalHeaderItem(1,QTableWidgetItem("col2"))
        table.setHorizontalHeaderItem(2,QTableWidgetItem("col3"))
        table.horizontalHeader().setStretchLastSection(True)  
#**********************************class to define asset basket******************************
class AssetBasketForm(QDialog):
    createNewOne=pyqtSignal(bool)
    def __init__(self):
        super(AssetBasketForm,self).__init__()
        self.setWindowTitle("Add asset in your basket")
        self.setGeometry(700, 300, 400, 400)
 
        self.formGroupBox = FormGroup()
        self.formGroupBox.groupValidation.connect(self.formValidation)

        self.name=FormControl("Name")
        self.name.required=True
        self.name.form_control.setPlaceholderText('asset_name')
        self.name.form_control.setStyleSheet("background-color: yellow")
        

        self.type=ComboBoxControl(self,['Dollar','Gold','Crypto','IranStock'],"Type")
        self.type.required=True

        self.baseUnit=FormControl('Base Unit')
        self.baseUnit.required=True

        self.secondUnit=FormControl('Second Unit')
        self.secondUnit.required=True

        self.unitScale=FormControl('Base Unit/Second Unit')
        self.unitScale.number=True
        self.unitScale.required=True
        
        self.saveUnit=QCheckBox("Save By Second Unit")

        self.formGroupBox.addControl(self.name)
        self.formGroupBox.addControl(self.type)
        self.formGroupBox.addControl(self.baseUnit)
        self.formGroupBox.addControl(self.secondUnit)
        self.formGroupBox.addControl(self.unitScale)

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
        mainLayout.addWidget(self.saveUnit)
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
        self.saveAssetBascket()
        self.close()
    def saveAssetBascket(self):
        try:
            mydb =Sql_DB()
            myConnection=mydb.db_connect()
            mycursor = myConnection.cursor()
 
            name=self.name.form_control.text()  
            type=self.type.form_control.currentText()
            unit=self.baseUnit.form_control.text()
            secondUnit=self.secondUnit.form_control.text()
            unitScale=self.unitScale.form_control.text()
            saveunit=self.saveUnit.isChecked()
            
            sql = "INSERT INTO assetBasket (Name,Type,Unit,SecondUnit,UnitScale,saveunit) VALUES (%s, %s,%s,%s,%s,%s)"
            val = (name,type,unit,secondUnit,unitScale,saveunit)
            mycursor.execute(sql, val)
            myConnection.commit()
            messageBoxDialog.show_info_messagebox("created successfully")
            self.createNewOne.emit(True)
        except mc.Error as e:
            messageBoxDialog.show_critical_messagebox(e)                     
class AssetBasketList(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(700, 500))
        self.setWindowTitle("Ehsan Novin Asset Basket")

        self.basket_table=self.basketTable()
        self.add_new_asset_to_basket=QPushButton("Add New Asset To Basket")
        self.add_new_asset_to_basket.clicked.connect(self.openAssetBasketForm)

        self.main_layout=QVBoxLayout()
        self.main_layout.addWidget(self.add_new_asset_to_basket)
        self.main_layout.addWidget(self.basket_table)
        self.setLayout(self.main_layout)
    def openAssetBasketForm(self):
        Form=AssetBasketForm()
        Form.createNewOne.connect(self.updateTable)
        Form.exec()
    def getBasketContent(self):
        try:    
            mydb=Sql_DB()
            myConnection=mydb.db_connect()
            myCursor=myConnection.cursor()
            #header of table
            myColumnQuery="""SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = N'assetbasket'"""
            myCursor.execute(myColumnQuery)
            columnName=myCursor.fetchall()
            header=list(map(lambda x:x[0],columnName))
            header.append("")
            header.append("")
            #data of table
            myDataQuery="SELECT * FROM assetbasket"
            myCursor.execute(myDataQuery)
            data=myCursor.fetchall()
            return header,data
        except mc.Error as e:
            messageBoxDialog.show_critical_messagebox(F"Getting Basket Content Cause To problem :{e} ")  
    def basketTable(self):
        header,data=self.getBasketContent()          
        #draw table
        table=QTableWidget()
        table.setColumnCount(len(header))
        table.setRowCount(len(data))
        table.setHorizontalHeaderLabels(header)
        table.setMinimumHeight(500)
        table.setMinimumWidth(500)
        for j,row in enumerate(data):
            for i,value in enumerate(row):
                tabel_item=QTableWidgetItem(str(value))
                table.setItem(j,i,tabel_item)
            rmv_btn=QPushButton("Remove")
            edit_btn=QPushButton("Edit Asset")   
            rmv_btn.clicked.connect(partial(self.removeBasketContent,row[0])) 
            edit_btn.clicked.connect(partial(self.editBasketContent,row[0]))
            table.setCellWidget(j,7,rmv_btn)
            table.setCellWidget(j,8,edit_btn)
        table.resizeColumnsToContents()
        table.resizeRowsToContents()    
        return table
    def updateTable(self):
        header,data=self.getBasketContent()          
        #draw table
        table=self.basket_table
        table.setColumnCount(len(header))
        table.setRowCount(len(data))
        table.setHorizontalHeaderLabels(header)
        table.setMinimumHeight(500)
        table.setMinimumWidth(500)
        for j,row in enumerate(data):
            for i,value in enumerate(row):
                tabel_item=QTableWidgetItem(str(value))
                table.setItem(j,i,tabel_item)
            rmv_btn=QPushButton("Remove")
            edit_btn=QPushButton("Edit Asset")   
            rmv_btn.clicked.connect(partial(self.removeBasketContent,row[0])) 
            edit_btn.clicked.connect(partial(self.editBasketContent,row[0]))
            table.setCellWidget(j,7,rmv_btn)
            table.setCellWidget(j,8,edit_btn)
    def removeBasketContent(self,asset_id):
        is_used=self.checkStatus(asset_id)
        if is_used:
            messageBoxDialog.show_critical_messagebox("You Cant Remove This Stock From Bascket Because This Asset Has Been Registered")
        else:
            try:
                db=Sql_DB()
                connection=db.db_connect()
                mycursor=connection.cursor()
                rmv_query=F"DELETE FROM assetbasket WHERE Id='{asset_id}'"
                mycursor.execute(rmv_query)
                connection.commit()
                messageBoxDialog.show_info_messagebox("The Stock Has Been Deleted Successfully")
                self.updateTable()
            except mc.Error as e:
                messageBoxDialog.show_critical_messagebox(F"{e}")    
                 

    def editBasketContent(self,asset_id):
        is_used=self.checkStatus(asset_id)
        if is_used:
            messageBoxDialog.show_critical_messagebox("You Cant Edit This Stock In Our Basket Beacause This Has Been Registered In our Assets")
        else:
            print("yes")
    def checkStatus(self,asset_id):
        try:
            db=Sql_DB()
            connection=db.db_connect()
            mycursor=connection.cursor()
            check_query=F"SELECT COUNT(*) FROM assets WHERE assetId='{asset_id}'"
            mycursor.execute(check_query)
            use_count=mycursor.fetchone()[0]
            return use_count>0
        except mc.Error as e:
            messageBoxDialog.show_critical_messagebox(F"{e}")   
class AssetPeriodAmountList(QWidget):
    def __init__(self):
        super(AssetPeriodAmountList,self).__init__()
        self.setMinimumSize(QSize(1200, 700))
        self.setWindowTitle("List of Ehsan Novin Assets Amount")
        self.superLayout=QVBoxLayout(self)
        self.main_table=self.mainTable()
        self.superLayout.addWidget(self.main_table)
        
    def mainTable(self):
        periods,basket,assets=self.getAssetPeriodAmount()
        header=[]
        row=[]
        header_counter={}
        row_counter={}
        total=[]
        for i,value in enumerate(periods):
            header_counter[value[1]]=i
            header.append(value[0])
        for i,value in enumerate(basket):
            row_counter[value[1]]=i
            row.append(F"{value[0]}")
            total.append(0)
        header.append("Total")        
        table=QTableWidget()
        table.setColumnCount(len(header))
        table.setRowCount(len(row))
        table.setMinimumWidth(400)
        table.setMinimumHeight(500)
        table.setHorizontalHeaderLabels(header)
        table.setVerticalHeaderLabels(row)
        for rec in assets:
            tableItem=QTableWidgetItem(F"{rec[0]}")
            line=row_counter[rec[2]]
            total[line]+=rec[0]
            col=header_counter[rec[1]]
            table.setItem(line,col,tableItem)
        total_col=len(header)-1   
        for i,pay in enumerate(total):
            tableItem=QTableWidgetItem(F"{pay}")
            table.setItem(i,total_col,tableItem)
        table.resizeColumnsToContents()
        table.resizeRowsToContents()     

        return table

    def getAssetPeriodAmount(self):
        basket=[]
        asset_list=[]
        try:
            mydb=Sql_DB()
            myConnection=mydb.db_connect()
            myCursor=myConnection.cursor()        
            #header of table
            my_period_query="""SELECT name,id
                                FROM assetperiod
                                ORDER BY year,month"""
            myCursor.execute(my_period_query)
            period_list=myCursor.fetchall()        
            asset_query="""SELECT  SUM(sharebought), PeriodId, assetId
                                FROM assets
                                GROUP BY periodId,assetId
                                ORDER BY PeriodId"""
            myCursor.execute(asset_query)
            asset_list= myCursor.fetchall() 
            my_asset_name_query="""SELECT name,id
                                            FROM assetbasket
                                            ORDER BY Id"""
            myCursor.execute(my_asset_name_query)
            basket=myCursor.fetchall()   
            return period_list,basket,asset_list  

        except mc.Error as e:
            messageBoxDialog.show_critical_messagebox(f"{e}") 

def getAssetBasketcontentById():
    mydb=Sql_DB()
    myConnection=mydb.db_connect()
    myCursor=myConnection.cursor()
    query="SELECT Name,Id FROM assetbasket"
    myCursor.execute(query)
    asset_names=myCursor.fetchall()
    name_dict_by_id=dict(asset_names)
    id_dict_by_name={key:value for value,key in asset_names}         
    return name_dict_by_id ,id_dict_by_name
def getTotalAsset():
    total_assets=[]
    try:
        conection=Sql_DB().db_connect()
        myCursor=conection.cursor()
        query="""SELECT name,SUM( ShareBought ) , assets.unit
                FROM assets
                RIGHT JOIN assetbasket ON assets.assetId = assetbasket.Id
                GROUP BY name
        """
        myCursor.execute(query)
        total_assets=myCursor.fetchall()
        return total_assets
    except mc.Error as e:
        print(f"{e}")
    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    #ui=AssetBasketList()
    #ui=AssetList()
    ui=AssetPeriodAmountList()
    ui.show()
    sys.exit(app.exec_())
