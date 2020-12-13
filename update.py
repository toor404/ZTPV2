import sqlite3

sqliteConnection = sqlite3.connect('ztp.db')
cursor = sqliteConnection.cursor()
modelslct=cursor.execute("select model, count(model) as jumlah from device_info group by model")
model_reslt=cursor.fetchall()
sqliteConnection.commit()
cursor.close()

print(model_reslt)
