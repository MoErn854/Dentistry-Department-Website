import os
from flask import Flask,flash, render_template, request, redirect, url_for, session
import mysql.connector
import re
from werkzeug.utils import secure_filename
import json

# Connect Database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="dentalhealth"
)

mycursor = mydb.cursor(buffered=True)


# Retrieve all information about app
mycursor.execute("SELECT * FROM siteInfo")
siteInfoTable = mycursor.fetchone()

# Retrieve slider images
mycursor.execute("SELECT * FROM slider")
sliderImg = mycursor.fetchall()

# Retrieve all doctors data
mycursor.execute("SELECT * FROM Doctors")
DoctorsTable = mycursor.fetchall()

# Retrieve all treatments data
mycursor.execute("SELECT * FROM treatments")
TreatTable = mycursor.fetchall()

# Our Website
website = Flask(__name__)
UPLOAD_FOLDER = '/Static/img/' # {{ url_for('static', filename='img/') }}
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

website.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
website.secret_key = '01140345493Mm'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


""" Routes of Pages """
# Home Page
@website.route("/", methods =['GET', 'POST'])
def HomePage():

  # Retrieve slider images
  mycursor.execute("SELECT * FROM slider")
  sliderImg = mycursor.fetchall()

  session['title'] = siteInfoTable[1]
  session['address'] = siteInfoTable[2]
  session['email'] = siteInfoTable[3]
  session['phone'] = siteInfoTable[4]
  session['discr'] = siteInfoTable[5]
  # Retrieve all treatments data
  mycursor.execute("SELECT * FROM treatments")
  TreatTable = mycursor.fetchall()
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
              return redirect(url_for('ProfilePage'))
    else:
        msg = 'Incorrect email or password !'
        return render_template("index.html",
                        titlePage="Homepage", 
                        ActiveHome="active", 
                        msg = msg, 
                        TreatData=TreatTable,
                        sliderImg=sliderImg)
  else:
    return render_template("index.html",
                        titlePage="Homepage", 
                        ActiveHome="active", 
                        msg = msg, 
                        TreatData=TreatTable,
                        sliderImg=sliderImg)

# About Us
@website.route("/About")
def AboutUsPage():
  # Retrieve all information about app
  mycursor.execute("SELECT * FROM siteInfo")
  siteInfoTable = mycursor.fetchone()
  return render_template("about.html", 
                          titlePage="About Us", 
                          ActiveAbout="active")

# Doctors
@website.route("/Doctors")
def DoctorsPage():
  # Retrieve all doctors data
  mycursor.execute("SELECT * FROM Doctors")
  DoctorsTable = mycursor.fetchall()
  return render_template("Doctors.html", 
                          titlePage="Our Dentists", 
                          ActiveDoctors="active",
                          DoctorsData=DoctorsTable)

# Appointments
@website.route("/Appointment", methods=['GET', 'POST'])
def Appointment():
    msg = ""
    Tcost = 0
    PassOrNot = "text-danger"

    if request.method == 'POST' and 'Fname' in request.form and 'Lname' in request.form and 'Age' in request.form and 'Gender' in request.form and 'Doctors' in request.form and 'Service' in request.form:
        Fname = request.form['Fname']
        Lname = request.form['Lname']
        Age = request.form['Age']
        Gender = request.form['Gender']
        Doctors = request.form['Doctors']
        Service = request.form['Service']
        userId = session['id']

        # Display Cost
        mycursor.execute('SELECT Tcost FROM treatments where TName = %s',(Service,))
        Tcost = mycursor.fetchone()

        mycursor.execute('SELECT SSN FROM Doctors where D_Name = %s',(Doctors,))
        DSSN = mycursor.fetchone()

        mycursor.execute('SELECT id FROM treatments where TName = %s',(Service,))
        ServiceId = mycursor.fetchone()
        
        mycursor.execute('SELECT * FROM appointments')
        mycursor.fetchall()
        number_of_rows = mycursor.rowcount
        mycursor.execute("INSERT INTO appointments VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (number_of_rows+1 ,Fname, Lname, Age, Gender, DSSN[0], ServiceId[0], userId ))
        mydb.commit()
        msg = 'You have successfully booked an appointment!'
        PassOrNot = "text-success"

    # Retrieve all treatments data
    mycursor.execute("SELECT * FROM treatments")
    TreatTable = mycursor.fetchall()

    # Retrieve all doctors data
    mycursor.execute("SELECT * FROM Doctors")
    DoctorsTable = mycursor.fetchall()
    
    return render_template("Appointment.html", 
                          titlePage="Book an appointment", 
                          DoctorsData=DoctorsTable, 
                          TreatData=TreatTable,
                          cost=Tcost,
                          msg=msg,
                          PassOrNot=PassOrNot)

# Register
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


    return render_template('register.html', 
                            titlePage="Sign Up" , 
                            msg=msg, 
                            registered=PassOrNot, 
                            hidden="d-none")

# User Profile
@website.route("/profile")
def ProfilePage():
  if session['username']:
    mycursor.execute("select * from Appointments where userId = %s",(session['id'],))
    AppointmentsTable = mycursor.fetchall()

  mycursor.execute('SELECT * FROM users WHERE username = %s', (session['username'], ))
  UserInfo = mycursor.fetchone()

  UserProblems = []
  UserDoctors = []
  for Appointment in AppointmentsTable :
    mycursor.execute('SELECT * FROM Doctors WHERE SSN = %s', (Appointment[5], ))
    D_Name = mycursor.fetchone()
    
    mycursor.execute('SELECT * FROM treatments WHERE id = %s', (Appointment[6], ))
    T_Name = mycursor.fetchone()

    UserProblems.append(T_Name)
    UserDoctors.append(D_Name)

  return render_template("profile.html",
                        titlePage=session['username'], 
                        Info=UserInfo,
                        AppointmentsTable=AppointmentsTable,
                        UserProblems=UserProblems,
                        UserDoctors=UserDoctors )

# Logout
@website.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('HomePage'))


################################################################

# Admin Page
@website.route('/Admin/Home')
def Admin():
    # Check if user is loggedin
    if 'loggedinAdmin' in session:
      # User is loggedin show them the home page  
      return render_template('Admin/home.html' ,titlePage="Admin Control Panel")
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@website.route('/Admin/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        mycursor.execute('SELECT * FROM admins WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = mycursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedinAdmin'] = True
            session['idAdmin'] = account[0]
            session['usernameAdmin'] = account[1]
            # Redirect to home page
            return redirect(url_for('Admin'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('Admin/index.html', msg=msg, titlePage="Admin Control Panel")

@website.route('/Admin/logout')
def logoutAdmin():
    # Remove session data, this will log the user out
   session.pop('loggedinAdmin', None)
   session.pop('idAdmin', None)
   session.pop('usernameAdmin', None)
   # Redirect to login page
   return redirect(url_for('login'))

@website.route('/Admin/doctors', methods=['GET', 'POST'])
def doctors():
  # Check if user is loggedin
    if 'loggedinAdmin' in session:
      msg = ''
      PassOrNot = "text-danger"
      if request.method == 'POST' and 'SSN' in request.form and 'Name' in request.form and 'Telephone' in request.form and 'Gender' in request.form and 'Email' in request.form and 'Age' in request.form and 'Degree' in request.form :
          SSN = request.form['SSN']
          Name = request.form['Name']
          Telephone = request.form['Telephone']
          Gender = request.form['Gender']
          Email = request.form['Email']
          Age = request.form['Age']
          Degree = request.form['Degree']

          mycursor.execute('SELECT * FROM doctors WHERE SSN = %s', (SSN, ))
          D_SSN = mycursor.fetchone()
          mycursor.execute('SELECT * FROM doctors WHERE D_Email = %s', (Email, ))
          emailAdd = mycursor.fetchone()
          if D_SSN:
              msg = 'SSN already exists !'
          elif emailAdd :
              msg = 'Email already exists !'
          elif not re.match(r'[A-Za-z]+', Name):
              msg = 'Name must contain only characters'
          else:
              mycursor.execute("INSERT INTO doctors VALUES (%s, %s, %s, %s, %s, %s, %s)", (SSN ,Name, Gender, Email, Age, Degree,Telephone ))
              mydb.commit()
              msg = 'You have successfully Added Doctor.'
              PassOrNot = "text-success"
      
      # Update all doctors data
      mycursor.execute("SELECT * FROM Doctors")
      DoctorsTable = mycursor.fetchall()

      # User is loggedin show them the home page  
      return render_template('Admin/doctors.html',registered=PassOrNot, msg=msg, DoctorsData=DoctorsTable ,titlePage="Doctors Control Panel")
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@website.route('/Admin/slider', methods=['GET', 'POST'])
def sliderAdmin():
  if 'loggedinAdmin' in session:
    msg = ''
    if request.method == 'POST':
        file = request.files['file']
        title = request.form['title']
        description = request.form['description']

        mycursor.execute('SELECT * FROM slider')
        mycursor.fetchall()
        number_of_rows = mycursor.rowcount

        path = "static/img/slider/" + secure_filename(file.filename)
        file.save(path)
        mycursor.execute("INSERT INTO slider VALUES (%s, %s, %s, %s)", (number_of_rows+1, path, title, description))
        mydb.commit()
        msg = 'Uploaded successfully'

    # Retrieve slider images
    mycursor.execute("SELECT * FROM slider")
    sliderImg = mycursor.fetchall()
    return render_template('Admin/Slider.html', msg=msg,titlePage="Slider Control Panel",sliderImg=sliderImg)

  return redirect(url_for('login'))


@website.route('/Admin/users', methods=['GET', 'POST'])
def usersAdmin():
  if 'loggedinAdmin' in session:    
    # Retrieve slider images
    mycursor.execute("SELECT * FROM users")
    users = mycursor.fetchall()
    return render_template('Admin/users.html', titlePage="Users",users=users)

  return redirect(url_for('login'))

@website.route('/Admin/Services', methods=['GET', 'POST'])
def servicesAdmin():
  # Check if user is loggedin
    if 'loggedinAdmin' in session:
      msg = ''
      PassOrNot = "text-danger"
      if request.method == 'POST' :
          Name = request.form['Name']
          Cost = request.form['Cost']
          Duration = request.form['Duration']
          mycursor.execute('SELECT * FROM treatments')
          mycursor.fetchall()
          number_of_rows = mycursor.rowcount
          mycursor.execute("INSERT INTO treatments VALUES (%s, %s, %s, %s)", (number_of_rows+1 ,Name, Cost, Duration))
          mydb.commit()
          msg = 'You Have Successfully Added New Services.'
          PassOrNot = "text-success"
      
      # Update all doctors data
      mycursor.execute("SELECT * FROM treatments")
      servicesData = mycursor.fetchall()

      # User is loggedin show them the home page  
      return render_template('Admin/services.html',registered=PassOrNot, msg=msg, servicesData=servicesData ,titlePage="Doctors Control Panel")
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


if __name__ == "__main__":  
  # RUN
  website.run(debug=True,port=9000)