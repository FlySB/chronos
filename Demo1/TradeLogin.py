from NewTrade import SyncTradeApi
def TradeLogin(url, SerciceID, trade_user, fgs_user):
    trade_api = SyncTradeApi()
    trade_api.Initialize(url, SerciceID)
    ok = trade_api.Connect()
    if trade_api.IsConnected():
        print('trade_api已经连接到%s' % url)
    else:
        print('trade_api无法连接到%s' % url)
    trade_result = trade_api.ReqUserLogin(trade_user, fgs_user)
    if trade_result[1] == 0:
        print('trade_api登陆成功，返回消息：%s' % trade_result[0].ret_msg)
    else:
        print('trade_api登陆失败，错误代码%d，错误信息：%s' % (trade_result[1], trade_result[2]))