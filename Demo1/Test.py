import chronos_sdk
from Time import time_t
from NewQuote import SyncQuoteApi
from NewTrade import SyncTradeApi


url = 'ssl://139.159.228.12:8001'
fgs_user = chronos_sdk.FgsUser()

fgs_user.login_code  = 'uestctest'
fgs_user.password    = 'uestc123!'
fgs_user.login_type  = chronos_sdk.LoginType.kUserName

trade_user = chronos_sdk.TradeUser()
trade_user.account_type   = chronos_sdk.AccountType.kActGeneral
trade_user.bacid          = ''
trade_user.bacidcard      = ''
trade_user.data_mode      = chronos_sdk.DataMode.kDmAccountAll
trade_user.id             = 15050001
trade_user.password       = ''
trade_user.trade_identity = chronos_sdk.TradeIdentity.kTiPortfolio

trade_api = SyncTradeApi()
trade_api.Initialize(url, chronos_sdk.ServiceID.kServiceCOMS)
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


def get_Ukey_by_code(Market, code):
    ukey_handle = None
    if Market == 'SH':
        market = chronos_sdk.MarketType.MARKET_SHA
    elif Market == 'SZ':
        market = chronos_sdk.MarketType.MARKET_SZA
    else:
        print("市场简称请输入SH或SZ")
        return
    result = quote_api.ReqQueryUkeyInfoByCode(market, code)
    print(result)
    if result[1] == 0:
        ukey_handle = result[0]
    else:
        print('ukey查询失败，错误代码%d，错误信息：%s' % (result[1], result[2]))
        return

    if ukey_handle is not None:
        ukey_info = chronos_sdk.UkeyInfo()
        if ukey_handle.GetUkeyInfoByCode(market, code, ukey_info) == 0:
            print('查询成功：%s的UKEY编码为%d。' % (ukey_info.market_code_ex, ukey_info.ukey))
            return ukey_info.ukey
        else:
            print('查询失败！')
            return


x = get_Ukey_by_code('SH','603068')
print(x)


out = quote_api.ReqQueryMdSnapshot([x], time_t("2019-10-8 10:30:00"), time_t("2019-10-8 10:31:00"))
for sp in out[0]:
    print(sp.high)







