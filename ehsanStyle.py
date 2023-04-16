class TableCSS():
    def tableStyle1():
        css_str="""
             QTableView::item
                {
                padding: 4px;
                font-size: 10pt;
                border-style: none;
                border-radius: 10px;
                padding-right:auto;
                padding-left:auto;
                background-color: #edffa1;
                
                }
           
            QHeaderView::section {
                background-color: #e0f777;
                padding: 4px;
                font-size: 10pt;
                border-style: none;
                border-radius: 10px;
                border-bottom: 2px solid #fffff8;
                border-right: 2px solid #fffff8;
                padding-right:auto;
                padding-left:auto;

            }
            QTableView{
                border-radius: 10px;
                border:none;
                background-color:#e8f5a9;
            }
            """
        return css_str  
    
class BtnCss():
           def btnStyle():
                return"""background-color: #e0f777;
                border-radius: 10px;
                font-size: 10pt;
                font:bold;
                padding: 2px;
                width: 90px;
                height: 50px;"""