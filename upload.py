import sqlite3
from datetime import datetime

now = datetime.now()
dt_string = now.strftime("%d-%m-%Y %H:%M:%S")

identity='mikocok10'
ip='6.6.6.10'
serial_number='6.6.6.6.6.10'
model='model10'
version='v11'
date_in="datetime(now)"

try:
    sqliteConnection = sqlite3.connect('ztp.db')
    cursor = sqliteConnection.cursor()
    cursor.execute("INSERT INTO device_info ({}, {}, {}, {}, {}, {}) VALUES('{}', '{}', '{}', '{}', '{}', '{}')".format('identity', 'ip_address', 'serial_number', 'model', 'version','date_in', identity, ip, serial_number, model, version,dt_string))
    sqliteConnection.commit()
    cursor.close()
except sqliteConnection.Error as error:
    sqliteConnection = sqlite3.connect('ztp.db')
    cursor = sqliteConnection.cursor()
    cursor.execute("update device_info set identity='{identity}', ip_address='{ip_address}', model='{model}', version='{version}', date_in='{date_in}' where serial_number='{sn}'".format( identity=identity, ip_address=ip, model=model, version=version, date_in=dt_string, sn=serial_number))
    sqliteConnection.commit()
    cursor.close()
finally:
    print("Sukses bro")



