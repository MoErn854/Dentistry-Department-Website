import mysql.connector

# Connecting with Database
def mysql_connector():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="stomology-dep"
    )

    # Initialize our cursor
    mycursor = mydb.cursor(buffered=True)

    return mydb, mycursor


"""Retrive Database Tables"""

def admin(mycursor) :
    'Retrieve all admin data'
    mycursor.execute("SELECT * FROM admin")
    admin_table = mycursor.fetchall()

    return admin_table

def site_information(mycursor) :
    'Retrieve site information data'
    mycursor.execute("SELECT * FROM site_information")
    site_info_table = mycursor.fetchone()
    
    return site_info_table

def slider(mycursor) :
    'Retrieve slider data'
    mycursor.execute("SELECT * FROM slider")
    slider_table = mycursor.fetchall()
    
    return slider_table

def doctors(mycursor) :
    'Retrieve all doctors data'
    mycursor.execute("SELECT * FROM doctors")
    doctors_table = mycursor.fetchall()
    
    return doctors_table

def treatments(mycursor) :
    'Retrieve all treatments data'
    mycursor.execute("SELECT * FROM treatments")
    treatments_table = mycursor.fetchall()
    
    return treatments_table

def appointments(mycursor) :
    'Retrieve all appointments data'
    mycursor.execute("SELECT * FROM appointments")
    appointments_table = mycursor.fetchall()

    return appointments_table

def users(mycursor) :
    'Retrieve all users data'
    mycursor.execute("SELECT * FROM users")
    users_table = mycursor.fetchall()

    return users_table

def rates(mycursor) :
    'Retrieve all rates data'
    mycursor.execute("SELECT * FROM rates limit 10")
    rates_table = mycursor.fetchall()
    
    return rates_table

def retrive_tables(mycursor) :
    tables = dict()

    tables["admin"] = admin(mycursor)
    tables["site_information"] = site_information(mycursor)
    tables["slider"] = slider(mycursor)
    tables["doctors"] = doctors(mycursor)
    tables["treatments"] = treatments(mycursor)
    tables["appointments"] = appointments(mycursor)
    tables["users"] = users(mycursor)
    tables["rates"] = rates(mycursor)

    return tables
