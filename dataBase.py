import mysql.connector as mc
from messageBox import messageBoxDialog
class Sql_DB():
    db_name='ehsan_novin'
    def db_connect(self):
            try:
                    mydb = mc.connect(
                        host="localhost",
                        user="root",
                        password="",
                        database=self.db_name
                    )
                    return mydb
            except mc.Error as err:
                messageBoxDialog.show_info_messagebox("database_connection_error")

    def create_database(self):
        try:
            mydb = mc.connect(
 
                host="localhost",
                user="root",
                password=""
            )
            cursor = mydb.cursor()
            cursor.execute("CREATE DATABASE {} ".format(self.db_name))
        except mc.Error as e:
            self.show_info_messagebox("database_creation_error")  

    """       # Table structure for table `customers`
        customer_query='CREATE TABLE IF NOT EXISTS `customers` ('\
        '`Id` char(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,'\
        '`Name` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,'\
        '`Family` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,'\
        '`Senior` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,'\
        '`NationCode` varchar(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,'\
        '`WhatsApp` varchar(11) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,'\
        'PRIMARY KEY (`Id`),'\
        ' UNIQUE KEY `NationCode` (`NationCode`)'\
        ') ENGINE=InnoDB DEFAULT CHARSET=latin1;'       
"""            
"""--
-- Table structure for table `assetperiod`
--

CREATE TABLE IF NOT EXISTS `assetperiod` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) CHARACTER SET utf16 COLLATE utf16_unicode_ci NOT NULL,
  `Year` int(11) NOT NULL,
  `Month` int(11) NOT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Name` (`Name`)
) ENGINE=In""noDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;
"""

"""
CREATE TABLE `ehsan_novin`.`assetBasket` (
`Id` INT( 10 ) NOT NULL AUTO_INCREMENT PRIMARY KEY ,
`Name` VARCHAR( 100 ) CHARACTER SET utf16 COLLATE utf16_unicode_ci NOT NULL ,
`Type` VARCHAR( 100 ) CHARACTER SET utf16 COLLATE utf16_unicode_ci NOT NULL ,
UNIQUE (
`Name`
)
) ENGINE = INNODB

"""
"""
CREATE TABLE `ehsan_novin`.`assets` (`Date` DATE NOT NULL, 
`PeriodId` INT(100) NOT NULL,
 `AssetId` INT(100) NOT NULL, `SharePrice` FLOAT NOT NULL, 
 `ShareInvestment` FLOAT NOT NULL,
 `ShareBought` FLOAT NOT NULL, `Unit` VARCHAR(20) NOT NULL, 
 `Fee` FLOAT NOT NULL, 
 `Id` INT(100) NOT NULL AUTO_INCREMENT PRIMARY KEY) ENGINE = InnoDB;




    def create_database(self):
        try:
            mydb = mc.connect(
 
                host="localhost",
                user="root",
                password=""
            )
            cursor = mydb.cursor()
            dbname = 'ehsan_novin'
            cursor.execute("CREATE DATABASE {} ".format(dbname))
        except mc.Error as e:
            self.show_info_messagebox("database_creation_error")  

        # Table structure for table `customers`
        customer_query='CREATE TABLE IF NOT EXISTS `customers` ('\
        '`Id` char(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,'\
        '`Name` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,'\
        '`Family` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,'\
        '`Senior` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,'\
        '`NationCode` varchar(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,'\
        '`WhatsApp` varchar(11) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,'\
        'PRIMARY KEY (`Id`),'\
        ' UNIQUE KEY `NationCode` (`NationCode`)'\
        ') ENGINE=InnoDB DEFAULT CHARSET=latin1;'       
"""