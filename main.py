from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import re

# Connect Database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="dentalhealth"
)

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM Doctors")

DoctorsTable = mycursor.fetchall()

website = Flask(__name__)
website.secret_key = '01140345493'

@website.route("/", methods =['GET', 'POST'])
def HomePage():
  msg = ""
  if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
    email = request.form['email']
    password = request.form['password']

    mycursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password, ))
    user = mycursor.fetchone()
    if user:
              session['loggedin'] = True
              session['id'] = user[0]
              session['username'] = user[3]
              msg = 'Logged in successfully !'
              return render_template("index.html",
                        titlePage="Homepage", 
                        ActiveHome="active", msg = msg)
    else:
        msg = 'Incorrect email or password !'
        return render_template("index.html",
                        titlePage="Homepage", 
                        ActiveHome="active", msg = msg)
  else:
    return render_template("index.html",
                        titlePage="Homepage", 
                        ActiveHome="active", msg = msg)


@website.route("/About")
def AboutUsPage():
  return render_template("about.html", 
                          titlePage="About Us", 
                          ActiveAbout="active",
                          AboutPar= "here about para")


@website.route("/Doctors")
def DoctorsPage():
  return render_template("Doctors.html", 
                          titlePage="Doctors", 
                          ActiveDoctors="active",
                          DoctorsData=DoctorsTable)

@website.route("/Appointment")
def AppointmentPage():
  return render_template("Appointment.html", 
                          titlePage="Book an Appointment", 
                          ActiveApointment="active")


@website.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    PassOrNot = "text-danger"
    if request.method == 'POST' and 'Fname' in request.form and 'Lname' in request.form and 'username' in request.form and 'password' in request.form and 'repassword' in request.form and 'email' in request.form :
        Fname = request.form['Fname']
        Lname = request.form['Lname']
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['repassword']
        email = request.form['email']

        mycursor.execute('SELECT * FROM users WHERE username = %s', (username, ))
        user = mycursor.fetchone()
        mycursor.execute('SELECT * FROM users WHERE email = %s', (email, ))
        emailAdd = mycursor.fetchone()
        if user:
            msg = 'username already exists !'
        elif emailAdd :
            msg = 'Email already exists !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not repassword == password :
            msg = 'Please Enter  the same password !'
        else:
            mycursor.execute('SELECT * FROM users')
            mycursor.fetchall()
            number_of_rows = mycursor.rowcount
            mycursor.execute("INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s)", (number_of_rows+1 ,Fname, Lname, username, password, email, ))
            mydb.commit()
            msg = 'Congratulation !! You have successfully registered.'
            PassOrNot = "text-success"


    return render_template('register.html', titlePage="Sign Up" , msg=msg, registered=PassOrNot, hidden="d-none")

@website.route("/profile")
def ProfilePage():
  mycursor.execute("select * from users where username = %s",(session.username,))
  UserInfo = mycursor.fetchall()
  return render_template("profile.html", titlePage=session.username, Info=UserInfo)

@website.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('index.html', titlePage="Homepage", 
                        ActiveHome="active")


if __name__ == "__main__":  
  website.run(debug=True,port=9000)