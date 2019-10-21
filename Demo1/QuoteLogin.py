from NewQuote import SyncQuoteApi

def QuoteLogin(url, fgs_user):
    quote_api = SyncQuoteApi()
    quote_api.Initialize(url)
    ok = quote_api.Connect()
    if quote_api.IsConnected():
        print('quote_api已经连接到%s' % url)
    else:
        print('quote_api无法连接到%s' % url)
    quote_result = quote_api.ReqUserLogin(fgs_user)
    if quote_result[1] == 0:
        print('quote_api登陆成功，返回消息：%s' % quote_result[0].ret_msg)
    else:
        print('quote_api登陆失败，错误代码%d，错误信息：%s' % (quote_result[1], quote_result[2]))
