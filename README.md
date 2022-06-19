# Dentist Clinic Website

A responsive full stack web application with administration panel and dentistry appointment booking system.

## Features

- Sign Up & Login
- The application enable the user to make an appointment in specific date.
- Contact us forms for any complains or special request.
- The application is synchronized with calender for doctors.
- The application use static files, file uploads
- Administration panal:
  - The admin can edit the appointments, accept & refuse it, assign it to the doctors.
  - Statistical analysis for the admin entry.

### Prerequisites
<hr>
1- python 3 
[Install](https://www.python.org/downloads/)

2- The Following Libraries :
```
typing
dns.flags
flask
mysql.connector
re
werkzeug.utils
random
string
flask_wtf
wtforms
flask_mail
json
```
**To install** :
`pip install [library name]`

### How to Run
<hr>

#### First : You need to run stomology-department.sql file to setup the database.

#### Second : Edit the database information for connection (line 37).
![Database Connection](https://github.com/MoErn854/Dentistry-Department-Website/blob/main/ReadMeimg/database.png)

#### Third : Run main.py file by command :
```
cd [Folder Path]
python3 main.py
```

Finally, you can go to http://127.0.0.1:9000/ .

**Enjoy :)**

![Website Capture](https://github.com/MoErn854/Dentistry-Department-Website/blob/main/ReadMeimg/Website.png)
