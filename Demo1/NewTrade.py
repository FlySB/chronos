#coding=utf-8

import chronos_api
import threading
import time
import chronos_sdk.Error as Error

_error_info_success = "业务操作成功。"
_error_code_success = 0
_error_info_failed  = "业务操作失败。"
_error_code_failed  = -1

class SyncTradeSpi(chronos_api.TradeSpi):
    def __init__(self):
        chronos_api.TradeSpi.__init__(self)
        self.mCondition = threading.Condition()
        self.mIsConnected = False
        self.mResult = None
        self.mErrorCode = _error_code_success
        self.mErrorInfo = _error_info_success
        self.mResultCount = 0
        self.mRequestId = 0

    def OnConnected(self):
        self.mIsConnected = True

    def OnDisconnect(self):
        self.mIsConnected = False

    def OnRspCancelOrder(self, cancel_order_ans):
        chronos_api.TradeSpi.OnRspCancelOrder(self, cancel_order_ans)
        self.mCondition.acquire()
        self.mErrorCode = _error_code_success
        self.mErrorInfo = _error_info_success
        self.mResult = cancel_order_ans
        self.mCondition.notify()
        self.mCondition.release()

    def OnRspError(self, rsp_code, request_id):
        chronos_api.TradeSpi.OnRspError(self, rsp_code, request_id)
        self.mCondition.acquire()
        if rsp_code is not None:
            self.mErrorCode = rsp_code.ret_code
            self.mErrorInfo = rsp_code.ret_msg
        else:
            self.mErrorCode = _error_code_failed
            self.mErrorInfo = _error_info_failed

        self.mRequestId = request_id
        self.mResult = None
        self.mCondition.notify()
        self.mCondition.release()

    def OnRspOrderRtn(self, order_status, fund=None, position=None):
        chronos_api.TradeSpi.OnRspOrderRtn(self, order_status, fund, position)

    def OnRspQueryFund(self, rsp_code, fund_arry, request_id):
        chronos_api.TradeSpi.OnRspQueryFund(self, rsp_code, fund_arry, request_id)
        self.mCondition.acquire()
        self.mErrorCode = rsp_code.ret_code
        self.mErrorInfo = rsp_code.ret_msg
        self.mResult = fund_arry
        self.mRequestId = request_id
        self.mCondition.notify()
        self.mCondition.release()

    def OnRspQueryOrder(self, rsp_code, order_status_array, request_id):
        chronos_api.TradeSpi.OnRspQueryOrder(self, rsp_code, order_status_array, request_id)
        self.mCondition.acquire()
        self.mErrorCode = rsp_code.ret_code
        self.mErrorInfo = rsp_code.ret_msg
        self.mResult = order_status_array
        self.mRequestId = request_id
        self.mCondition.notify()
        self.mCondition.release()

    def OnRspQueryPosition(self, rsp_code, position_array, request_id):
        chronos_api.TradeSpi.OnRspQueryPosition(self, rsp_code, position_array, request_id)
        self.mCondition.acquire()
        self.mErrorCode = rsp_code.ret_code
        self.mErrorInfo = rsp_code.ret_msg
        self.mResult = position_array
        self.mRequestId = request_id
        self.mCondition.notify()
        self.mCondition.release()

    def OnRspQueryUkeyInfo(self, rsp_code, handle, request_id):
        chronos_api.TradeSpi.OnRspQueryUkeyInfo(self, rsp_code, handle, request_id)
        self.mCondition.acquire()
        self.mErrorCode = rsp_code.ret_code
        self.mErrorInfo = rsp_code.ret_msg
        self.mResult = handle
        self.mRequestId = request_id
        self.mCondition.notify()
        self.mCondition.release()

    def OnRspSendOrder(self, send_order_ans):
        chronos_api.TradeSpi.OnRspSendOrder(self, send_order_ans)
        self.mCondition.acquire()
        self.mErrorCode = _error_code_success
        self.mErrorInfo = _error_info_success
        self.mResult = send_order_ans
        self.mCondition.notify()
        self.mCondition.release()

    def OnRspUserLogin(self, login_ans):
        chronos_api.TradeSpi.OnRspUserLogin(self, login_ans)
        self.mCondition.acquire()
        self.mErrorCode = _error_code_success
        self.mErrorInfo = _error_info_success
        self.mResult = login_ans
        self.mCondition.notify()
        self.mCondition.release()

    def OnRspUserLogout(self, logout_ans):
        chronos_api.TradeSpi.OnRspUserLogout(self, logout_ans)
        self.mCondition.acquire()
        self.mErrorCode = _error_code_success
        self.mErrorInfo = _error_info_success
        self.mResult = logout_ans
        self.mCondition.notify()
        self.mCondition.release()

class SyncTradeApi:
    def __init__(self, log_level = 0, log_dir = ""):
        self.mInitialized = False
        self.mTradeApi = chronos_api.TradeApi(log_level = log_level, log_dir = log_dir)
        self.mRequestId = 1

    def GetApiVersion(self):
        return self.mTradeApi.GetApiVersion()

    def Initialize(self, url, srv_id):
        if not self.mInitialized:
            self.SyncTradeSpi = SyncTradeSpi()
            self.mInitialized = True
        return self.mTradeApi.Initialize(url, self.SyncTradeSpi, srv_id)

    def Release(self):
        return self.mTradeApi.Release()

    def Connect(self, timeout = 10):
        t = 10 if timeout < 0 else timeout
        for i in range(1, t):
            if self.SyncTradeSpi.mIsConnected:
                return True
            else:
                time.sleep(1)
        return self.SyncTradeSpi.mIsConnected

    def IsConnected(self):
        return self.SyncTradeSpi.mIsConnected

    def ReqUserLogin(self, trade_user, fgs_user):
        self.SyncTradeSpi.mCondition.acquire()
        ret_code = self.mTradeApi.ReqUserLogin(trade_user, fgs_user)
        if ret_code != 0:
            self.SyncTradeSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncTradeSpi.mCondition.wait()

        return (self.SyncTradeSpi.mResult,
                self.SyncTradeSpi.mErrorCode,
                self.SyncTradeSpi.mErrorInfo)

    def ReqUserLogout(self):
        self.SyncTradeSpi.mCondition.acquire()
        ret_code = self.mTradeApi.ReqUserLogout()
        if ret_code != 0:
            self.SyncTradeSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncTradeSpi.mCondition.wait()

        return (self.SyncTradeSpi.mResult,
                self.SyncTradeSpi.mErrorCode,
                self.SyncTradeSpi.mErrorInfo)

    def ReqSendOrder(self, order):
        self.SyncTradeSpi.mCondition.acquire()
        ret_code = self.mTradeApi.ReqSendOrder(order)
        if ret_code != 0:
            self.SyncTradeSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncTradeSpi.mCondition.wait()

        return (self.SyncTradeSpi.mResult,
                self.SyncTradeSpi.mErrorCode,
                self.SyncTradeSpi.mErrorInfo)

    def ReqQueryFund(self, query_fund):
        self.SyncTradeSpi.mCondition.acquire()
        ret_code = self.mTradeApi.ReqQueryFund(query_fund, self.mRequestId)
        if ret_code != 0:
            self.SyncTradeSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncTradeSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncTradeSpi.mResult,
                self.SyncTradeSpi.mErrorCode,
                self.SyncTradeSpi.mErrorInfo)

    def ReqQueryPosition(self, query_position):
        self.SyncTradeSpi.mCondition.acquire()
        ret_code = self.mTradeApi.ReqQueryPosition(query_position, self.mRequestId)
        if ret_code != 0:
            self.SyncTradeSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncTradeSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncTradeSpi.mResult,
                self.SyncTradeSpi.mErrorCode,
                self.SyncTradeSpi.mErrorInfo)

    def ReqQueryOrder(self, query_order):
        self.SyncTradeSpi.mCondition.acquire()
        ret_code = self.mTradeApi.ReqQueryOrder(query_order, self.mRequestId)
        if ret_code != 0:
            self.SyncTradeSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncTradeSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncTradeSpi.mResult,
                self.SyncTradeSpi.mErrorCode,
                self.SyncTradeSpi.mErrorInfo)

    def ReqCancelOrder(self, cancel_order):
        self.SyncTradeSpi.mCondition.acquire()
        ret_code = self.mTradeApi.ReqCancelOrder(cancel_order)
        if ret_code != 0:
            self.SyncTradeSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncTradeSpi.mCondition.wait()

        return (self.SyncTradeSpi.mResult,
                self.SyncTradeSpi.mErrorCode,
                self.SyncTradeSpi.mErrorInfo)

    def ReqQueryUkeyInfo(self, ukey):
        self.SyncTradeSpi.mCondition.acquire()
        ret_code = self.mTradeApi.ReqQueryUkeyInfo(ukey, self.mRequestId)
        if ret_code != 0:
            self.SyncTradeSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncTradeSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncTradeSpi.mResult,
                self.SyncTradeSpi.mErrorCode,
                self.SyncTradeSpi.mErrorInfo)

    def ReqQueryUkeyInfoByCode(self, market_id, market_code):
        self.SyncTradeSpi.mCondition.acquire()
        ret_code = self.mTradeApi.ReqQueryUkeyInfoByCode(ukey, market_id, market_code, self.mRequestId)
        if ret_code != 0:
            self.SyncTradeSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncTradeSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncTradeSpi.mResult,
                self.SyncTradeSpi.mErrorCode,
                self.SyncTradeSpi.mErrorInfo)

    def ReqQueryUkeyInfoByType(self, market_id, variety):
        self.SyncTradeSpi.mCondition.acquire()
        ret_code = self.mTradeApi.ReqQueryUkeyInfoByType(market_id, variety, self.mRequestId)
        if ret_code != 0:
            self.SyncTradeSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncTradeSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncTradeSpi.mResult,
                self.SyncTradeSpi.mErrorCode,
                self.SyncTradeSpi.mErrorInfo)


