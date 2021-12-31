import mysql.connector

# Connect Database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="dentalhealth"
)

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM Doctors")

myresult = mycursor.fetchall()

print(myresult)
for i in myresult :