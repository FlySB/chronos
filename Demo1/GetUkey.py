import chronos_sdk
from NewQuote import SyncQuoteApi

def get_Ukey_by_code(Market, Code):
    SyncQuoteApi.Initialize()
    ukey_handle = None
    if Market == 'SH':
        market = chronos_sdk.MarketType.MARKET_SHA
    elif Market == 'SZ':
        market = chronos_sdk.MarketType.MARKET_SZA
    else:
        print("市场简称请输入SH或SZ")
        return
    result = SyncQuoteApi.ReqQueryUkeyInfoByCode(market, Code)
    print(result)
    if result[1] == 0:
        ukey_handle = result[0]
    else:
        print('ukey查询失败，错误代码%d，错误信息：%s' % (result[1], result[2]))
        return

    if ukey_handle is not None:
        ukey_info = chronos_sdk.UkeyInfo()
        if ukey_handle.GetUkeyInfoByCode(market, Code, ukey_info) == 0:
            print('查询成功：%s的UKEY编码为%d。' % (ukey_info.market_code_ex, ukey_info.ukey))
            return ukey_info.ukey
        else:
            print('查询失败！')
            return