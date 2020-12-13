from librouteros import connect
api = connect(
    username='admin',
    password='',
    host='172.16.29.79',
    )

router_board_info = api.path('system/routerboard/')
result=tuple(router_board_info)
print(result)