import MySQLdb

connection = MySQLdb.connect(host="localhost", user="root", passwd="Kaoutar08Ftouhi", db="medical_database")
c = connection.cursor()
c.execute("SELECT * FROM patient_database")
rows = c.fetchall()
for eachRow in rows:
    print(eachRow)



