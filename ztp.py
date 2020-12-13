from flask import Flask, request, jsonify, render_template
from librouteros.query import Key
import paramiko 
import time
from librouteros import connect
import sqlite3
from datetime import datetime




app = Flask(__name__)

@app.route('/base')
def base():
    return render_template ('base.html')

@app.route('/')
def index():
    sqliteConnection = sqlite3.connect('ztp.db')
    cursor = sqliteConnection.cursor()
    cursor.execute("select * from device_info")
    datatest=cursor.fetchall()
    result_len2=len(datatest)
    modelslct2=cursor.execute("select model, count(model) as jumlah from device_info group by model")
    model_reslt2=cursor.fetchall()
    total_mdl=cursor.execute("select DISTINCT model from device_info")
    result_total_mdl=cursor.fetchall()
    result_total_mdl2=len(result_total_mdl)
    total_mdl=cursor.execute("select DISTINCT version from device_info")
    result_total_ver=cursor.fetchall()
    result_total_ver2=len(result_total_ver)
    return render_template ('index.html', datatest=datatest, result_len2=result_len2, mdlrslt2=model_reslt2, result_total_mdl=result_total_mdl2, result_total_ver=result_total_ver2)


@app.route('/tables')
def table():
    sqliteConnection = sqlite3.connect('ztp.db')
    cursor = sqliteConnection.cursor()
    cursor.execute("select * from device_info")
    data=cursor.fetchall()
    result_len=len(data)
    return render_template ('tables.html', data=data, result=result_len)


@app.route('/configure', methods=['POST'])
def configure():
    dats = request.get_json()
    ip = dats['ip_router']
    username = 'admin'
    password = ''

    #time
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")

    api = connect(
    username='admin',
    password='',
    host=ip,
    )
  
    #get info router using API
    router_board_info = api.path('system/routerboard')
    tuple(router_board_info)
    time.sleep(0.2)
    

    identity_info = api.path('system/identity')
    tuple(identity_info)
    time.sleep(0.2)

    for rbi in router_board_info:
        serial_number=rbi['serial-number']
        model=rbi['model']
        version=rbi['upgrade-firmware']
        time.sleep(0.2)

    
    for ii in identity_info:
        identity=ii['name']
        time.sleep(0.2)

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
        time.sleep(0.2)

    
    
    # connect to router using ssh
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip, username=username, password=password, allow_agent=False, look_for_keys=False, banner_timeout=200)

    config_list = [
        'system identity set name=Hotspot-Client',
        'user add name=support password=Letmein disabled=no group=full',
        'interface wireless enable wlan1',
        'interface wireless set mode=ap-bridge numbers=wlan1',
        'interface wireless set wlan1 ssid=Fariz-HotSpot',
        'ip firewall nat add chain=srcnat out-interface=ether1 action=masquerade',
        'ip address add address=172.168.2.1/24 interface=wlan1',
        'ip pool add name=dhcp_hotspot ranges=172.168.2.2-172.168.2.254',
        'ip dhcp-server add address-pool=dhcp_hotspot disabled=no interface=wlan1 name=hotspot',
        'ip dhcp-server network add address=172.168.2.0/24 dns-server=8.8.8.8 gateway=172.168.2.1',
        'ip dns set servers=8.8.8.8',
        'ip hotspot profile add dns-name=fariz.net hotspot-address=172.168.2.1 name=hotspot1',
        'ip hotspot add address-pool=dhcp_hotspot disabled=no interface=wlan1 name=hotspot1 profile=hotspot1',
        'ip hotspot user add name=fariz password=Letmein99',
    ]
    
    for config in config_list:
        ssh_client.exec_command(config)
        time.sleep(0.2)
        

    data = {'status': 'ok'}

    return jsonify(data)


#host dibawah adalah ip server ZTP
if __name__ == '__main__':
    app.run(host='172.16.29.10', debug=True)