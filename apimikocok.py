import jsonify
from librouteros import connect
from librouteros.query import Key
api = connect(
    username='support',
    password='Letmein',
    host='192.168.100.11',
)

router_board_info = api.path('system/routerboard')
tuple(router_board_info)

identity_info = api.path('system/identity')
tuple(identity_info)

for rbi in router_board_info:
    serial_number=rbi['serial-number']
    model=rbi['model']
    version=rbi['upgrade-firmware']


for ii in identity_info:
    identity=ii['name']


print('Hostname: '+identity)
print('Serial Number: '+serial_number)
print('Model: '+ str(model))
print('Verison: '+version)