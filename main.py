from tkinter import *
from tkinter import messagebox
import tkinter.messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import getpass

# ****** GLOBAL VARIABLES ******

objects = []
window = Tk()
window.withdraw()
window.title('Email Storage')
emailAuto = StringVar()
passwordAuto = StringVar()  


class popupWindow(object):

    loop = False
    attempts = 0
    

    def __init__(self, master):
        top = self.top = Toplevel(master)
        top.title('Input Password')
        top.geometry('{}x{}'.format(250, 100))
        top.resizable(width=False, height=False)
        self.l = Label(top, text=" Password: ", font=('Courier', 14), justify=CENTER)
        self.l.pack()
        self.e = Entry(top, show='*', width=30)
        self.e.pack(pady=7)
        self.b = Button(top, text='Submit', command=self.cleanup, font=('Courier', 14))
        self.b.pack()

    def cleanup(self):
        self.value = self.e.get()
        access = 'password'

        if self.value == access:
            self.loop = True
            self.top.destroy()
            window.deiconify()
        else:
            self.attempts += 1
            if self.attempts == 5:
                window.quit()
            self.e .delete(0, 'end')
            messagebox.showerror('Incorrect Password', 'Incorrect password, attempts remaining: ' + str(5 - self.attempts))

class entity_add:

    def __init__(self, master, n, p, e):
        self.password = p
        self.name = n
        self.email = e
        self.window = master

    def write(self):
        f = open('data.txt', "a")
        n = self.name
        e = self.email
        p = self.password

        encryptedN = ""
        encryptedE = ""
        encryptedP = ""
        for letter in n:
            if letter == ' ':
                encryptedN += ' '
            else:
                encryptedN += chr(ord(letter) + 5)

        for letter in e:
            if letter == ' ':
                encryptedE += ' '
            else:
                encryptedE += chr(ord(letter) + 5)

        for letter in p:
            if letter == ' ':
                encryptedP += ' '
            else:
                encryptedP += chr(ord(letter) + 5)

        f.write(encryptedN + ',' + encryptedE + ',' + encryptedP + ', \n')
        f.close()


class entity_display:

    def __init__(self, master, n, e, p, i):
        self.password = p
        self.name = n
        self.email = e
        self.window = master
        self.i = i

        dencryptedN = ""
        dencryptedE = ""
        dencryptedP = ""
        for letter in self.name:
            if letter == ' ':
                dencryptedN += ' '
            else:
                dencryptedN += chr(ord(letter) - 5)

        for letter in self.email:
            if letter == ' ':
                dencryptedE += ' '
            else:
                dencryptedE += chr(ord(letter) - 5)

        for letter in self.password:
            if letter == ' ':
                dencryptedP += ' '
            else:
                dencryptedP += chr(ord(letter) - 5)

        self.label_name = Label(self.window, text=dencryptedN, font=('Courier', 14))
        self.label_email = Label(self.window, text=dencryptedE, font=('Courier', 14))
        self.label_pass = Label(self.window, text=dencryptedP, font=('Courier', 14))
        self.deleteButton = Button(self.window, text='X', fg='red', command=self.delete)

    def display(self):
        self.label_name.grid(row=6 + self.i, sticky=W)
        self.label_email.grid(row=6 + self.i, column=1)
        self.label_pass.grid(row=6 + self.i, column=2, sticky=E)
        self.deleteButton.grid(row=6 + self.i, column=3, sticky=E)

    def delete(self):
        answer = tkinter.messagebox.askquestion('Delete', 'Are you sure you want to delete this entry?')

        if answer == 'yes':
            for i in objects:
                i.destroy()

            f = open('data.txt', 'r')
            lines = f.readlines()
            f.close()

            f = open('data.txt', "w")
            count = 0

            for line in lines:
                if count != self.i:
                    f.write(line)
                    count += 1

            f.close()
            readfile()

    def destroy(self):
        self.label_name.destroy()
        self.label_email.destroy()
        self.label_pass.destroy()
        self.deleteButton.destroy()


# ******* FUNCTIONS *********

def onsubmit():
    m1 = email.get()
    p1 = password.get()
    n1 = name.get()
    e = entity_add(window, n1, p1, m1)  
    e.write()
    name.delete(0, 'end')
    email.delete(0, 'end')
    password.delete(0, 'end')
    messagebox.showinfo('Added Entity', 'Successfully Added, \n' + 'Name: ' + n1 + '\nEmail: ' + m1 + '\nPassword: ' + p1)
    readfile()


def automate():

    val1 = emailAuto.get()
    val2 = passwordAuto.get()
    print(val1)
    print(val2)

    
   # val1 = emailAuto.get()
   # val2 = passwordAuto.get()
   # usernameStr = input("> ")
   # passwordStr = getpass.getpass(prompt="> ")
   # val1 = emailAuto.get()
   # val2 = passwordAuto.get()
    

    browser = webdriver.Chrome()
   
    browser.get(('https://accounts.google.com/ServiceLogin?'
                 'service=mail&continue=https://mail.google'
                 '.com/mail/#identifier'))
    
    # fill in username and hit the next button
    
    username = browser.find_element_by_id('identifierId')
    username.send_keys(val1)
    
    nextButton = browser.find_element_by_id('identifierNext')
    nextButton.click()
    
    # wait for transition then continue to fill items
    
    password = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.NAME, "password")))
    
    password.send_keys(val2)
    
    signInButton = browser.find_element_by_id('passwordNext')
    signInButton.click()




def clearfile():
    f = open('data.txt', "w")
    f.close()


def readfile():
    f = open('data.txt', 'r')
    count = 0

    for line in f:
        entityList = line.split(',')
        e = entity_display(window, entityList[0], entityList[1], entityList[2], count)
        objects.append(e)
        e.display()
        count += 1
    f.close()




# ******* GRAPHICS *********

popupwindow = popupWindow(window)

entity_label = Label(window, text='Storage Vault', font=('Courier', 18))
name_label = Label(window, text='Name: ', font=('Courier', 14))
email_label = Label(window, text='Email: ',  font=('Courier', 14))
pass_label = Label(window, text='Password: ', font=('Courier', 14))
name = Entry(window, font=('Courier', 14))
email = Entry(window,textvariable = emailAuto, font=('Courier', 14))
password = Entry(window,textvariable = passwordAuto, show='*', font=('Courier', 14))
submit2 = Button(window, text="Open Browser", command = automate, font=('Courier', 14))
submit = Button(window, text='Add Email', command=onsubmit, font=('Courier', 14))


entity_label.grid(columnspan=3, row=0)
name_label.grid(row=1, sticky=E, padx=3)
email_label.grid(row=2, sticky=E, padx=3)
pass_label.grid(row=3, sticky=E, padx=3)

name.grid(columnspan=3, row=1, column=1, padx=2, pady=2, sticky=W)
email.grid(columnspan=3, row=2, column=1, padx=2, pady=2, sticky=W)
password.grid(columnspan=3, row=3, column=1, padx=2, pady=2, sticky=W)

submit.grid(columnspan=3, pady=4, sticky = W)
submit2.grid(columnspan=3, row =4, padx = 2, pady=2, sticky=E)

name_label2 = Label(window, text='Name: ', font=('Courier', 14))
email_label2 = Label(window, text='Email: ', font=('Courier', 14))
pass_label2 = Label(window, text='Password: ', font=('Courier', 14))

name_label2.grid(row=5)
email_label2.grid(row=5, column=1)
pass_label2.grid(row=5, column=2)

readfile()



window.mainloop()

