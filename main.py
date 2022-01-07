#Imports
from typing import Dict
from flask import Flask,flash, render_template, request, redirect, url_for, session
import mysql.connector
import re
from werkzeug.utils import secure_filename
import random
import string
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, SubmitField
from flask_mail import Mail, Message
#--------------------------------------------------------------------------#

"""Classes"""
class ContactForm(FlaskForm):
    name = StringField("Name")
    email = StringField("Email")
    subject = StringField("Subject")
    message = TextAreaField("Message")
    submit = SubmitField("Send")


"""Functions"""
# Generate random password
def get_random_number():
    length = random.randint(8,10)
    # choose from all lowercase letter
    numbers = string.digits
    result_str = ''.join(random.choice(numbers) for i in range(length))
    return result_str

#--------------------------------------------------------------------------#

# Connecting with Database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="stomology-dep"
)
# Initialize our cursor
mycursor = mydb.cursor(buffered=True)

#--------------------------------------------------------------------------#

"""Retrive Database Tables"""
# Retrieve all information about site
mycursor.execute("SELECT * FROM site_information")
siteInfoTable = mycursor.fetchone()

# Retrieve slider images
mycursor.execute("SELECT * FROM slider")
sliderImg = mycursor.fetchall()

# Retrieve all doctors data
mycursor.execute("SELECT * FROM doctors")
DoctorsTable = mycursor.fetchall()

# Retrieve all treatments data
mycursor.execute("SELECT * FROM treatments")
TreatTable = mycursor.fetchall()

# Retrieve all Rates data
mycursor.execute("SELECT * FROM rates limit 10")
RatesTable = mycursor.fetchall()

# Retrieve all information about app
mycursor.execute("SELECT * FROM users")
users = mycursor.fetchall()

#--------------------------------------------------------------------------#


"""Our Website"""
website = Flask(__name__)
website.secret_key = '**************' # Put your Secret_Key


# Initilize contact us information
website.config.update(dict(
    MAIL_SERVER = 'smtp.googlemail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = siteInfoTable[2],
    MAIL_PASSWORD = '**************' # Put your password of email
))
mail = Mail(website)


# Initilize Upload Settings
UPLOAD_FOLDER = '/Static/img/' # {{ url_for('static', filename='img/') }}
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

website.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#--------------------------------------------------------------------------#



""" Routes of Pages """
# Home Page
@website.route("/", methods =['GET', 'POST'])
def HomePage():

  # Identify site's information
  session['title'] = siteInfoTable[0]
  session['address'] = siteInfoTable[1]
  session['email'] = siteInfoTable[2]
  session['phone'] = siteInfoTable[3]
  session['short'] = siteInfoTable[4]
  session['long'] = siteInfoTable[5]

  # Retrieve All slider's images
  mycursor.execute("SELECT * FROM slider")
  sliderImg = mycursor.fetchall()

  # Retrieve all treatments' data
  mycursor.execute("SELECT * FROM treatments")
  TreatTable = mycursor.fetchall()

  msg = ""
  # If login
  if request.method == 'POST' :
    
    doctor = request.form.get('doctor')
    email = request.form['email']
    password = request.form['password']

    if doctor == 'on' :
      # If doctor
      mycursor.execute('SELECT * FROM doctors WHERE D_Email = %s AND password = %s', (email, password, ))
      doctor = mycursor.fetchone()
      if doctor:
        # If info of doctor is right
          session['loggedin'] = True
          session['id'] = doctor[0]
          session['ssn'] = doctor[1]
          session['username'] = doctor[8]
          session['doctor'] = True
          msg = 'Logged in successfully !'
          
          return redirect(url_for('ProfilePage'))

      else:
        # If info is Wrong
          msg = 'Incorrect email or password !'
          return render_template("index.html",
                          titlePage="Homepage", 
                          ActiveHome="active", 
                          msg = msg, 
                          TreatData=TreatTable,
                          sliderImg=sliderImg,
                          RatesTable=RatesTable,
                          users=users)
    else :
      # If normal user
      mycursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password, ))
      user = mycursor.fetchone()
      if user:
                session['loggedin'] = True
                session['id'] = user[0]
                session['username'] = user[5]
                session['doctor'] = False

                msg = 'Logged in successfully !'
                return redirect(url_for('ProfilePage'))

      else:
          msg = 'Incorrect email or password !'
          return render_template("index.html",
                          titlePage="Homepage", 
                          ActiveHome="active", 
                          msg = msg, 
                          TreatData=TreatTable,
                          sliderImg=sliderImg,
                          RatesTable=RatesTable,
                          users=users)

  else:
    return render_template("index.html",
                        titlePage="Homepage", 
                        ActiveHome="active", 
                        msg = msg, 
                        TreatData=TreatTable,
                        sliderImg=sliderImg,
                        RatesTable=RatesTable,
                        users=users)


# About Us
@website.route("/About")
def AboutUsPage():
  # Retrieve all information about app
  mycursor.execute("SELECT * FROM site_information")
  siteInfoTable = mycursor.fetchone()
  return render_template("about.html", 
                          titlePage="About Us", 
                          ActiveAbout="active",
                          users=users)



# Doctors
@website.route("/Doctors")
def DoctorsPage():
  # Retrieve all doctors data
  mycursor.execute("SELECT * FROM doctors")
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

    if request.method == 'POST' :
        SSN = request.form['SSN']
        FName = request.form['FName']
        MidName = request.form['MidName']
        LName = request.form['LName']
        Age = request.form['Age']
        Gender = request.form['Gender']
        userId = session['id']
        Doctor = request.form['Doctor']
        DoctorName=Doctor.split()
        Service = request.form['Service']
        

        # Display Cost
        mycursor.execute('SELECT cost FROM treatments where Name = %s',(Service,))
        Tcost = mycursor.fetchone()

        mycursor.execute('SELECT Id FROM doctors where FName = %s and MidName = %s and LName = %s',(DoctorName[0],DoctorName[1],DoctorName[2]))
        D_Id = mycursor.fetchone()

        mycursor.execute('SELECT id FROM treatments where Name = %s',(Service,))
        ServiceId = mycursor.fetchone()
        
        mycursor.execute("INSERT INTO appointments(SSN, FName, MidName, LName, Age, Gender,  Status  , userId, DoctorID, ServiceID ) VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s)", 
                                                  (SSN, FName, MidName, LName, Age, Gender, "Waiting", userId, D_Id[0] , ServiceId[0] ))
        mydb.commit()
        msg = 'You have successfully booked an appointment!'
        PassOrNot = "text-success"

    # Retrieve all treatments data
    mycursor.execute("SELECT * FROM treatments")
    TreatTable = mycursor.fetchall()

    # Retrieve all doctors data
    mycursor.execute("SELECT * FROM doctors")
    DoctorsTable = mycursor.fetchall()
    
    return render_template("Appointment.html", 
                          titlePage="Book an appointment", 
                          DoctorsData=DoctorsTable, 
                          TreatData=TreatTable,
                          cost=Tcost,
                          msg=msg,
                          PassOrNot=PassOrNot)


# # Scans And Problems
# @website.route("/Problem", methods=['GET', 'POST'])
# def Problem():
  # pass
  # msg = ""
  # Tcost = 0
  # PassOrNot = "text-danger"

  # if request.method == 'POST':
      
  #     Image = request.files['image']
  #     Age = request.form['Age']
  #     Gender = request.form['Gender']
  #     Doctors = request.form['Doctors']
  #     userId = session['id']
  #     Description = request.form['Description']

  #     mycursor.execute('SELECT SSN FROM Doctors where D_Name = %s',(Doctors,))
  #     DSSN = mycursor.fetchone()
      
      
  #     path = "static/img/UsersProfile/" + secure_filename(Image.filename)
  #     Image.save(path)
      
  #     mycursor.execute("INSERT INTO appointments VALUES (%s, %s, %s, %s, %s, %s, %s)", (NULL, path, Age, Gender, DSSN[0], userId, Description ))
  #     mydb.commit()
  #     msg = 'You have successfully Send your problem, please wait until doctor respond!'
  #     PassOrNot = "text-success"

  # # Retrieve all treatments data
  # mycursor.execute("SELECT * FROM treatments")
  # scansTable = mycursor.fetchall()

  # # Retrieve all doctors data
  # mycursor.execute("SELECT * FROM Doctors")
  # DoctorsTable = mycursor.fetchall()
  
  # return render_template("scans.html", 
  #                       titlePage="Problems", 
  #                       DoctorsData=DoctorsTable, 
  #                       scansTable=scansTable,
  #                       msg=msg,
  #                       PassOrNot=PassOrNot)


# Register
@website.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    PassOrNot = "text-danger"
    if request.method == 'POST' :
        FName = request.form['FName']
        MidName = request.form['MidName']
        LName = request.form['LName']
        Image = request.files["file"]
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['repassword']
        email = request.form['email']
        phone = request.form['Phone']

        mycursor.execute('SELECT * FROM users WHERE UserName = %s', (username, ))
        NewUser = mycursor.fetchone()
        mycursor.execute('SELECT * FROM users WHERE Email = %s', (email, ))
        NewEmail = mycursor.fetchone()
        if NewUser:
            msg = 'Username already exists !'
        elif NewEmail :
            msg = 'Email already exists !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not repassword == password :
            msg = 'Please Enter the same password !'
        elif len(password) < 5 :
            msg = 'Weak Password !'
        else:
            path = "static/img/UsersProfile/" + secure_filename(Image.filename)
            Image.save(path)

            mycursor.execute("INSERT INTO users(FName, MidName, LName, Image, UserName, Password, Email, phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                                               (FName, MidName, LName, path, username, password, email, phone))
            mydb.commit()
            msg = 'Congratulation !! You have successfully registered.'
            PassOrNot = "text-success"


    return render_template('register.html', 
                            titlePage="Sign Up" , 
                            msg=msg, 
                            registered=PassOrNot, 
                            hidden="d-none")


# User Profile
@website.route("/profile", methods =['GET', 'POST'])
def ProfilePage():
  Treatments = []
  Doctors = []
  Users = []
  if session['username']:

    if session['doctor'] :
      # If doctor
      mycursor.execute("select * from appointments where DoctorId = %s",(session['id'],))
      AppointmentsTable = mycursor.fetchall()

      mycursor.execute('SELECT * FROM doctors WHERE Email = %s', (session['username'], ))
      UserInfo = mycursor.fetchone()

      for Appointment in AppointmentsTable :
        mycursor.execute('SELECT * FROM users WHERE id = %s', (Appointment[9], ))
        U_Name = mycursor.fetchone()
        
        mycursor.execute('SELECT * FROM treatments WHERE id = %s', (Appointment[11], ))
        T_Name = mycursor.fetchone()

        Treatments.append(T_Name)
        Users.append(U_Name)

    else:
      # If normal user
      if request.method == 'POST' :
        id = request.form['id']
        if request.form['status'] == 'Confirm':
          mycursor.execute('Update appointments set Status="Scheduled" WHERE id = %s', (id, ))
        elif request.form['status'] == 'Reject':
          mycursor.execute('Update appointments set Status="Refused" WHERE id = %s', (id, ))
      
        mydb.commit()
      
      mycursor.execute("select * from Appointments where UserID = %s",(session['id'],))
      AppointmentsTable = mycursor.fetchall()

      mycursor.execute('SELECT * FROM users WHERE UserName = %s', (session['username'], ))
      UserInfo = mycursor.fetchone()

      for Appointment in AppointmentsTable :
        mycursor.execute('SELECT * FROM doctors WHERE id = %s', (Appointment[10], ))
        D_Name = mycursor.fetchone()
        
        mycursor.execute('SELECT * FROM treatments WHERE id = %s', (Appointment[11], ))
        T_Name = mycursor.fetchone()

        Treatments.append(T_Name)
        Doctors.append(D_Name)

  return render_template("profile.html",
                        titlePage=session['username'], 
                        Info=UserInfo,
                        AppointmentsTable=AppointmentsTable,
                        Treatments=Treatments,
                        Doctors=Doctors,
                        Users=Users)


# Contact Us
@website.route("/Contact", methods=["GET", "POST"])
def ContactUs():
  msg = ""
  form = ContactForm()
  if request.method == 'POST':
      name = request.form["name"]
      email = request.form["email"]
      subject = request.form["subject"]
      message = request.form["message"]

      msg = Message(subject, sender=email, recipients=[siteInfoTable[3]])
      msg.body = "From " + email + " :\n" + name + " says : \n" + message
      mail.send(msg)
      
      msg = "Thanks for the message!!"
      
      return render_template("contact.html", 
                              titlePage="Contact Us", 
                              form=form,
                              ActiveContact="active",
                              msg=msg)

  return render_template("contact.html", 
                              titlePage="Contact Us", 
                              form=form,
                              ActiveContact="active",
                              msg=msg)
  

# Rate Us
@website.route("/Rate", methods=['GET', 'POST'])
def RateUs():
    msg = ""
    Tcost = 0
    PassOrNot = "text-danger"

    if request.method == 'POST' :
        rating = request.form['rating']
        message = request.form['message']
        userId = session['id']
        
        mycursor.execute("INSERT INTO Rates(rating, Review, UserID) VALUES (%s, %s, %s)", 
                                           (rating, message, userId))
        mydb.commit()

        msg = 'Thanks fou you!'
        PassOrNot = "text-success"

    # Retrieve all doctors data
    mycursor.execute("SELECT * FROM Rates")
    RatesTable = mycursor.fetchall()
    
    return render_template("rate.html", 
                          titlePage="Rate Us", 
                          RateData=RatesTable,
                          msg=msg, 
                          PassOrNot=PassOrNot)

# Logout
@website.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('doctor', None)

    return redirect(url_for('HomePage'))

#--------------------------------------------------------------------------#

"""Admin Control Panal"""
# Admin Page
@website.route('/Admin/Home')
def Admin():
    # Check if Admin is loggedin
    if 'loggedinAdmin' in session:

      """ Statistical Analysis """
      # Average of ratings
      mycursor.execute('SELECT * FROM rates')
      Rates = mycursor.fetchall()
      Rates = [rate[1] for rate in Rates]
      if len(Rates) == 0 :
        AvgOfRates = 0
      else :
        AvgOfRates = sum(Rates)/len(Rates)

      # Statistical Analysis Appointments
      mycursor.execute('SELECT Count(id) FROM appointments')
      numOfApp = mycursor.fetchall()[0][0]
      
      mycursor.execute('SELECT Count(id) FROM appointments where Status="Scheduled"')
      numOfAppSucc = mycursor.fetchall()[0][0]
      
      mycursor.execute('SELECT Count(id) FROM appointments where Status="Accepted"')
      numOfAppAcc = mycursor.fetchall()[0][0]

      mycursor.execute('SELECT Count(id) FROM Appointments where Status="Refused"')
      numOfAppRef = mycursor.fetchall()[0][0]

      AppointmentsList = [numOfApp,numOfAppSucc,numOfAppAcc,numOfAppRef]
      if numOfApp == 0 :
        AppointmentsListPrecentage = [0,0,0]
      else :
        AppointmentsListPrecentage = [numOfAppSucc/numOfApp,numOfAppAcc/numOfApp,numOfAppRef/numOfApp]
      
      # Statistical Analysis Doctors
      mycursor.execute('SELECT Count(id) FROM doctors')
      numOfDoctors = mycursor.fetchall()[0][0]

      mycursor.execute('SELECT Count(id) FROM doctors where Age>=20 and Age<30')
      numOfDoctors20 = mycursor.fetchall()[0][0]

      mycursor.execute('SELECT Count(id) FROM doctors where Age>=30 and Age<40')
      numOfDoctors30 = mycursor.fetchall()[0][0]

      mycursor.execute('SELECT Count(id) FROM doctors where Age>=40 and Age<50')
      numOfDoctors40 = mycursor.fetchall()[0][0]

      mycursor.execute('SELECT Count(id) FROM doctors where Age>=50')
      numOfDoctors50 = mycursor.fetchall()[0][0]

      DoctorsList = [numOfDoctors, numOfDoctors20, numOfDoctors30, numOfDoctors40, numOfDoctors50]
      if numOfDoctors == 0 :
        DoctorsListPrecentage = [0, 0, 0, 0]
      else :
        DoctorsListPrecentage = [numOfDoctors20/numOfDoctors, numOfDoctors30/numOfDoctors, numOfDoctors40/numOfDoctors, numOfDoctors50/numOfDoctors]

      # Statistical Analysis Services
      mycursor.execute('select ServiceID, COUNT(id) from appointments group by ServiceID order by ServiceID')
      ServicesListItems = mycursor.fetchall()

      ServicesDict = dict()
      for service in ServicesListItems:
        mycursor.execute('select Name from treatments where id = %s', (service[0],))
        ServicesDict[mycursor.fetchall()[0][0]] = service[1]

      colors = ["color-brown","color-black","color-blue","color-green","color-yellow","color-orange","color-red"]
      
      # Admin is loggedin show them the home page  
      return render_template('Admin/home.html',
                            titlePage="Admin Control Panel",
                            AvgOfRates=AvgOfRates,
                            AppointmentsList=AppointmentsList,
                            AppointmentsListPrecentage=AppointmentsListPrecentage,
                            DoctorsList=DoctorsList,
                            DoctorsListPrecentage=DoctorsListPrecentage,
                            ServicesDict=ServicesDict,
                            colors=colors)

    # Admin is not loggedin redirect to login page
    return redirect(url_for('login'))

@website.route('/Admin/', methods=['GET', 'POST'])
def login():

  if 'loggedinAdmin' in session:
    return redirect(url_for('Admin'))
  else :
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST':
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        
        # Check if account exists using MySQL
        mycursor.execute('SELECT * FROM admin WHERE UserName = %s AND Password = %s', (username, password,))
        
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
    return render_template('Admin/index.html', 
                            msg=msg, 
                            titlePage="Admin Control Panel",
                            hide="d-none",
                            login=True)

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
      if request.method == 'POST' :
          SSN = request.form['SSN']
          file = request.files['file']
          FName = request.form['FName']
          MidName = request.form['MidName']
          LName = request.form['LName']
          Phone = request.form['Phone']
          Gender = request.form['Gender']
          Email = request.form['Email']
          Age = request.form['Age']
          Degree = request.form['Degree']
          Password = get_random_number()

          mycursor.execute('SELECT * FROM doctors WHERE SSN = %s', (SSN, ))
          D_SSN = mycursor.fetchone()
          mycursor.execute('SELECT * FROM doctors WHERE Email = %s', (Email, ))
          emailAdd = mycursor.fetchone()

          # Check if SSN is repeated
          if D_SSN:
              msg = 'SSN already exists !'
          # Check if Email is repeated
          elif emailAdd :
              msg = 'Email already exists !'
          # Check if name contains only characters
          elif not re.match(r'[A-Za-z]+', FName):
              msg = 'First Name must contain only characters'
          elif not re.match(r'[A-Za-z]+', MidName):
              msg = 'Name must contain only characters'
          elif not re.match(r'[A-Za-z]+', LName):
              msg = 'Last Name must contain only characters'
          else:
              path = "static/img/doctorsProfile/" + secure_filename(file.filename)
              file.save(path)
              
              mycursor.execute("INSERT INTO doctors(SSN, FName, MidName, LName, Age, Gender, Phone, Email, Degree, Password, Image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                                                   (SSN, FName, MidName, LName, Age, Gender, Phone, Email, Degree, Password, path))
              mydb.commit()
              
              msg = 'You have successfully Added Doctor.'
              PassOrNot = "text-success"
      
      # Update all doctors data
      mycursor.execute("SELECT * FROM Doctors")
      DoctorsTable = mycursor.fetchall()

      # User is loggedin show them the home page  
      return render_template('Admin/doctors.html',
                            registered=PassOrNot, 
                            msg=msg, 
                            DoctorsData=DoctorsTable,
                            titlePage="Doctors Control Panel")

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@website.route('/Admin/General', methods=['GET', 'POST'])
def generalAdmin():
  if 'loggedinAdmin' in session:
    msg = ''
    if request.method == 'POST':
        title = request.form['title']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']
        short = request.form['short']
        long = request.form['long']
        icon = request.files['icon']

        path = "static/img/icon/icon.png" 
        icon.save(path)

        mycursor.execute("UPDATE site_information SET Title=%s, Address=%s, Email=%s, Phone=%s, Short_description=%s, Long_description=%s, Icon=%s", (title, address, email, phone, short, long, path))
        mydb.commit()
        msg = 'Updated successfully, please restart the website to update the changes.'

    # Retrieve slider images
    mycursor.execute("SELECT * FROM site_information")
    siteinfo = mycursor.fetchone()
    
    return render_template('Admin/general.html', 
                          msg=msg,
                          titlePage="Site Informtion Control Panel",
                          siteinfo=siteinfo)

  return redirect(url_for('login'))

@website.route('/Admin/slider', methods=['GET', 'POST'])
def sliderAdmin():
  if 'loggedinAdmin' in session:
    msg = ''
    if request.method == 'POST':
        file = request.files['file']
        title = request.form['title']
        Description = request.form['description']

        path = "static/img/slider/" + secure_filename(file.filename)
        file.save(path)
        
        mycursor.execute("INSERT INTO slider(Image, Title, Description) VALUES (%s, %s, %s)", 
                                            (path,  title, Description))
        mydb.commit()

        msg = 'Image Uploaded successfully'

    # Retrieve slider images
    mycursor.execute("SELECT * FROM slider")
    sliderImg = mycursor.fetchall()
    return render_template('Admin/Slider.html', 
                          msg=msg, 
                          titlePage="Slider Control Panel",
                          sliderImg=sliderImg)

  return redirect(url_for('login'))

@website.route('/Admin/users', methods=['GET', 'POST'])
def usersAdmin():
  if 'loggedinAdmin' in session:    
    # Retrieve slider images
    mycursor.execute("SELECT * FROM users")
    users = mycursor.fetchall()
    return render_template('Admin/users.html', 
                          titlePage="Users", 
                          users=users)

  return redirect(url_for('login'))

@website.route('/Admin/Services', methods=['GET', 'POST'])
def servicesAdmin():
  # Check if user is loggedin
    if 'loggedinAdmin' in session:
      msg = ''
      PassOrNot = "text-danger"
      if request.method == 'POST' :
          Name = request.form['Name']
          Image = request.files['file']
          Cost = request.form['Cost']
          Duration = request.form['Duration']
          Description = request.form['Description']

          path = "static/img/ServicesProfile/" + secure_filename(Image.filename)
          Image.save(path)

          mycursor.execute("INSERT INTO treatments(Image, Name, cost, Duration, Description) VALUES (%s, %s, %s, %s, %s)", 
                                                  (path,  Name, Cost, Duration, Description))
          mydb.commit()

          msg = 'You Have Successfully Added New Service/Treatment.'
          PassOrNot = "text-success"
      
      # Update all doctors data
      mycursor.execute("""SELECT * 
                          FROM treatments;""")

      servicesData = mycursor.fetchall()

      # User is loggedin show them the home page  
      return render_template('Admin/services.html',
                            titlePage="Doctors Control Panel",
                            registered=PassOrNot, 
                            msg=msg, 
                            servicesData=servicesData)

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@website.route('/Admin/Appointemnts', methods=['GET', 'POST'])
def appointmentsAdmin():
    if request.method == 'POST' :
        id = request.form['id']
        date = request.form['date']
        if request.form['status'] == 'Accepted':
          mycursor.execute('update appointments set Status="Accepted", App_date=%s WHERE id = %s', (date, id, ))
        else:
          mycursor.execute('update appointments set Status="Refused" WHERE id = %s', (id, ))
      
        mydb.commit()

    mycursor.execute("select * from Appointments")
    AppointmentsTable = mycursor.fetchall()
    
    Treatments = []
    Doctors = []
    Users = []

    mycursor.execute("select * from Appointments where UserID = %s",(session['id'],))
    AppointmentsTable = mycursor.fetchall()

    for Appointment in AppointmentsTable :
      mycursor.execute('SELECT * FROM doctors WHERE id = %s', (Appointment[10], ))
      D_Name = mycursor.fetchone()
      
      mycursor.execute('SELECT * FROM treatments WHERE id = %s', (Appointment[11], ))
      T_Name = mycursor.fetchone()

      Treatments.append(T_Name)
      Doctors.append(D_Name)
      
    return render_template('Admin/Appointments.html',
                            titlePage="Appointments Control Panel",
                            AppointmentsTable=AppointmentsTable)

#--------------------------------------------------------------------------#

# Run Website
if __name__ == "__main__":  
  # RUN
  website.run(debug=True,port=9000)