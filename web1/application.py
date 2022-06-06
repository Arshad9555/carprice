from _curses import flash

import MySQLdb
from flask import Flask, render_template, request, redirect, url_for, session
import xgboost

import pickle
import pandas as pd
import numpy as np
import logging as lg
import mysql.connector as conn
from flaskext import mysql
import re

app = Flask(__name__)
app.secret_key = 'your secret key'

model = pickle.load(open('dfLassoRegressionModel95.pkl', 'rb'))
df = pd.read_csv('changed.csv')
lg.basicConfig(filename='LogFile.log', level=lg.INFO, format="%(asctime)s %(levelname)s %(message)s")


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('Login.html')


@app.route('/Registration', methods=['POST', 'GET'])
def Registration():
    return render_template('Registration.html')


@app.route('/Home', methods=['POST', 'GET'])
def Home():
    return render_template('index.html')


@app.route('/home', methods=['POST', 'GET'])
def home():
    username = str(request.form['username'])
    password = str(request.form['password'])
    print(username)
    print(password)
    password = request.form['password']
    mydb = conn.connect(host='localhost', user='root', passwd='A#@95rshad')
    print(mydb)
    cur = mydb.cursor()
    cur.execute('use car')
    # cur.execute('select * from car.login')
    cur.execute('SELECT * FROM car.login WHERE username = %s AND password = %s', (username, password,))
    # Fetch one record and return result
    data = cur.fetchone()
    print(data)
    print(type(data))
    # data = cur.fetchall()

    # return data
    # print(data)
    # return render_template('index.html')
    # DbUname = str(data[0][0])
    DbUname = str(data[0])
    print(DbUname)
    print(type(DbUname))
    session['username'] = data[0]
    session['password'] = data[1]
    DbPass = str(data[1])
    print(DbPass)
    print(type(DbPass))
    try:
        if DbUname == username and DbPass == password:
            # return redirect(url_for('index'))
            return render_template('index.html')
            flash('successfully loggedIn!')
        else:

            error_msg = 'Incorrect username/password!'
            return render_template('Login.html', error_msg=error_msg)
    except NoneType:
        error_msg = 'Incorrect username/password!'
        return render_template('Login.html', error_msg=error_msg)


@app.route('/xyz1', methods=['POST', 'GET'])
def xyz1():
    try:
        if request.method == 'POST':
            username = str(request.form['username'])
            password = str(request.form['password'])
            print(username)
            print(password)
            password = request.form['password']
            mydb = conn.connect(host='localhost', user='root', passwd='A#@95rshad')
            print(mydb)
            cur = mydb.cursor()
            cur.execute('use car')
            # cur.execute('select * from car.login')
            cur.execute('SELECT EmailId,Password FROM car.registration WHERE EmailId = %s AND Password = %s',
                        (username, password,))
            # Fetch one record and return result
            data = cur.fetchone()
            print(data)
            print(type(data))
            # data = cur.fetchall()

            # return data
            # print(data)
            # return render_template('index.html')
            # DbUname = str(data[0][0])
            DbUname = str(data[0])
            print(DbUname)
            print(type(DbUname))
            session['username'] = data[0]
            session['password'] = data[1]
            DbPass = str(data[1])
            print(DbPass)
            print(type(DbPass))

        if DbUname == username and DbPass == password:
            # return redirect(url_for('index'))
            return render_template('index.html')
            # flash('successfully loggedIn!')
        else:

            error_msg = 'Incorrect username/password!'
            # flash('Invalid user credentials!please try agian  with valid credentilas')
            return render_template('Login.html', error_msg=error_msg)
    except TypeError:
        error_msg = 'Incorrect username/password!'
        error_msg = 'Incorrect username/password!'
        # flash('Invalid user credentials!please try agian  with valid credentials')
    except NameError:
        error_msg = 'Incorrect username/password!'
        # flash('Invalid user credentials!please try agian  with valid credentials')
    return render_template('Login.html', error_msg=error_msg)


@app.route('/logout')
def logout():
    return render_template('Login.html')
    # return redirect(url_for('xyz1'))


@app.route('/pythonlogin', methods=['GET', 'POST'])
def pythonlogin():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        mydb = conn.connect(host='localhost', user='root', passwd='A#@95rshad')
        print(mydb)
        cur = mydb.cursor()
        cur.execute('use car')
        cur.execute('SELECT * FROM car.login WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = str(cur.fetchone())
        print(type(account))
        print(account)
        account[0]
        account[1]
        # print(account['username'])
        # print(account['password'])
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True

            session['username'] = account[0]
            session['password'] = account[1]
            if account[0] == username and account[1] == password:
                return render_template('index.html')
                return "logged in successfully"
            else:
                errormsg = 'Incorrect username/password!'
                return render_template('Login.html', errormasg=errormsg)


        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        fname = request.form['firstname']
        lname = request.form['lastname']
        password = request.form['password']
        cpassword = request.form['cpassword']
        cartype = request.form['cartype']
        email = request.form['emailid']
        phone = request.form['phonenumber']
        print(fname, lname, password, cpassword, cartype, email, phone)
        mydb = conn.connect(host='localhost', user='root', passwd='A#@95rshad')
        print(mydb)
        cursor = mydb.cursor(buffered=True)
        cursor.execute('use car')
        cursor.execute('SELECT EmailId FROM car.registration WHERE EmailId = %s', (email,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', email):
            msg = 'Username must contain only characters and numbers !'

        else:
            # cursor.execute('INSERT INTO car.registration VALUES (NULL, % s, % s, % s)', (email, password, email,))
            # cursor.execute("""insert into car.registration(FirstName,LastName,Password,CPassword,CarType,EmailId,
            # Phone) values(fname,lname,password,cpassword,cartype,email,phone)""")
            cursor.execute("INSERT INTO car.registration (FirstName,LastName,Password,CPassword,CarType,EmailId,"
                           "Phone) VALUES "
                           "(%s, %s, %s, %s, %s, %s, %s)", (fname, lname, password, cpassword, cartype, email, phone))
            mydb.commit()
            cursor.close()
            mydb.close()
            msg = 'You have successfully registered !'
    # elif request.method == 'POST':
    #     msg = 'Please fill out the form !'
    return render_template('Registration.html', msg=msg)


@app.route('/RetrieveData', methods=['POST', 'GET'])
def RetrieveData():
    print("Hello World")
    try:
        if request.method == 'POST':
            print("inside retrieve method")
            Car_Name = request.form['Car_Name1']
            manufacturer = request.form['Manufacturer1']
            year = request.form['Year1']
            fuel_Type = request.form['Fuel_Type1']
            transmission = request.form['Transmission1']

            print(Car_Name, manufacturer, year, fuel_Type, transmission)
            mydb = conn.connect(host='localhost', user='root', passwd='A#@95rshad')
            print(mydb)
            cur = mydb.cursor(buffered=True)

            # query = 'select Present_Price,First_Launched,Data_Available_From from CarInfo where Car_Name=Car_Name,' \
            #         'Manufacturer=manufacturer,Year=year,Fuel_Type=fuel_Type,Transmission=transmission'
            cur.execute("""select distinct Present_Price,First_Launched,Data_Available_From from car.carinfo1 where 
            Car_Name=Car_Name AND Manufacturer=manufacturer AND Year=year AND Fuel_Type=fuel_Type AND 
            Transmission=transmission""")
            # cur.execute("""select distinct Present_Price,First_Launched,Data_Available_From from car.carinfo1 where
            # Car_Name=%s AND Manufacturer=%s AND Year=%s AND Fuel_Type=%s AND Transmission=%s ,(car)""")
            query = """select Present_Price, First_Launched, Data_Available_From from car.cardata where Car_Name=%s 
                        and Manufacturer=%s and Year=%s and Fuel_Type=%s and Transmission=%s"""
            values = (Car_Name, manufacturer, year, fuel_Type, transmission,)
            cur.execute(query, values)

            data = cur.fetchone()
            data = list(data)
            print(data[0])
            print(data[1])
            print(data[2])

            print(data)
            # return str(output)
            # return redirect(url_for('/RetrieveData'))
            # return redirect(url_for("PredictPriceForm"))
            msg = "The Car Price in the year {} is {} and Data Is Available From Year {} And was First Launched In " \
                  "the Year{}".format(year, data[0], data[2], data[1])
            return render_template('index1.html', msg=msg)

        else:
            msg = "sorry data not found"
            return render_template('index1.html', msg=msg)
    except TypeError:
        msg = "Sorry Data Not Found!"
        return render_template('index1.html', msg=msg)


@app.route('/PredictPriceForm', methods=['GET', 'POST'])
def PredictPriceForm():
    # return redirect(url_for('index1.html'))
    # return render_template('index1.html')
    lg.info("Home Page")
    Car_Name = sorted(df['Car_Name'].unique())
    Manufacturer = sorted(df['Manufacturer'].unique())
    Year = sorted(df['Year'].unique())
    Kms_Driven = sorted(df['Kms_Driven'].unique())
    Fuel_Type = sorted(df['Fuel_Type'].unique())
    Seller_Type = sorted(df['Seller_Type'].unique())
    Transmission = sorted(df['Transmission'].unique())
    No_Of_Owners = sorted(df['No_Of_Owners'].unique())
    Insurance = sorted(df['Insurance'].unique())

    Car_Name.insert(0, '<--Select-->')
    Manufacturer.insert(0, '<--Select-->')
    Year.insert(0, '<--Select-->')
    Fuel_Type.insert(0, '<--Select-->')
    Seller_Type.insert(0, '<--Select-->')
    Transmission.insert(0, '<--Select-->')
    Insurance.insert(0, '<--Select-->')

    return render_template('index1.html', Car_Name=Car_Name, Manufacturer=Manufacturer, Year=Year, Fuel_Type=Fuel_Type,
                           Seller_Type=Seller_Type, Transmission=Transmission, Insurance=Insurance)


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        lg.info("The control has entered the predict method of predict route")
        try:
            Manufacturer = request.form['Manufacturer']
            Car_Name = request.form['Car_Name']
            Year = request.form['Year']
            Kms_Driven = request.form['Kms_Driven']
            Fuel_Type = request.form['Fuel_Type']
            Seller_Type = request.form['Seller_Type']
            Transmission = request.form['Transmission']
            No_Of_Owners = request.form['No_Of_Owners']
            Present_Price = request.form['Present_Price']
            Insurance = request.form['Insurance']

            print(Car_Name, Manufacturer, Year, Kms_Driven, Fuel_Type, Seller_Type, Transmission, No_Of_Owners,
                  Present_Price, Insurance)
            lg.info(str(Manufacturer) + str(Car_Name) + str(Year) +
                    str(Kms_Driven) + str(Fuel_Type) + str(Seller_Type) + str(Transmission) + str(No_Of_Owners) + str(
                Present_Price) + str(Insurance))

            prediction = model.predict(pd.DataFrame(columns=['Car_Name', 'Manufacturer', 'Year', 'Kms_Driven',
                                                             'Fuel_Type', 'Seller_Type', 'Transmission', 'No_Of_Owners',
                                                             'Present_Price', 'Insurance'],
                                                    data=np.array([
                                                        Car_Name, Manufacturer, Year, Kms_Driven, Fuel_Type,
                                                        Seller_Type,
                                                        Transmission, No_Of_Owners,
                                                        Present_Price, Insurance]).reshape(1, 10)))
            final_result = abs(round(prediction[0], 1))
            # print(round(prediction[0], 1))
            print(final_result)

            if final_result != " ":
                return render_template('index1.html',
                                       prediction_text="The Market Value Of The Car is: ₹{}".format(final_result))
            else:
                return render_template('index1.html', prediction_text="Sorry! we could not evaluate your Car value")

        except Exception as e:
            lg.error("Error has occured!please check the description below")
            lg.exception(str(e))
            print(e)

            return render_template('index1.html', prediction_text="sorry!")
    else:

        return render_template('index1.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8001, debug=True)
