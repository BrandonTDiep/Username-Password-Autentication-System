import PySimpleGUI as sg
import sqlite3

con = sqlite3.connect('login.db') #***MAKE SURE TO COMMENT THIS OUT AFTER FIRST TEST RUN***

#con = sqlite3.connect(':memory:')  #***MAKE SURE TO UNCOMMENT THIS OUT AFTER FIRST TEST RUN***
cur = con.cursor() 

cur.execute("""CREATE TABLE login
(Username text, Password text)""")

cur.execute("INSERT INTO login VALUES ('jack','wordpass')")
cur.execute("INSERT INTO login VALUES ('james','password123')")
cur.execute("INSERT INTO login VALUES ('german','potato')")

con.commit()


def deleteAccount(value):
    return_statement = sg.Text()
    layout = [
        [sg.Text("Delete Account")],
        [sg.Text("Are you sure you want to delete your account?")],
        [return_statement],
        [sg.Button("Yes"), sg.Button("No")]
    ]  
    window = sg.Window("Delete Account", layout)
    while True:
        event1, value1 = window.read()
        if event1 == "Yes":
            con.execute("DELETE from login where Username = ? and Password = ?", (value[0], value[1]))
            sg.popup("Account has been deleted")
            break
        if event1 == sg.WIN_CLOSED or event1 == 'No':
            break
    window.close()
    return event1

      
def changePassword(value):
    return_statement = sg.Text()
    layout = [
        [sg.Text("Change Password")],
        [sg.Text("Current Password",size = (10,2)), sg.InputText()],
        [sg.Text("New Password",size = (10,2)), sg.InputText()],
        [sg.Text("Confirm New Password",size = (10,2)), sg.InputText()],
        [return_statement],
        [sg.Button("Enter"), sg.Button("Exit")]
    ]
    window = sg.Window("Change Password", layout)
    while True:
        event1, value1 = window.read()
        if event1 == sg.WIN_CLOSED or event1 == 'Exit':
            pwdChanged = False
            break
        if event1 == "Enter":
            if value1[0] != value[1]:
                return_statement.update(value="The password did not match our records")
                continue                            
            elif value1[2] != value1[1]:
                return_statement.update(value="Your new passwords do not match")
                continue
            else:
                cur.execute("UPDATE login SET password = ? where Username = ?", (value1[1], value[0]))
                con.commit() 
                sg.popup("Your password has been changed!")
                return_statement.update(value="Your password has been changed!")
                pwdChanged = True
                break
    window.close()
    return pwdChanged


def forgotPassword(data, value, return_statement):
    if value[0] == "":
        return_statement.update(value= "Enter your username to retrieve your passsword") 
    else:
        for row in data:
            if value[0] in row[0]:
                return_statement.update(value = row[1]) 
                break             
            else:
                return_statement.update(value= "Enter your username to retrieve your passsword")     

        
def createAccount(data):
    return_statement = sg.Text()
    layout = [
        [sg.Text("Create Account")],
        [sg.Text("Username",size = (10,1)), sg.InputText()],
        [sg.Text("Password",size = (10,1)), sg.InputText()],
        [return_statement],
        [sg.Button("Enter"), sg.Button("Exit")]
    ]
    window = sg.Window("Create New Account", layout)
    while True:
        event, value = window.read()
        if event == "Enter":
            for row in data:
                if value[0] in row[0]:
                    return_statement.update(value = "Username already exist")
                    exist = False
                    break
                else:
                    exist = True
                    continue
            if exist != False:
                cur.execute("INSERT INTO login VALUES (?, ?)", (value[0], value[1]))
                con.commit()
                data.append((value[0], value[1]))
                return_statement.update(value = "You have created a new account!")
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
    window.close()

def accountManage(value):
    return_statement = sg.Text()
    layout = [
        [sg.Text("Welcome!")],
        [sg.Text("Account Management")],
        [return_statement],
        [sg.Button("Change Password"), sg.Button("Delete Account"), sg.Button("Sign Out")]
    ]
    window = sg.Window("Account Management", layout)
    while True:
        event1, value1 = window.read()
        
        if event1 == "Change Password":
            choice = changePassword(value)
            if choice == True:
                break
            else:
                continue
            
        if event1 == "Delete Account":
            choice = deleteAccount(value)
            if choice != "Yes":
                continue
            else:
                break
            
        if event1 == sg.WIN_CLOSED or event1 == "Sign Out":
            break
    window.close()  

   
def main():
    return_statement = sg.Text()
    layout = [
        [sg.Text("Login Screen")],
        [sg.Text("Username",size = (15,1)), sg.InputText()],
        [sg.Text("Password",size = (15,1)), sg.InputText()],
        [return_statement],
        [sg.Button("Enter"), sg.Button("Exit"),sg.Button("Create Account"), sg.Button("Forgot Password")]
    ]
    window = sg.Window("Login Portal", layout)


    while True:             
        event, value = window.read()
        
        cursorS = con.execute("SELECT * from login") 
        data = cursorS.fetchall()
        
        cursorS = con.execute("SELECT ?, ? from login", (value[0], value[1])) 
        loginInfo = cursorS.fetchone()

        if event == sg.WIN_CLOSED or event == "Exit":
            break
        if event == "Enter":
            if loginInfo in data:
                return_statement.update(value = "The password was correct! You are now logged in.")
                accountManage(value)
            else:
                return_statement.update(value = "The Username or password you entered does not exist or is incorrect")
                
        if event == "Create Account":
            createAccount(data)
          
        if event == "Forgot Password":
            forgotPassword(data, value, return_statement)
            
    window.close()
    
    cursorS = con.execute("SELECT Username, Password from login")
    for row in cursorS:
        print("Username:", row [0], "| Password:", row[1])
        
if __name__ == "__main__":
    main()
    
    






    
    
    
    
    
    
