import sqlite3

conn = sqlite3.connect('ztp.db')
print ("Opened database successfully");

conn.execute('CREATE TABLE device_info (identity TEXT, ip_address TEXT, serial_number TEXT PRIMARY KEY, model TEXT, version TEXT, date_in TEXT)')
print ("Table created successfully");
conn.close()