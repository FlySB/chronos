import chronos_sdk
from QuoteLogin import QuoteLogin
from TradeLogin import TradeLogin
from Test import get_Ukey_by_code

url = 'ssl://139.159.228.12:8001'

fgs_user = chronos_sdk.FgsUser()
fgs_user.login_code  = 'uestctest'
fgs_user.password    = 'uestc123!'
fgs_user.login_type  = chronos_sdk.LoginType.kUserName

trade_user = chronos_sdk.TradeUser()
trade_user.account_type   = chronos_sdk.AccountType.kActGeneral
trade_user.data_mode      = chronos_sdk.DataMode.kDmAccountAll
trade_user.trade_identity = chronos_sdk.TradeIdentity.kTiPortfolio
trade_user.id             = 15050001
trade_user.password       = ''
trade_user.bacid          = ''
trade_user.bacidcard      = ''
ServiceID = chronos_sdk.ServiceID.kServiceCOMS




QuoteLogin(url, fgs_user)
Ukey = get_Ukey_by_code('SH','603068')
