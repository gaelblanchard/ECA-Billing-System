#Gael Blanchard
#Implementing a GUI which uses an underlying SQL database to graph data, search data and create data
#Tkinter,Matplotlib,
from tkinter import *
import tkinter.messagebox as tkMessageBox
import sqlite3
import tkinter.ttk as ttk
import sqlite3
import numpy as np
import matplotlib
matplotlib.use('TkAgg') #line is necessary to use both tkinter and matplotlib together
import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple

root = Tk()
root.title("ECA Billing System")

tkvar = StringVar(root)

width = 1200
height = 820
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.config(bg="#B2D2D3")

#========================================VARIABLES========================================
USERNAME = StringVar()
PASSWORD = StringVar()

PATIENT_ID = IntVar()
LAST_NAME = StringVar()
FIRST_NAME = StringVar()
DATE_OF_BIRTH = StringVar()
GENDER = StringVar()
INS_ID = StringVar()
ADDRESS = StringVar()
PAT_INS = StringVar()
EMAIL = StringVar()
PHONE = StringVar()

GIVEN_DATE = StringVar()

SEARCH = StringVar()
SEARCH_TYPE = StringVar()

BILLING_ID = IntVar()
SURGEON_NAME = StringVar()
BILLING_TYPE = StringVar()
DATE_OF_SERV = StringVar()
# LAST_NAME = StringVar()
# FIRST_NAME = StringVar()
DOB = StringVar()
# INS_NAME = StringVar()
PAT_ID = IntVar()
PATI_ID = IntVar()
BILLING_DATE = StringVar()
BILLING_AMOUNT = IntVar()
PAID_DATE = StringVar()
PAID_AMOUNT = IntVar()
MONTH = IntVar()

#Set variables for month so that we can perform sql queries easily
January = 1
February = 2
March = 3
April = 4
May = 5
June = 6
July = 7
August = 8
September = 9
October = 10
November = 11
December = 12

#========================================METHODS==========================================
#defines each of our databases and enters from csv our pre existing data
def Database():
    global conn, cursor
    conn = sqlite3.connect("clinic_final.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `admin` (admin_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS patient2 (Patient_id INT NOT NULL, LastName VARCHAR(255) NOT NULL, FirstName VARCHAR(255) NOT NULL, DateOfBirth DATE NOT NULL, Sex CHAR(1),Address VARCHAR(255), Insurance_id INT, PatientInsurance_id INT NOT NULL,PhoneNumber INT, Email VARCHAR(255), FOREIGN KEY(Insurance_id) REFERENCES insurance(Insurance_id), PRIMARY KEY(Patient_id));")
    cursor.execute("CREATE TABLE IF NOT EXISTS insurance (Insurance_id INT NOT NULL, Name VARCHAR(255), InsuranceType VARCHAR(255), PRIMARY KEY(Insurance_id));")
    with open('patient.csv','rt') as fin:
        dr = csv.DictReader(fin)
        #i[col1] for every column into 
        to_db = [(i['Patient_id'],i['LastName'],i['FirstName'],i['DateOfBirth'],i['Sex'],i['Address'],i['Insurance_id'],i['PatientInsurance_id'],i['PhoneNumber'],i['Email']) for i in dr]

    cursor.executemany("INSERT OR IGNORE INTO patient2 (Patient_id, LastName,FirstName,DateOfBirth,Sex,Address,Insurance_id,PatientInsurance_id,PhoneNumber,Email) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
    cursor.execute("CREATE TABLE IF NOT EXISTS billing (Case_id INT NOT NULL, SurgeonName VARCHAR(255), DateOfService DATE, Patient_id INT, PatientInsurance_id INT, BillingDate DATE, BillingAmount INT,PaidDate DATE, PaidAmount INT, Month INT, FOREIGN KEY(Patient_id) REFERENCES patient(Patient_id), FOREIGN KEY(PatientInsurance_id) REFERENCES patient(PatientInsurance_id), PRIMARY KEY(Case_id));")
    with open('billing.csv','rt') as fin:
        dr = csv.DictReader(fin)
        #i[col1] for every column into 
        to_db = [(i['Case_id'],i['SurgeonName'],i['DateOfService'],i['Patient_id'],i['PatientInsurance_id'],i['BillingDate'],i['BillingAmount'],i['PaidDate'],i['PaidAmount'],i['Month']) for i in dr]

    cursor.executemany("INSERT OR IGNORE INTO billing (Case_id, SurgeonName,DateOfService,Patient_id,PatientInsurance_id,BillingDate,BillingAmount,PaidDate,PaidAmount,Month) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?);", to_db)
    with open('insurance.csv','rt') as fin:
        dr = csv.DictReader(fin)
        #i[col1] for every column into 
        to_db = [(i['Insurance_id'],i['Name'],i['InsuranceType']) for i in dr]
    cursor.executemany("INSERT OR IGNORE INTO insurance (Insurance_id, Name,InsuranceType) VALUES (?, ?, ?);", to_db)
    cursor.execute("SELECT * FROM `admin` WHERE `username` = 'admin' AND `password` = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `admin` (username, password) VALUES('admin', 'admin')")
        conn.commit()

def Exit():
    result = tkMessageBox.askquestion('ECA Billing System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()

def Exit2():
    result = tkMessageBox.askquestion('ECA Billing System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        Home.destroy()
        exit()

def ShowLoginForm():
    global loginform
    loginform = Toplevel()
    loginform.title("ECA Billing System/Account Login")
    width = 600
    height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    loginform.resizable(0, 0)
    loginform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    LoginForm()
    
def LoginForm():
    global lbl_result
    TopLoginForm = Frame(loginform, width=600, height=100, bd=1, relief=SOLID)
    TopLoginForm.pack(side=TOP, pady=20)
    lbl_text = Label(TopLoginForm, text="Administrator Login", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    MidLoginForm = Frame(loginform, width=600)
    MidLoginForm.pack(side=TOP, pady=50)
    lbl_username = Label(MidLoginForm, text="Username:", font=('arial', 18), bd=18)
    lbl_username.grid(row=0)
    lbl_password = Label(MidLoginForm, text="Password:", font=('arial', 18), bd=18)
    lbl_password.grid(row=1)
    lbl_result = Label(MidLoginForm, text="", font=('arial', 18))
    lbl_result.grid(row=3, columnspan=2)
    username = Entry(MidLoginForm, textvariable=USERNAME, font=('arial', 18), width=15)
    username.grid(row=0, column=1)
    password = Entry(MidLoginForm, textvariable=PASSWORD, font=('arial', 18), width=15, show="*")
    password.grid(row=1, column=1)
    btn_login = Button(MidLoginForm, text="Login", font=('arial', 18), width=20, command=Login)
    btn_login.grid(row=2, columnspan=2, pady=20)
    btn_login.bind('<Return>', Login)
    
def Home():
    global Home
    Home = Tk()
    Home.title("ECA Billing System/Home")
    width = 1240
    height = 820
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    Home.geometry("%dx%d+%d+%d" % (width, height, x, y))
    Home.resizable(0, 0)
    Title = Frame(Home, bd=2, relief=SOLID)
    Title.pack(pady=10)
    lbl_display = Label(Title, text="ECA Billing System", font=('arial', 24))
    lbl_display.pack()
    menubar = Menu(Home)

    filemenu = Menu(menubar, tearoff=0)
    filemenu2 = Menu(menubar, tearoff=0)
    filemenu3 = Menu(menubar, tearoff=0)
    filemenu4 = Menu(menubar, tearoff=0)
    filemenu5 = Menu(menubar, tearoff=0)
    filemenu6 = Menu(menubar, tearoff=0)

    filemenu.add_command(label="Logout", command=Logout)
    filemenu.add_command(label="Exit", command=Exit2)

    filemenu2.add_command(label="Add new", command=ShowAddNew)
    filemenu2.add_command(label="View", command=ShowView)
    filemenu2.add_command(label="Graph", command=graph_patients)

    filemenu3.add_command(label="Add new", command=ShowAddNew)
    filemenu3.add_command(label="View", command=ShowView)
    filemenu3.add_command(label="Graph", command=graph_insurance)
    #insurance type by month
    filemenu3.add_command(label="Graph by Given Month", command=ShowAddGraph)

    filemenu4.add_command(label="Add new", command=ShowAddNewBilling)
    filemenu4.add_command(label="View", command=ShowViewBilling)

    filemenu5.add_command(label="Payment Surgeon Wise", command=ShowAddNew)
    filemenu5.add_command(label="Payment by Date", command=ShowView)

    filemenu6.add_command(label="Exit", command=Exit)

    menubar.add_cascade(label="Account", menu=filemenu)
    menubar.add_cascade(label="Patient", menu=filemenu2)
    menubar.add_cascade(label="Insurance", menu=filemenu3)
    menubar.add_cascade(label="Billing", menu=filemenu4)
    menubar.add_cascade(label="Reports", menu=filemenu5)
    menubar.add_cascade(label="Exit", menu=filemenu6)
    
    Home.config(menu=menubar)
    Home.config(bg="#B8BCDB")

#GRAPHING FUNCTION BEGIN
def graph_patient(n_results,n_prices,n_std,n_labels):
    n_groups = n_results
    average_patient = n_prices
    std_men = n_std
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.45
    opacity = 0.4
    error_config = {'ecolor': '0.3'}
    rects1 = ax.bar(index, average_patient, bar_width,
                    alpha=opacity, color='b',
                    yerr=std_men, error_kw=error_config,
                    label='Patients')
    #Axes of the graph
    ax.set_xlabel('Patient')
    ax.set_ylabel('Amount') 
    #Title
    ax.set_title('Amount for patients per visit')
    ax.set_xticks(index + bar_width / 2)
    #Can set given names
    ax.set_xticklabels(n_labels)
    ax.legend()
    fig.tight_layout()
    plt.show()


def graph_patients():
    conn = sqlite3.connect('clinic_final.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT LastName, BillingAmount FROM patient2 INNER JOIN billing on patient2.Patient_id=billing.Patient_id;")
    rows = c.fetchall()
    data_count = 0
    list_prices = []
    list_names = []
    list_std = []
    for row in rows:
        count = len(row)
        print(count)
        if row[0]!='':
            data_count = data_count + 1
            list_std.append(0)
            #This is returned to the graph for graphing
        for i in range(count):
            if row[i] == '':
                break
            if i == 0:
                print(row[i])
                list_names.append(row[i])
            if i == 1:
                print(row[i])
                list_prices.append(row[i])
    graph_patient(data_count,tuple(list_prices),tuple(list_std),tuple(list_names))

def graph_ins(n_results,n_prices,n_std,n_labels):
    n_groups = n_results
    average_ins = n_prices
    std_men = n_std
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.45
    opacity = 0.4
    error_config = {'ecolor': '0.3'}
    rects1 = ax.bar(index, average_ins, bar_width,
                    alpha=opacity, color='r',
                    yerr=std_men, error_kw=error_config,
                    label='Insurance Companies')
    #Axes of the graph
    ax.set_xlabel('Insurance')
    ax.set_ylabel('Amount')
    #Title
    ax.set_title('Average Insurance Costs per month')
    ax.set_xticks(index + bar_width / 2)
    #Can set given names
    ax.set_xticklabels(n_labels)
    ax.legend()
    fig.tight_layout()
    plt.show()

def graph_ins_type(n_results,n_prices,n_std,n_labels):
    n_groups = n_results
    average_ins = n_prices
    std_men = n_std
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.5
    opacity = 0.4
    error_config = {'ecolor': '0.3'}
    rects1 = ax.bar(index, average_ins, bar_width,
                    alpha=opacity, color='b',
                    yerr=std_men, error_kw=error_config,
                    label='Insurance Type')
    #Axes of the graph
    ax.set_xlabel('Insurance Type')
    ax.set_ylabel('Amount')
    #Title
    ax.set_title('Average Costs by Insurance Type for the given month')
    ax.set_xticks(index + bar_width / 2)
    #Can set given names
    ax.set_xticklabels(n_labels)
    ax.legend()
    fig.tight_layout()
    plt.show()


def graph_insurance_type_by_month(given_date):
    conn = sqlite3.connect('clinic_final.db')
    c = conn.cursor()
    print("The given date")
    print(given_date)
    c.execute('SELECT DISTINCT InsuranceType, sum(PaidAmount), Month FROM insurance INNER JOIN billing on insurance.insurance_id=billing.PatientInsurance_id WHERE month=(?) GROUP BY month, InsuranceType;',(int(given_date),))
    rows = c.fetchall()
    data_count = 0
    list_prices = []
    list_names = []
    list_std = []
    for row in rows:
        count = len(row)
        if row[0]!='':
            data_count = data_count + 1
            list_std.append(0)
            #This is returned to the graph for graphing
        for i in range(count):
            if row[i] == '':
                break
            if i == 0:
                zeta = row[0]
                list_names.append(zeta)
            if i == 1:
                list_prices.append(row[i])
    graph_ins_type(data_count,tuple(list_prices),tuple(list_std),tuple(list_names))

def ret_ibm():
    if tkvar.get() == 'January':
        date=January
    if tkvar.get() == 'February':
        date=February
    if tkvar.get() == 'March':
        date=March
    if tkvar.get() == 'April':
        date=April
    if tkvar.get() == 'May':
        date=May
    if tkvar.get() == 'June':
        date=June
    if tkvar.get() == 'July':
        date=July
    if tkvar.get() == 'August':
        date=August
    if tkvar.get() == 'September':
        date=September
    if tkvar.get() == 'October':
        date=October
    if tkvar.get() == 'November':
        date=November
    if tkvar.get() == 'December':
        date=December
    graph_insurance_type_by_month(date)

def ShowAddGraph():
    global graphForm
    graphForm = Toplevel()
    graphForm.title("Graph by Month")
    width = 600
    height = 850
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    graphForm.geometry("%dx%d+%d+%d" % (width, height, x, y))
    graphForm.resizable(0, 0)
    AddNewGraph()

def change_dropdown(*args):
    if tkvar.get() == 'January':
        date = January
    if tkvar.get() == 'February':
        date = February
    if tkvar.get() == 'March':
        date = March
    if tkvar.get() == 'April':
        date = April
    if tkvar.get() == 'May':
        date = May
    if tkvar.get() == 'June':
        date = June
    if tkvar.get() == 'July':
        date = July
    if tkvar.get() == 'August':
        date = August
    if tkvar.get() == 'September':
        date = September
    if tkvar.get() == 'October':
        date = October
    if tkvar.get() == 'November':
        date = November
    if tkvar.get() == 'December':
        date = December

def AddNewGraph():
    TopAddGraph = Frame(graphForm, width=600, height=100, bd=1, relief = SOLID)
    TopAddGraph.pack(side=TOP, pady=20)
    lbl_text = Label(TopAddGraph, text = "Enter given month you want to search", font=('arial',18), width=600)
    lbl_text.pack(fill=X)
    MidAddGraph = Frame(graphForm, width=600)
    MidAddGraph.pack(side=TOP, pady=50)

    lbl_givendate = Label(MidAddGraph, text="Enter desired month:", font=('arial',16),bd = 10)
    lbl_givendate.grid(row=0,sticky=W)
    # Dictionary with options
    choices = { 'January','February','March','April','May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'}
    tkvar.set('January') # set the default option

    popupMenu = OptionMenu(MidAddGraph, tkvar, *choices)
    popupMenu.grid(row = 0, column =1)
    ibutton = Button(MidAddGraph, text="Retrieve Insurance by Month", command = ret_ibm)
    ibutton.grid(row=1,column=1)

    tkvar.trace('w', change_dropdown)

def graph_insurance():
    conn = sqlite3.connect('clinic_final.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT Name, avg(PaidAmount) FROM insurance INNER JOIN billing on insurance.insurance_id=billing.PatientInsurance_id GROUP BY Name;")
    rows = c.fetchall()
    data_count = 0
    list_prices = []
    list_names = []
    list_std = []
    for row in rows:
        count = len(row)
        print(count)
        if row[0]!='':
            data_count = data_count + 1
            list_std.append(0)
            #This is returned to the graph for graphing
        for i in range(count):
            if row[i] == '':
                break
            if i == 0:
                print(row[i])
                list_names.append(row[i])
            if i == 1:
                print(row[i])
                list_prices.append(row[i])
    graph_ins(data_count,tuple(list_prices),tuple(list_std),tuple(list_names))
#GRAPHING FUNCTION END
# Patient Add New and View Records -------  Starts here --------

def ShowAddNew():
    global addnewform
    addnewform = Toplevel()
    addnewform.title("ECA Billing System/Add new")
    width = 600
    height = 850
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    addnewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    addnewform.resizable(0, 0)
    AddNewForm()

def AddNewForm():
    TopAddNew = Frame(addnewform, width=600, height=100, bd=1, relief=SOLID)
    TopAddNew.pack(side=TOP, pady=20)
    lbl_text = Label(TopAddNew, text="Add New Patient", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    MidAddNew = Frame(addnewform, width=600)
    MidAddNew.pack(side=TOP, pady=50)


    lbl_patientid = Label(MidAddNew, text="Patient ID:", font=('arial', 16), bd=10)
    lbl_patientid.grid(row=0, sticky=W)
    
    lbl_lastname = Label(MidAddNew, text="Last Name:", font=('arial', 16), bd=10)
    lbl_lastname.grid(row=1, sticky=W)

    lbl_firstname = Label(MidAddNew, text="First Name:", font=('arial', 16), bd=10)
    lbl_firstname.grid(row=2, sticky=W)

    lbl_dateofbirth = Label(MidAddNew, text="Date of Birth:", font=('arial', 16), bd=10)
    lbl_dateofbirth.grid(row=3, sticky=W)

    lbl_gender = Label(MidAddNew, text="Gender:", font=('arial', 16), bd=10)
    lbl_gender.grid(row=4, sticky=W)

    lbl_insname = Label(MidAddNew, text="Address:", font=('arial', 16), bd=10)
    lbl_insname.grid(row=5, sticky=W)

    lbl_insid = Label(MidAddNew, text="Insurance ID:", font=('arial', 16), bd=10)
    lbl_insid.grid(row=6, sticky=W)

    lbl_address = Label(MidAddNew, text="Patient Insurance ID:", font=('arial', 16), bd=10)
    lbl_address.grid(row=7, sticky=W)

    lbl_city = Label(MidAddNew, text="Phone Number:", font=('arial', 16), bd=10)
    lbl_city.grid(row=8, sticky=W)

    lbl_state = Label(MidAddNew, text="Email:", font=('arial', 16), bd=10)
    lbl_state.grid(row=9, sticky=W)


    ptid = Entry(MidAddNew, textvariable=PATIENT_ID, font=('arial', 16), width=15)
    ptid.grid(row=0, column=1)
    
    ptlastname = Entry(MidAddNew, textvariable=LAST_NAME, font=('arial', 16), width=15)
    ptlastname.grid(row=1, column=1)
    
    ptfirstname = Entry(MidAddNew, textvariable=FIRST_NAME, font=('arial', 16), width=15)
    ptfirstname.grid(row=2, column=1)
    
    ptdateofbirth = Entry(MidAddNew, textvariable=DATE_OF_BIRTH, font=('arial', 16), width=15)
    ptdateofbirth.grid(row=3, column=1)

    ptgender = Entry(MidAddNew, textvariable=GENDER, font=('arial', 16), width=15)
    ptgender.grid(row=4, column=1)

    ptinsname = Entry(MidAddNew, textvariable=ADDRESS, font=('arial', 16), width=15)
    ptinsname.grid(row=5, column=1)

    ptinsid = Entry(MidAddNew, textvariable=INS_ID, font=('arial', 16), width=15)
    ptinsid.grid(row=6, column=1)

    ptaddress = Entry(MidAddNew, textvariable=PAT_INS, font=('arial', 16), width=15)
    ptaddress.grid(row=7, column=1)

    ptcity = Entry(MidAddNew, textvariable=PHONE, font=('arial', 16), width=15)
    ptcity.grid(row=8, column=1)

    ptstate = Entry(MidAddNew, textvariable=EMAIL, font=('arial', 16), width=15)
    ptstate.grid(row=9, column=1)

    btn_add = Button(MidAddNew, text="Save", font=('arial', 16), width=50, bg="#009ACD", command=AddNew)
    btn_add.grid(row=15, columnspan=2, pady=20)

def AddNew():
    Database()
    cursor.execute("INSERT INTO patient2 (Patient_id, LastName, FirstName, DateOfBirth, Sex, Address, Insurance_id, PatientInsurance_id, PhoneNumber, Email) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (int(PATIENT_ID.get()), str(LAST_NAME.get()), str(FIRST_NAME.get()), str(DATE_OF_BIRTH.get()), str(GENDER.get()), str(ADDRESS.get()), int(INS_ID.get()), int(PAT_INS.get()), int(PHONE.get()), str(EMAIL.get())))
    conn.commit()

    PATIENT_ID.set("")
    LAST_NAME.set("")
    FIRST_NAME.set("")
    DATE_OF_BIRTH.set("")
    GENDER.set("")
    ADDRESS.set("")
    INS_ID.set("")
    PAT_INS.set("")
    PHONE.set("")  
    EMAIL.set("") 
    cursor.close()
    conn.close()

def ViewForm():
    global tree
    TopViewForm = Frame(viewform, width=600, bd=1, relief=SOLID)
    TopViewForm.pack(side=TOP, fill=X)
    LeftViewForm = Frame(viewform, width=300)
    LeftViewForm.pack(side=LEFT, fill=Y)
    MidViewForm = Frame(viewform, width=600)
    MidViewForm.pack(side=RIGHT)
    
    lbl_text = Label(TopViewForm, text="View Patient", font=('arial', 18), width=300)
    lbl_text.pack(fill=X)
    
    lbl_txtsearch = Label(LeftViewForm, text="Search-LAST NAME", font=('arial', 12))
    lbl_txtsearch.pack(side=TOP, anchor=W)
    search = Entry(LeftViewForm, textvariable=SEARCH, font=('arial', 15), width=10)
    search.pack(side=TOP,  padx=10, fill=X)
    btn_search = Button(LeftViewForm, text="Search", command=Search)
    btn_search.pack(side=TOP, padx=10, pady=10, fill=X)

    # lbl_txtsearch_f = Label(LeftViewForm, text="Search-FIRST NAME", font=('arial', 12))
    # lbl_txtsearch_f.pack(side=TOP, anchor=W)
    # search = Entry(LeftViewForm, textvariable=SEARCH_F, font=('arial', 15), width=10)
    # search.pack(side=TOP,  padx=10, fill=X)
    # btn_search_f = Button(LeftViewForm, text="Search_f", command=Search_first)
    # btn_search_f.pack(side=TOP, padx=10, pady=10, fill=X)

    btn_reset = Button(LeftViewForm, text="Reset", command=Reset)
    btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_delete = Button(LeftViewForm, text="Delete", command=Delete)
    btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
    scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
    tree = ttk.Treeview(MidViewForm, columns=("Patient ID", "Last Name", "First Name", "Date of Birth", "Gender", "Address","Insurance ID","Patient Insurance ID","Phone Number","Email"), selectmode="extended", height=200, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('Patient ID', text="Patient ID",anchor=W)
    tree.heading('Last Name', text="Last Name",anchor=W)
    tree.heading('First Name', text="First Name",anchor=W)
    tree.heading('Date of Birth', text="Date of Birth",anchor=W)
    tree.heading('Gender', text="Gender",anchor=W)
    tree.heading('Address', text="Address",anchor=W)
    tree.heading('Insurance ID', text="Insurance ID",anchor=W)
    tree.heading('Patient Insurance ID', text="Patient Insurance ID",anchor=W)
    tree.heading('Phone Number', text="Phone Number",anchor=W)
    tree.heading('Email', text="Email",anchor=W)

    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=60)     #   Patient ID
    tree.column('#2', stretch=NO, minwidth=0, width=120)    #   Last Name
    tree.column('#3', stretch=NO, minwidth=0, width=120)    #   First Name
    tree.column('#4', stretch=NO, minwidth=0, width=120)    #   Date of Birth   
    tree.column('#5', stretch=NO, minwidth=0, width=50)     #   Gender
    tree.column('#6', stretch=NO, minwidth=0, width=120)    #   Address
    tree.column('#7', stretch=NO, minwidth=0, width=100)    #   Insurance ID
    tree.column('#8', stretch=NO, minwidth=0, width=190)    #   Patient Insurance ID
    tree.column('#9', stretch=NO, minwidth=0, width=100)    #   Phone Number
    tree.column('#10', stretch=NO, minwidth=0, width=50)    #   Email

    tree.pack()
    DisplayData()

def DisplayData():
    Database()
    cursor.execute("SELECT * FROM patient2")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

def Search():
    if SEARCH.get() != "":
        tree.delete(*tree.get_children())
        Database()
        cursor.execute("SELECT * FROM patient2 WHERE LastName LIKE ?", ('%'+str(SEARCH.get())+'%',))
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

def Reset():
    tree.delete(*tree.get_children())
    DisplayData()
    SEARCH.set("")

def Delete():
    if not tree.selection():
       print("ERROR")
    else:
        result = tkMessageBox.askquestion('ECA Billing System', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            Database()
            cursor.execute("DELETE FROM patient2 WHERE PATIENT_ID = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()
    
def ShowView():
    global viewform
    viewform = Toplevel()
    viewform.title("ECA Billing System/View Patient")
    width = 1400
    height = 900
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    viewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    viewform.resizable(0, 0)
    ViewForm()

# Patient Add New and View Records -------  ENDS here --------

# BILLING Add New and View Records -------  Starts here --------

def ShowAddNewBilling():
    global addnewformBilling
    addnewformBilling = Toplevel()
    addnewformBilling.title("ECA Billing System/Add Billing Entry")
    width = 600
    height = 850
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    addnewformBilling.geometry("%dx%d+%d+%d" % (width, height, x, y))
    addnewformBilling.resizable(0, 0)
    AddNewFormBilling()

def AddNewFormBilling():
    TopAddNew = Frame(addnewformBilling, width=600, height=100, bd=1, relief=SOLID)
    TopAddNew.pack(side=TOP, pady=20)
    lbl_text = Label(TopAddNew, text="Add New Billing Entry", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    MidAddNew = Frame(addnewformBilling, width=600)
    MidAddNew.pack(side=TOP, pady=50)

    lbl_billingid = Label(MidAddNew, text="Billing Case ID:", font=('arial', 16), bd=10)
    lbl_billingid.grid(row=0, sticky=W)

    lbl_surgeonname = Label(MidAddNew, text="Name of Surgeon:", font=('arial', 16), bd=10)
    lbl_surgeonname.grid(row=1, sticky=W)
    
    lbl_dos = Label(MidAddNew, text="Date of Service:", font=('arial', 16), bd=10)
    lbl_dos.grid(row=2, sticky=W)

    lbl_insid = Label(MidAddNew, text="Patient ID:", font=('arial', 16), bd=10)
    lbl_insid.grid(row=3, sticky=W)

    lbl_patid = Label(MidAddNew, text="Patient Insurance ID:", font=('arial', 16), bd=10)
    lbl_patid.grid(row=4, sticky=W)
    
    lbl_billingdate = Label(MidAddNew, text="Billing Date:", font=('arial', 16), bd=10)
    lbl_billingdate.grid(row=5, sticky=W)

    lbl_billingamt = Label(MidAddNew, text="Billing Amount:", font=('arial', 16), bd=10)
    lbl_billingamt.grid(row=6, sticky=W)

    lbl_paiddate = Label(MidAddNew, text="Paid Date:", font=('arial', 16), bd=10)
    lbl_paiddate.grid(row=7, sticky=W)

    lbl_paidamount = Label(MidAddNew, text="Paid Amount:", font=('arial', 16), bd=10)
    lbl_paidamount.grid(row=8, sticky=W)

    lbl_month = Label(MidAddNew, text="Month:", font=('arial', 16), bd=10)
    lbl_month.grid(row=9, sticky=W)

    
    bill_id = Entry(MidAddNew, textvariable=BILLING_ID, font=('arial', 16), width=15)
    bill_id.grid(row=0, column=1)
    
    bill_surgeon = Entry(MidAddNew, textvariable=SURGEON_NAME, font=('arial', 16), width=15)
    bill_surgeon.grid(row=1, column=1)
    
    bill_dos = Entry(MidAddNew, textvariable=DATE_OF_SERV, font=('arial', 16), width=15)
    bill_dos.grid(row=2, column=1)

    bill_ins_id = Entry(MidAddNew, textvariable=PAT_ID, font=('arial', 16), width=15)
    bill_ins_id.grid(row=3, column=1)

    bill_pins_id = Entry(MidAddNew, textvariable=PATI_ID, font=('arial', 16), width=15)
    bill_pins_id.grid(row=4, column=1)

    bill_date = Entry(MidAddNew, textvariable=BILLING_DATE, font=('arial', 16), width=15)
    bill_date.grid(row=5, column=1)

    bill_amount = Entry(MidAddNew, textvariable=BILLING_AMOUNT, font=('arial', 16), width=15)
    bill_amount.grid(row=6, column=1)

    bill_paid_date = Entry(MidAddNew, textvariable=PAID_DATE, font=('arial', 16), width=15)
    bill_paid_date.grid(row=7, column=1)

    bill_paid_amount = Entry(MidAddNew, textvariable=PAID_AMOUNT, font=('arial', 16), width=15)
    bill_paid_amount.grid(row=8, column=1)

    bill_month = Entry(MidAddNew, textvariable=MONTH, font=('arial', 16), width=15)
    bill_month.grid(row=9, column=1)

    btn_add = Button(MidAddNew, text="Save", font=('arial', 16), width=50, bg="#009ACD", command=AddNewBilling)
    btn_add.grid(row=14, columnspan=2, pady=20)

def AddNewBilling():
    Database()
    cursor.execute("INSERT INTO billing (Case_id, SurgeonName,DateOfService,Patient_id,PatientInsurance_id,BillingDate,BillingAmount,PaidDate,PaidAmount,Month) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (int(BILLING_ID.get()), str(SURGEON_NAME.get()), str(DATE_OF_SERV.get()), str(PAT_ID.get()), str(PATI_ID.get()), str(BILLING_DATE.get()), str(BILLING_AMOUNT.get()), str(PAID_DATE.get()), str(PAID_AMOUNT.get()), str(MONTH.get())))
    conn.commit()

    BILLING_ID.set("")
    SURGEON_NAME.set("")
    DATE_OF_SERV.set("")
    PAT_ID.set("")
    PATI_ID.set("")
    BILLING_DATE.set("")
    BILLING_AMOUNT.set("")
    PAID_DATE.set("")
    PAID_AMOUNT.set("")
    MONTH.set("")
    cursor.close()
    conn.close()

def ViewFormBilling():
    global tree
    TopViewFormBilling = Frame(viewformBilling, width=600, bd=1, relief=SOLID)
    TopViewFormBilling.pack(side=TOP, fill=X)
    LeftViewFormBilling = Frame(viewformBilling, width=300)
    LeftViewFormBilling.pack(side=LEFT, fill=Y)
    MidViewFormBilling = Frame(viewformBilling, width=600)
    MidViewFormBilling.pack(side=RIGHT)
    
    lbl_textBilling = Label(TopViewFormBilling, text="View BILLING", font=('arial', 18), width=300)
    lbl_textBilling.pack(fill=X)
    
    lbl_txtsearchBilling = Label(LeftViewFormBilling, text="Search-INSURANCE ID", font=('arial', 12))
    lbl_txtsearchBilling.pack(side=TOP, anchor=W)
    searchBilling = Entry(LeftViewFormBilling, textvariable=SEARCH, font=('arial', 15), width=10)
    searchBilling.pack(side=TOP,  padx=10, fill=X)
    btn_searchBilling = Button(LeftViewFormBilling, text="Search", command=SearchBilling)
    btn_searchBilling.pack(side=TOP, padx=10, pady=10, fill=X)

    lbl_txtsearchType = Label(LeftViewFormBilling, text="Search-DATE OF SERVICE", font=('arial', 12))
    lbl_txtsearchType.pack(side=TOP, anchor=W)
    searchType = Entry(LeftViewFormBilling, textvariable=SEARCH_TYPE, font=('arial', 15), width=10)
    searchType.pack(side=TOP,  padx=10, fill=X)
    btn_searchType = Button(LeftViewFormBilling, text="SearchType", command=SearchType)
    btn_searchType.pack(side=TOP, padx=10, pady=10, fill=X)

    btn_reset = Button(LeftViewFormBilling, text="Reset", command=ResetBilling)
    btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_delete = Button(LeftViewFormBilling, text="Delete", command=DeleteBilling)
    btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
    scrollbarx = Scrollbar(MidViewFormBilling, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidViewFormBilling, orient=VERTICAL)
    tree = ttk.Treeview(MidViewFormBilling, columns=("Billing ID", "Surgeon Name", "Date of Serv","Patient ID","Patient Insurance ID","Billing Date","Billing Amount","Paid Date","Paid Amount","Month"), selectmode="extended", height=200, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('Billing ID', text="Billing ID",anchor=W)
    tree.heading('Surgeon Name', text="Surgeon Name",anchor=W)
    tree.heading('Date of Serv', text="Date of Serv",anchor=W)
    tree.heading('Patient ID', text="Patient ID",anchor=W)
    tree.heading('Patient Insurance ID', text="Patient Insurance ID",anchor=W)
    tree.heading('Billing Date', text="Billing Date",anchor=W)
    tree.heading('Billing Amount', text="Billing Amount",anchor=W)
    tree.heading('Paid Date', text="Paid Date",anchor=W)
    tree.heading('Paid Amount', text="Paid Amount",anchor=W)
    tree.heading('Month', text="Month",anchor=W)
    
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=60)     
    tree.column('#2', stretch=NO, minwidth=0, width=130)   
    tree.column('#3', stretch=NO, minwidth=0, width=90)   
    tree.column('#4', stretch=NO, minwidth=0, width=90)    
    tree.column('#5', stretch=NO, minwidth=0, width=120)    
    tree.column('#6', stretch=NO, minwidth=0, width=120)     
    tree.column('#7', stretch=NO, minwidth=0, width=90)     
    tree.column('#8', stretch=NO, minwidth=0, width=160)    
    tree.column('#9', stretch=NO, minwidth=0, width=120)    
    tree.column('#10', stretch=NO, minwidth=0, width=90)    
    tree.pack()
    DisplayDataBilling()

def DisplayDataBilling():
    Database()
    cursor.execute("SELECT * FROM billing")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

def SearchBilling():
    if SEARCH.get() != "":
        tree.delete(*tree.get_children())
        Database()
        cursor.execute("SELECT * FROM billing WHERE PatientInsurance_id LIKE ?", ('%'+str(SEARCH.get())+'%',))
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

def SearchType():
    if SEARCH_TYPE.get() != "":
        tree.delete(*tree.get_children())
        Database()
        cursor.execute("SELECT * FROM billing WHERE DateOfService LIKE ?", ('%'+str(SEARCH_TYPE.get())+'%',))
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

def ResetBilling():
    tree.delete(*tree.get_children())
    DisplayDataBilling()
    SEARCH.set("")

def DeleteBilling():
    if not tree.selection():
       print("ERROR")
    else:
        result = tkMessageBox.askquestion('ECA Billing System', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            Database()
            cursor.execute("DELETE FROM billing WHERE Case_id = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()
    
def ShowViewBilling():
    global viewformBilling
    viewformBilling = Toplevel()
    viewformBilling.title("ECA Billing System/View Billing Information")
    width = 1600
    height = 900
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    viewformBilling.geometry("%dx%d+%d+%d" % (width, height, x, y))
    viewformBilling.resizable(0, 0)
    ViewFormBilling()

# BILLING Add New and View Records -------  ENDS here --------


def Logout():
    result = tkMessageBox.askquestion('ECA Billing System', 'Are you sure you want to logout?', icon="warning")
    if result == 'yes': 
        admin_id = ""
        root.deiconify()
        Home.destroy()
  
def Login(event=None):
    global admin_id
    Database()
    if USERNAME.get == "" or PASSWORD.get() == "":
        lbl_result.config(text="Please complete the required field!", fg="red")
    else:
        cursor.execute("SELECT * FROM `admin` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            cursor.execute("SELECT * FROM `admin` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
            data = cursor.fetchone()
            admin_id = data[0]
            USERNAME.set("")
            PASSWORD.set("")
            lbl_result.config(text="")
            ShowHome()
        else:
            lbl_result.config(text="Invalid username or password", fg="red")
            USERNAME.set("")
            PASSWORD.set("")
    cursor.close()
    conn.close() 

def ShowHome():
    root.withdraw()
    Home()
    loginform.destroy()


#========================================MENUBAR WIDGETS==================================
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="LOGIN", command=ShowLoginForm)
filemenu.add_command(label="Exit", command=Exit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

#========================================FRAME============================================
Title = Frame(root, bd=1, relief=SOLID)
Title.pack(pady=10)

#========================================LABEL WIDGET=====================================
lbl_display = Label(Title, text="ECA Billing System", font=('arial', 28))
lbl_display.pack()

#========================================INITIALIZATION===================================
if __name__ == '__main__':
    root.mainloop()
