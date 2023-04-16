from PyQt5.QtWidgets import QWidget,QVBoxLayout,QLabel,QApplication
from payment import getTotalPayment
from assets import getTotalAsset
class EhsanHome(QWidget):
    def __init__(self):
        super(EhsanHome,self).__init__()
        self.setGeometry(0,0,1000,800)
        self.main_layout=QVBoxLayout()
        self.payment_lable=QLabel()
        payment_amont=getTotalPayment()
        text=F"the Investors has paid {payment_amont} Tooman "
        self.main_layout.addWidget(self.payment_lable)
        self.payment_lable.setText(text)
        self.assets=getTotalAsset()
        for asset in self.assets:
            lable=QLabel()
            lable.setText(F"{asset[0]} :{asset[1]}{asset[2]}")
            self.main_layout.addWidget(lable)
        self.setLayout(self.main_layout)
    def getAllPayments(self):
        return 10804500

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    #ui=AssetBasketList()
    ui=EhsanHome()
    ui.show()
    sys.exit(app.exec_())            
