from PyQt5.QtWidgets import QMessageBox
class messageBoxDialog():
    def show_info_messagebox(messageText):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
    
        # setting message for Message Box
        msg.setText(messageText)
        
        # setting Message box window title
        msg.setWindowTitle("Information MessageBox")
        
        # declaring buttons on Message Box
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        # start the app
        retval = msg.exec_()
    
    
    def show_warning_messagebox(Warning):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
    
        # setting message for Message Box
        msg.setText(Warning)
        
        # setting Message box window title
        msg.setWindowTitle("Warning MessageBox")
        
        # declaring buttons on Message Box
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        # start the app
        retval = msg.exec_()
    
    
    def show_question_messagebox(Question):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
    
        # setting message for Message Box
        msg.setText(Question)
        
        # setting Message box window title
        msg.setWindowTitle("Question MessageBox")
        
        # declaring buttons on Message Box
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        # start the app
        retval = msg.exec_()
    
    
    def show_critical_messagebox(Critical):
        msg = QMessageBox()
        #msg.setIcon(QMessageBox.critical)
    
        # setting message for Message Box
        msg.setText(Critical)
        
        # setting Message box window title
        msg.setWindowTitle("Critical MessageBox")
        
        # declaring buttons on Message Box
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        # start the app
        retval = msg.exec_()
        


