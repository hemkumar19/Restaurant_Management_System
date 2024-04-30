import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QLabel, QVBoxLayout, QWidget
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from datetime import date
from PyQt5.QtCore import QDate
import random
import mysql.connector
class Welcome(QDialog):
    def __init__(self):
        super(Welcome, self).__init__()
        loadUi("welcome.ui",self)
        self.login.clicked.connect(self.gotologin)
        self.create.clicked.connect(self.gotocreate)

    def gotologin(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotocreate(self):
        create = Create()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui",self)
        global num1 
        num1 = int(random.randint(1, 100000))  # Generate a random number for comparison
        self.lineEdit1.setText(str(num1))
        self.create_id_back.clicked.connect(self.create_id)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.clicked.connect(self.loginfunction)
        self.verify.clicked.connect(self.verify_btn)
    
    def create_id(self):
        widget.removeWidget(widget.currentWidget())      

    def verify_btn(self):
        try:
            num2 = int(self.lineEdit2.text())  # Get the user's input (second number)
            if num1 == num2:  # Compare the first number with the user's input
                self.label_5.setText("Match! First number equals second number.")
                return True
            else:
                self.label_5.setText("No match! First number doesn't equal second number.")
                return False
        except ValueError:
            self.label_5.setText("Invalid input. Please enter a number.")

    def loginfunction(self):
        user = self.emailfield.text()
        password = self.passwordfield.text()
        
        Home() #remove after
        
        
        if len(user)==0 or len(password)==0:
            self.error.setText("Please input all fields.")

        else:
            connection = mysql.connector.connect(host="localhost", user="root", password="", database="restaurant")
            cursor = connection.cursor()
            query = 'SELECT password FROM login WHERE username = %s'
            cursor.execute(query, (user,))
            result_pass = cursor.fetchone()
            if ( result_pass and result_pass[0] == password) and (True == self.verify_btn()):
                print("Successfully logged in.")

                Home()
            else:
                self.error.setText("Invalid username or password")


class Create(QDialog):  
    def __init__(self):
        super(Create, self).__init__()
        loadUi("create.ui",self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup.clicked.connect(self.signupfunction)
        self.login_id.clicked.connect(self.login_idf)
    
    def login_idf(self):
        widget.removeWidget(widget.currentWidget())      

    def signupfunction(self):
        user = self.emailfield.text()
        password = self.passwordfield.text()
        confirmpassword = self.confirmpasswordfield.text()

        if len(user)==0 or len(password)==0 or len(confirmpassword)==0:
            self.error.setText("Please fill in all inputs.")

        elif password!=confirmpassword:
            self.error.setText("Passwords do not match.")
        else:
            try:
                connection = mysql.connector.connect(host="localhost", user="root", password="", database="restaurant")
                cursor = connection.cursor()
                login = (user, password) 
                cursor.execute('INSERT INTO login (username, password) VALUES (%s, %s)', login)

                connection.commit()
                connection.close()
                print("Signup successful.")  
                welcome.gotologin()
            except mysql.connector.Error as err:
                print("Error:", err)

class Logout(QDialog):
    def __init__(self):
        super(Logout, self).__init__()

    def logout(self):
        widget.removeWidget(widget.currentWidget())

class Home(QDialog):
    def __init__(self):
        super(Home, self).__init__()
        loadUi("home.ui", self)
        widget.addWidget(self)
        widget.setCurrentIndex(widget.currentIndex() + 1)

        self.add_btn.clicked.connect(self.add)
        self.menu_btn.clicked.connect(self.menu_button)
        self.analysis_btn.clicked.connect(self.analysis_button)
        self.logout.clicked.connect(self.logout_btn)

    def logout_btn(self):
        # self.close()
        logout = Logout()
        widget.addWidget(logout)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
             

    def add(self):
        add_btn = Add()
        widget.addWidget(add_btn)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def menu_button(self):
        menu = Menu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def analysis_button(self):
        analysis = Analysis()
        widget.addWidget(analysis)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def open_next_page(self):
        pass

class Add(QDialog):
    def __init__(self):
        super(Add,self).__init__()
        loadUi("customer.ui",self)
        global current_date 
        global total  ,I1 
        current_date = QDate.currentDate()  # Get the current date
        self.dateEdit.setDate(current_date) 

        self.submit_btn.clicked.connect(self.submit)
        self.back_btn.clicked.connect(self.back)

    def back(self):
        Home()

    def submit(self):
        connection = mysql.connector.connect(host="localhost", user="root", password="",database="restaurant")
        try:
            if connection.is_connected():
                print("Connection is Successfully")
                cursor = connection.cursor()
                phone_number = self.bt1.text()
                name = self.bt2.text()
                address = self.bt3.text()
                no_of_person = self.bt4.text()
                date_time = self.dateEdit.date().toString("yyyy-MM-dd")
                query = " INSERT INTO customer(phone_number,name,address,no_of_person,date_time)VALUE(%s,%s,%s,%s,%s)"
                value = (phone_number,name,address,no_of_person,date_time)
                cursor.execute(query, value)
                connection.commit()
                cursor.close()

            else:
                print("Failed to connect")  
        except mysql.connector.Error as error:
            print("Error:", error)
        finally:
            if 'connection' in locals():
                connection.close()


class Menu(QDialog):  
    def __init__(self):
        super(Menu, self).__init__()
        loadUi("menu.ui",self)
        global total 
        current_date = QDate.currentDate()  # Get the current date
        self.dateEdit.setDate(current_date) 
        self.find_btn.clicked.connect(self.find)
        self.reset_btn.clicked.connect(self.reset)
        self.conform_btn.clicked.connect(self.conform)
        self.order_btn.clicked.connect(self.order)
        self.back_btn.clicked.connect(self.back)

        self.total =0 
        
        self.comboBox_1.addItem('')
        self.comboBox_1.addItem("Ribeye steak, ")
        self.comboBox_1.addItem("Grilled salmon, ")
        
        self.comboBox_2.addItem('')
        self.comboBox_2.addItem("Gulab jamun, ")
        self.comboBox_2.addItem("Rasmalai,")
        self.comboBox_2.addItem("Kheer, ")
        self.comboBox_2.addItem("Gajar ka halwa, ")
        self.comboBox_2.addItem("Jalebi, ")
        self.comboBox_2.addItem("Rasgulla, ")

        self.comboBox_3.addItem('')
        self.comboBox_3.addItem("Masala chai, ")
        self.comboBox_3.addItem("Thandai, ")
        self.comboBox_3.addItem("Fresh lime soda, ")
        self.comboBox_3.addItem("Salted lassi, ")
        self.comboBox_3.addItem("Mango lassi, ")
        self.comboBox_3.addItem("Mango juice, ")
        self.comboBox_3.addItem("Buttermilk, ")
        self.comboBox_3.addItem("Jaljeera, ")

        self.comboBox_4.addItem('')
        self.comboBox_4.addItem("Mixed fruit salad with chaat masala, ")
        self.comboBox_4.addItem("Palak soup, ")
        self.comboBox_4.addItem("Lentil salad with chaat masala, ")
        self.comboBox_4.addItem("Tomato shorba, ")
        self.comboBox_4.addItem("Mulligatawny soup, ")
        self.comboBox_4.addItem("Sprout salad with chaat masala, ")
        
        self.comboBox_5.addItem('')
        self.comboBox_5.addItem("Palak paneer, ")
        self.comboBox_5.addItem("Chana masala, ")
        self.comboBox_5.addItem("Baingan bharta, ")
        self.comboBox_5.addItem("Aloo gobi, ")
        self.comboBox_5.addItem("Dal makhani, ")
        self.comboBox_5.addItem("Paneer butter masala, ")
        self.comboBox_5.addItem("Vegetable korma, ")
        self.comboBox_5.addItem("Malai kofta, ")
        self.comboBox_5.addItem("Bhindi masala,  ")
        self.comboBox_5.addItem("Rajma, ")

        self.comboBox_6.addItem("5")
        self.comboBox_6.addItem("12")
        self.comboBox_6.addItem("18")
        self.comboBox_6.addItem("28")

    def reset(self):
        self.t1.setText('')
        self.t1_2.setText('')
        self.t1_3.setText('')
        self.t1_4.setText('')
        self.t1_5.setText('')
        
        self.t2.setText('')
        self.t2_2.setText('')
        self.t2_3.setText('')
        self.t2_4.setText('')
        self.t2_5.setText('')
        
        self.t3.setText('')
        self.t3_2.setText('')
        self.t3_3.setText('')
        self.t3_4.setText('')   
        self.t3_5.setText('')
       
        self.t4.setText('')
        self.t4_2.setText('')
        self.t4_3.setText('')
        self.t4_4.setText('')
        self.t4_5.setText('')
        
        self.t5.setText('')
        self.t5_2.setText('')
        self.t5_3.setText('')
        self.t5_4.setText('')
        self.t5_5.setText('')
       
        self.input1.setText('')
        self.input2.setText('')
        self.output1.setText('')
        self.output2.setText('')

        self.spinBox_1.setValue(0)
        self.spinBox_2.setValue(0)
        self.spinBox_3.setValue(0)
        self.spinBox_4.setValue(0)
        self.spinBox_5.setValue(0)
        

    def back(self):
        Home()

    def find(self):
        connection = mysql.connector.connect(host="localhost", user="root", password="",database="restaurant")
        customer = self.input1.text()
        print(customer)
        try:
            if connection.is_connected():
                print("Connection is Successfully")               
                cursor = connection.cursor()
                query = "SELECT * FROM `customer` WHERE `phone_number` = " + customer 
                cursor.execute(query)
                results = cursor.fetchall()
                if results:
                    for row in results:
                        print(row) 
                        name = row[1]
                        # self.input1.setText(str(phone_number))
                        self.input2.setText(str(name))
                else:
                        self.input1.clear()
                        self.input2.clear()
                connection.commit()
                cursor.close()
            else:
                print("Failed to connect")  
        except mysql.connector.Error as error:
            print("Error:", error)
        finally:
            if 'connection' in locals():
                connection.close()

    def conform(self):
        total1 = 0 
        total2 = 0 
        total3 = 0 
        total4 = 0 
        total5 = 0 
        
        enterd_text1 = self.t1.text()
        enterd_text2 = self.t1_2.text()
        enterd_text3 = self.t1_3.text()
        enterd_text4 = self.t1_4.text()
        enterd_text5 = self.t1_5.text()
       
        if enterd_text1 == '':
            
            comboBox_1 = self.comboBox_1.currentText()
            self.t1.setText(comboBox_1)

            comboBox_2 = self.comboBox_2.currentText()
            self.t2.setText(comboBox_2)

            comboBox_3 = self.comboBox_3.currentText()
            self.t3.setText(comboBox_3)
            
            comboBox_4 = self.comboBox_4.currentText()
            self.t4.setText(comboBox_4)

            comboBox_5 = self.comboBox_5.currentText()
            self.t5.setText(comboBox_5)
            
                # output2 comboBox_6
            i1 = int(self.spinBox_1.text())
            i2 = int(self.spinBox_2.text())
            i3 = int(self.spinBox_3.text())
            i4 = int(self.spinBox_4.text()) 
            i5 = int(self.spinBox_5.text())
            subtotal = 100*i1 + 90*i2 + 80*i3 + 60*i4 + 30*i5
            print("Subtotal:", subtotal)
            self.output1.setText(str(subtotal))
        
            gst_rate = int(self.comboBox_6.currentText())
            print("GST Rate:", gst_rate) 
            gst_amount = subtotal * gst_rate / 100
            print("GST Amount:", gst_amount)
            self.total += subtotal + gst_amount
            print("Total:", self.total)
        
            self.output2.setText(str(self.total))
            
        elif enterd_text2 == '':
                   
            comboBox_1 = self.comboBox_1.currentText()
            self.t1_2.setText(comboBox_1)

            comboBox_2 = self.comboBox_2.currentText()
            self.t2_2.setText(comboBox_2)

            comboBox_3 = self.comboBox_3.currentText()
            self.t3_2.setText(comboBox_3)
            
            comboBox_4 = self.comboBox_4.currentText()
            self.t4_2.setText(comboBox_4)

            comboBox_5 = self.comboBox_5.currentText()
            self.t5_2.setText(comboBox_5)
            
            i1 = int(self.spinBox_1.text())
            i2 = int(self.spinBox_2.text())
            i3 = int(self.spinBox_3.text())
            i4 = int(self.spinBox_4.text()) 
            i5 = int(self.spinBox_5.text())
            subtotal = 100*i1 + 90*i2 + 80*i3 + 60*i4 + 30*i5
            print("Subtotal:", subtotal)
            self.output1.setText(str(subtotal))
        
            gst_rate = int(self.comboBox_6.currentText())
            print("GST Rate:", gst_rate) 
            gst_amount = subtotal * gst_rate / 100
            print("GST Amount:", gst_amount)
            self.total += subtotal + gst_amount
            print("Total:", self.total)
        
            self.output2.setText(str(self.total))
            
        elif enterd_text3 == '':
                      
            comboBox_1 = self.comboBox_1.currentText()
            self.t1_3.setText(comboBox_1)

            comboBox_2 = self.comboBox_2.currentText()
            self.t2_3.setText(comboBox_2)

            comboBox_3 = self.comboBox_3.currentText()
            self.t3_3.setText(comboBox_3)
            
            comboBox_4 = self.comboBox_4.currentText()
            self.t4_3.setText(comboBox_4)

            comboBox_5 = self.comboBox_5.currentText()
            self.t5_3.setText(comboBox_5)
            i1 = int(self.spinBox_1.text())
            i2 = int(self.spinBox_2.text())
            i3 = int(self.spinBox_3.text())
            i4 = int(self.spinBox_4.text()) 
            i5 = int(self.spinBox_5.text())

            subtotal = 100*i1 + 90*i2 + 80*i3 + 60*i4 + 30*i5
            print("Subtotal:", subtotal)
            self.output1.setText(str(subtotal))
        
            gst_rate = int(self.comboBox_6.currentText())
            print("GST Rate:", gst_rate) 
            gst_amount = subtotal * gst_rate / 100
            print("GST Amount:", gst_amount)
            self.total += subtotal + gst_amount
            print("Total:", self.total)
        
            self.output2.setText(str(self.total))
            
        elif enterd_text4 == '':
            
                        
            comboBox_1 = self.comboBox_1.currentText()
            self.t1_4.setText(comboBox_1)

            comboBox_2 = self.comboBox_2.currentText()
            self.t2_4.setText(comboBox_2)

            comboBox_3 = self.comboBox_3.currentText()
            self.t3_4.setText(comboBox_3)
            
            comboBox_4 = self.comboBox_4.currentText()
            self.t4_4.setText(comboBox_4)

            comboBox_5 = self.comboBox_5.currentText()
            self.t5_4.setText(comboBox_5)
            
            i1 = int(self.spinBox_1.text())
            i2 = int(self.spinBox_2.text())
            i3 = int(self.spinBox_3.text())
            i4 = int(self.spinBox_4.text()) 
            i5 = int(self.spinBox_5.text())
            subtotal = 100*i1 + 90*i2 + 80*i3 + 60*i4 + 30*i5
            print("Subtotal:", subtotal)
            self.output1.setText(str(subtotal))
        
            gst_rate = int(self.comboBox_6.currentText())
            print("GST Rate:", gst_rate) 
            gst_amount = subtotal * gst_rate / 100
            print("GST Amount:", gst_amount)
            self.total += subtotal + gst_amount
            print("Total:", self.total)
        
            self.output2.setText(str(self.total))
              
        elif enterd_text5 == '': 
            comboBox_1 = self.comboBox_1.currentText()
            self.t1_5.setText(comboBox_1)

            comboBox_2 = self.comboBox_2.currentText()
            self.t2_5.setText(comboBox_2)

            comboBox_3 = self.comboBox_3.currentText()
            self.t3_5.setText(comboBox_3)
            
            comboBox_4 = self.comboBox_4.currentText()
            self.t4_5.setText(comboBox_4)

            comboBox_5 = self.comboBox_5.currentText()
            self.t5_5.setText(comboBox_5)

            i1 = int(self.spinBox_1.text())
            i2 = int(self.spinBox_2.text())
            i3 = int(self.spinBox_3.text())
            i4 = int(self.spinBox_4.text()) 
            i5 = int(self.spinBox_5.text())
            subtotal = 100*i1 + 90*i2 + 80*i3 + 60*i4 + 30*i5
            print("Subtotal:", subtotal)
            self.output1.setText(str(subtotal))
        
            gst_rate = int(self.comboBox_6.currentText())
            print("GST Rate:", gst_rate) 
            gst_amount = subtotal * gst_rate / 100
            print("GST Amount:", gst_amount)
            self.total += subtotal + gst_amount
            print("Total:", self.total)
        
            self.output2.setText(str(self.total))
              
        else :              
            print ("all filled is find")
            self.reset()

    def order(self):
        connection = mysql.connector.connect(host="localhost", user="root", password="",database="restaurant")
        try:
            if connection.is_connected():
                print("Connected successfully") 
                cursor = connection.cursor()
                number = str(self.input1.text()) 
                customer_name = self.input2.text() 
                
                item = str(self.t1.text(),)+ str(self.t2.text(),) +str(self.t3.text(),) + str(self.t4.text(),) +str(self.t5.text())
                print(item)
                quantity = int(self.spinBox_1.value()) + int(self.spinBox_2.value()) +int(self.spinBox_3.value()) +int(self.spinBox_4.value() )+int(self.spinBox_5.value())
                amount = self.output2.text()
                date = self.dateEdit.date().toString("yyyy-MM-dd")
                query = " INSERT INTO `order`(`number`,`customer_name`,`item`,`quantity`,`amount`,`date`)VALUE(%s,%s,%s,%s,%s,%s)"
                value = (number,customer_name,item,quantity,amount,date)
                cursor.execute(query, value)
                connection.commit()
                
                cursor.close()
            else:
                print("Failed to connect")

        except mysql.connector.Error as error:
            print("Error:", error)
        finally:    
            connection.close()

class Analysis(QDialog):
    def __init__(self):
        super(Analysis, self).__init__()
        loadUi("analysis.ui",self)
        self.static_search.clicked.connect(self.analysis)
        self.back_btn.clicked.connect(self.back)
    
    def back(self):
        Home()

    def analysis(self):
        order = self.ct1.text()
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="", database="restaurant")
            if connection.is_connected():
                print("Connected successfully")
                cursor = connection.cursor()
                #query = "SELECT * FROM `issue`"
                query = query = "SELECT * FROM `order` WHERE `number` = "+ order
                cursor.execute(query)
                results = cursor.fetchall()
                for row in results:
                    print(row) 
                    number = row[0] 
                    name = row[1]
                    self.ct1.setText(str(number))
                    self.ct2.setText(str(name))

                for i in range(len(results)):
                    res = results
                    for row in res:
                        foodname = row[2]
                        quantaty = row[3]
                        amount = row[4]
                        rate = row[5]
                        if(i == 0): 
                            self.input1.setText(str(foodname))
                            self.input2.setText(str(quantaty))
                            self.input3.setText(str(amount))
                            self.input4.setText(str(rate))
                            res.pop(0)
                            break
                        elif(i == 1):   
                            self.input1_2.setText(str(foodname))
                            self.input2_2.setText(str(quantaty))
                            self.input3_2.setText(str(amount))
                            self.input4_2.setText(str(rate))
                            res.pop(0)
                            break                       
                        elif(i == 2):
                            self.input1_3.setText(str(foodname))
                            self.input2_3.setText(str(quantaty))
                            self.input3_3.setText(str(amount))
                            self.input4_3.setText(str(rate))
                            res.pop(0) 
                            break                     
                        elif(i == 3):
                            self.input1_4.setText(str(foodname))
                            self.input2_4.setText(str(quantaty))
                            self.input3_4.setText(str(amount))
                            self.input4_4.setText(str(rate))  
                            res.pop(0)
                            break                         
                        else:
                            self.input1_5.setText(str(foodname))
                            self.input2_5.setText(str(quantaty))
                            self.input3_5.setText(str(amount))
                            self.input4_5.setText(str(rate))  
                            res.pop(0)
                            break  
                                    
            else:
                print("Failed to connect")  
        except mysql.connector.Error as error:
            print("Error:", error)
        finally:
            if 'connection' in locals():
                connection.close()


app = QApplication(sys.argv)
welcome = Welcome()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()
# a = b = c = d = e =0
login = Login()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")