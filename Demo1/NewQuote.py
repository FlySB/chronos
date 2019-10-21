# -*- coding: utf-8 -*-

import chronos_api
import threading
import time
import chronos_sdk.Error as Error

_error_info_success = "业务操作成功。"
_error_code_success = 0
_error_info_failed  = "业务操作失败。"
_error_code_failed  = -1

class SyncQuoteSpi(chronos_api.QuoteSpi):
    def __init__(self):
        chronos_api.QuoteSpi.__init__(self)
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

    def OnRspQueryUkeyInfo(self, rsp_code, handle, request_id):
        chronos_api.QuoteSpi.OnRspQueryUkeyInfo(self, rsp_code, handle, request_id)
        self.mCondition.acquire()
        self.mErrorCode = rsp_code.ret_code
        self.mErrorInfo = rsp_code.ret_msg
        self.mResult = handle
        self.mRequestId = request_id
        self.mCondition.notify()
        self.mCondition.release()

    def OnRspUserLogin(self, login_ans):
        chronos_api.QuoteSpi.OnRspUserLogin(self, login_ans)
        self.mCondition.acquire()
        self.mErrorCode = _error_code_success
        self.mErrorInfo = _error_info_success
        self.mResult = login_ans
        self.mCondition.notify()
        self.mCondition.release()

    def OnRspUserLogout(self, logout_ans):
        chronos_api.QuoteSpi.OnRspUserLogout(self, logout_ans)
        self.mCondition.acquire()
        self.mErrorCode = _error_code_success
        self.mErrorInfo = _error_info_success
        self.mResult = logout_ans
        self.mCondition.notify()
        self.mCondition.release()

    def OnRspError(self, rsp_code, request_id):
        chronos_api.QuoteSpi.OnRspError(self, rsp_code, request_id)
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

    def OnRspQuerySecumaster(self, rsp_code, ukey_handle, request_id):
        chronos_api.QuoteSpi.OnRspQuerySecumaster(self, rsp_code, ukey_handle, request_id)
        self.mCondition.acquire()
        self.mErrorCode = rsp_code.ret_code
        self.mErrorInfo = rsp_code.ret_msg
        self.mResult = ukey_handle
        self.mRequestId = request_id
        self.mCondition.notify()
        self.mCondition.release()

    def OnRspQueryFuturesContractPro(self, rsp_code, ukey_handle, request_id):
        chronos_api.QuoteSpi.OnRspQueryFuturesContractPro(self, rsp_code, ukey_handle, request_id)
        self.mCondition.acquire()
        self.mErrorCode = rsp_code.ret_code
        self.mErrorInfo = rsp_code.ret_msg
        self.mResult = ukey_handle
        self.mRequestId = request_id
        self.mCondition.notify()
        self.mCondition.release()

    def OnRspQueryMarket(self, rsp_code, ukey_handle, request_id):
        chronos_api.QuoteSpi.OnRspQueryMarket(self, rsp_code, ukey_handle, request_id)
        self.mCondition.acquire()
        self.mErrorCode = rsp_code.ret_code
        self.mErrorInfo = rsp_code.ret_msg
        self.mResult = ukey_handle
        self.mRequestId = request_id
        self.mCondition.notify()
        self.mCondition.release()

    def OnRspQueryEtfComponent(self, rsp_code, ukey_handle, request_id):
        chronos_api.QuoteSpi.OnRspQueryEtfComponent(self, rsp_code, ukey_handle, request_id)
        self.mCondition.acquire()
        self.mErrorCode = rsp_code.ret_code
        self.mErrorInfo = rsp_code.ret_msg
        self.mResult = ukey_handle
        self.mRequestId = request_id
        self.mCondition.notify()
        self.mCondition.release()

    def _OnEmptyResult(self, rsp_code, request_id):
        self.mCondition.acquire()
        self.mResult = []
        self.mResultCount = 0
        self.mErrorCode = rsp_code.ret_code
        self.mErrorInfo = rsp_code.ret_msg
        self.mRequestId = request_id
        self.mCondition.notify()
        self.mCondition.release()

    def OnRspQueryRightsIssue(self, rsp_code, data_list, request_id, page_num, page_cur):
        chronos_api.QuoteSpi.OnRspQueryRightsIssue(self, rsp_code, data_list, request_id, page_num, page_cur)
        if page_num == 0:
            self._OnEmptyResult(rsp_code, request_id)
            return

        if self.mResultCount == 0:
            self.mCondition.acquire()
            self.mResult = [None] * page_num
        self.mResult[page_cur - 1] = data_list
        self.mResultCount = self.mResultCount + 1
        if self.mResultCount == page_num:
            RealResult = []
            for page in self.mResult:
                RealResult.extend(page)
            self.mResult = RealResult
            self.mResultCount = 0
            self.mCondition.notify()
            self.mCondition.release()
            self.mErrorCode = rsp_code.ret_code
            self.mErrorInfo = rsp_code.ret_msg
            self.mRequestId = request_id

    def OnRspQueryDividend(self, rsp_code, data_list, request_id, page_num, page_cur):
        chronos_api.QuoteSpi.OnRspQueryDividend(self, rsp_code, data_list, request_id, page_num, page_cur)
        if page_num == 0:
            self._OnEmptyResult(rsp_code, request_id)
            return

        if self.mResultCount == 0:
            self.mCondition.acquire()
            self.mResult = [None] * page_num
        self.mResult[page_cur - 1] = data_list
        self.mResultCount = self.mResultCount + 1
        if self.mResultCount == page_num:
            RealResult = []
            for page in self.mResult:
                RealResult.extend(page)
            self.mResult = RealResult
            self.mResultCount = 0
            self.mCondition.notify()
            self.mCondition.release()
            self.mErrorCode = rsp_code.ret_code
            self.mErrorInfo = rsp_code.ret_msg
            self.mRequestId = request_id

    def OnRtnMdSnapshot(self, snapshot):
        chronos_api.QuoteSpi.OnRtnMdSnapshot(self,snapshot)
        self.mCondition.acquire()
        self.mResult = snapshot
        self.mCondition.notify()
        self.mCondition.release()

    def OnRspQueryMdSnapshot(self, rsp_code, data_list, request_id, page_num, page_cur):
        chronos_api.QuoteSpi.OnRspQueryMdSnapshot(self, rsp_code, data_list, request_id, page_num, page_cur)
        if page_num == 0:
            self._OnEmptyResult(rsp_code, request_id)
            return

        if self.mResultCount == 0:
            self.mCondition.acquire()
            self.mResult = [None] * page_num
        self.mResult[page_cur - 1] = data_list
        self.mResultCount = self.mResultCount + 1
        if self.mResultCount == page_num:
            RealResult = []
            for page in self.mResult:
                RealResult.extend(page)
            self.mResult = RealResult
            self.mResultCount = 0
            self.mCondition.notify()
            self.mCondition.release()
            self.mErrorCode = rsp_code.ret_code
            self.mErrorInfo = rsp_code.ret_msg
            self.mRequestId = request_id

    def OnRspQueryMdTransaction(self, rsp_code, data_list, request_id, page_num, page_cur):
        chronos_api.QuoteSpi.OnRspQueryMdTransaction(self, rsp_code, data_list, request_id, page_num, page_cur)
        if page_num == 0:
            self._OnEmptyResult(rsp_code, request_id)
            return

        if self.mResultCount == 0:
            self.mCondition.acquire()
            self.mResult = [None] * page_num
        self.mResult[page_cur - 1] = data_list
        self.mResultCount = self.mResultCount + 1
        if self.mResultCount == page_num:
            RealResult = []
            for page in self.mResult:
                RealResult.extend(page)
            self.mResult = RealResult
            self.mResultCount = 0
            self.mCondition.notify()
            self.mCondition.release()
            self.mErrorCode = rsp_code.ret_code
            self.mErrorInfo = rsp_code.ret_msg
            self.mRequestId = request_id

    def OnRspQueryMdOrder(self, rsp_code, data_list, request_id, page_num, page_cur):
        chronos_api.QuoteSpi.OnRspQueryMdOrder(self, rsp_code, data_list, request_id, page_num, page_cur)
        if page_num == 0:
            self._OnEmptyResult(rsp_code, request_id)
            return

        if self.mResultCount == 0:
            self.mCondition.acquire()
            self.mResult = [None] * page_num
        self.mResult[page_cur - 1] = data_list
        self.mResultCount = self.mResultCount + 1
        if self.mResultCount == page_num:
            RealResult = []
            for page in self.mResult:
                RealResult.extend(page)
            self.mResult = RealResult
            self.mResultCount = 0
            self.mCondition.notify()
            self.mCondition.release()
            self.mErrorCode = rsp_code.ret_code
            self.mErrorInfo = rsp_code.ret_msg
            self.mRequestId = request_id

    def OnRspQueryMdOrderQueue(self, rsp_code, data_list, request_id, page_num, page_cur):
        chronos_api.QuoteSpi.OnRspQueryMdOrderQueue(self, rsp_code, data_list, request_id, page_num, page_cur)
        if page_num == 0:
            self._OnEmptyResult(rsp_code, request_id)
            return

        if self.mResultCount == 0:
            self.mCondition.acquire()
            self.mResult = [None] * page_num
        self.mResult[page_cur - 1] = data_list
        self.mResultCount = self.mResultCount + 1
        if self.mResultCount == page_num:
            RealResult = []
            for page in self.mResult:
                RealResult.extend(page)
            self.mResult = RealResult
            self.mResultCount = 0
            self.mCondition.notify()
            self.mCondition.release()
            self.mErrorCode = rsp_code.ret_code
            self.mErrorInfo = rsp_code.ret_msg
            self.mRequestId = request_id

    def OnRspQueryMdKLineMinute(self, rsp_code, data_list, request_id, page_num, page_cur):
        chronos_api.QuoteSpi.OnRspQueryMdKLineMinute(self, rsp_code, data_list, request_id, page_num, page_cur)
        if page_num == 0:
            self._OnEmptyResult(rsp_code, request_id)
            return

        if self.mResultCount == 0:
            self.mCondition.acquire()
            self.mResult = [None] * page_num
        self.mResult[page_cur - 1] = data_list
        self.mResultCount = self.mResultCount + 1
        if self.mResultCount == page_num:
            RealResult = []
            for page in self.mResult:
                RealResult.extend(page)
            self.mResult = RealResult
            self.mResultCount = 0
            self.mCondition.notify()
            self.mCondition.release()
            self.mErrorCode = rsp_code.ret_code
            self.mErrorInfo = rsp_code.ret_msg
            self.mRequestId = request_id

    def OnRspQueryMdKLineDay(self, rsp_code, data_list, request_id, page_num, page_cur):
        chronos_api.QuoteSpi.OnRspQueryMdKLineDay(self, rsp_code, data_list, request_id, page_num, page_cur)
        if page_num == 0:
            self._OnEmptyResult(rsp_code, request_id)
            return

        if self.mResultCount == 0:
            self.mCondition.acquire()
            self.mResult = [None] * page_num
        self.mResult[page_cur - 1] = data_list
        self.mResultCount = self.mResultCount + 1
        if self.mResultCount == page_num:
            RealResult = []
            for page in self.mResult:
                RealResult.extend(page)
            self.mResult = RealResult
            self.mResultCount = 0
            self.mCondition.notify()
            self.mCondition.release()
            self.mErrorCode = rsp_code.ret_code
            self.mErrorInfo = rsp_code.ret_msg
            self.mRequestId = request_id

class SyncQuoteApi:
    def __init__(self, log_level = 0, log_dir = ""):
        self.mInitialized = False
        self.mQuoteApi = chronos_api.QuoteApi(log_level = log_level, log_dir = log_dir)
        self.mRequestId = 1

    def GetApiVersion(self):
        return self.mQuoteApi.GetApiVersion()

    def Initialize(self, url):
        if not self.mInitialized:
            self.SyncQuoteSpi = SyncQuoteSpi()
            self.mInitialized = True
        return self.mQuoteApi.Initialize(url, self.SyncQuoteSpi)

    def Release(self):
        return self.mQuoteApi.Release()

    def Connect(self, timeout = 10):
        t = 10 if timeout < 0 else timeout
        for i in range(1, t):
            if self.SyncQuoteSpi.mIsConnected:
                return True
            else:
                time.sleep(1)
        return self.SyncQuoteSpi.mIsConnected

    def IsConnected(self):
        return self.SyncQuoteSpi.mIsConnected

    def ReqUserLogin(self, fgs_user):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.ReqUserLogin(fgs_user)
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncQuoteSpi.mCondition.wait()

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    def ReqUserLogout(self):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.ReqUserLogout()
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncQuoteSpi.mCondition.wait()

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    def ReqQueryUkeyInfo(self, ukey):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.ReqQueryUkeyInfo(ukey, self.mRequestId)
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncQuoteSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    def ReqQueryUkeyInfoByCode(self, market_id, market_code):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.ReqQueryUkeyInfoByCode(market_id, market_code, self.mRequestId)
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncQuoteSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    def SubscribeMdSnapshot(self, ukey):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.SubscribeMdSnapshot(ukey)
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))
        self.SyncQuoteSpi.mCondition.wait()

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    def ReqQueryUkeyInfoByType(self, market_id, variety):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.ReqQueryUkeyInfoByType(market_id, variety, self.mRequestId)
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncQuoteSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    def ReqQuerySecumaster(self, ukey, date):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.ReqQuerySecumaster(ukey, date, self.mRequestId)
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncQuoteSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    def ReqQuerySecumasterByType(self, market_id, variety_id, date):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.ReqQuerySecumasterByType(market_id, variety_id, date, self.mRequestId)
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncQuoteSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    def ReqQueryFuturesContractProById(self, contract_id):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.ReqQueryFuturesContractProById(contract_id, self.mRequestId)
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncQuoteSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    def ReqQueryMarketById(self, market_id):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.ReqQueryMarketById(market_id, self.mRequestId)
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncQuoteSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    def ReqQueryETFComponentList(self, component_id):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.ReqQueryETFComponentList(component_id, self.mRequestId)
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncQuoteSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    def ReqQueryRightsIssueByNoticeDate(self, ukey, date_start, date_end, status):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.ReqQueryRightsIssueByNoticeDate(ukey, date_start, date_end, status, self.mRequestId)
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncQuoteSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    def ReqQueryRightsIssueByXrDate(self, ukey, date_start, date_end):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.ReqQueryRightsIssueByXrDate(ukey, date_start, date_end, self.mRequestId)
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncQuoteSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    def ReqQueryDividendByNoticeDate(self, ukey, date_start, date_end, status):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.ReqQueryDividendByNoticeDate(ukey, date_start, date_end, status, self.mRequestId)
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncQuoteSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    def ReqQueryDividendByXdDate(self, ukey, date_start, date_end):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.ReqQueryDividendByXdDate(ukey, date_start, date_end, self.mRequestId)
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncQuoteSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    def ReqQueryMdSnapshot(self, ukey_array, time_start, time_end):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.ReqQueryMdSnapshot(ukey_array, time_start, time_end, self.mRequestId)
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncQuoteSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    def ReqQueryMdTransaction(self, ukey_array, time_start, time_end):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.ReqQueryMdTransaction(ukey_array, time_start, time_end, self.mRequestId)
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncQuoteSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    def ReqQueryMdOrder(self, ukey_array, time_start, time_end):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.ReqQueryMdOrder(ukey_array, time_start, time_end, self.mRequestId)
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncQuoteSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    def ReqQueryMdOrderQueue(self, ukey_array, time_start, time_end):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.ReqQueryMdOrderQueue(ukey_array, time_start, time_end, self.mRequestId)
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncQuoteSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    def ReqQueryMdKLineMinute(self, ukey_array, time_start, time_end):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.ReqQueryMdKLineMinute(ukey_array, time_start, time_end, self.mRequestId)
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncQuoteSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    def ReqQueryMdKLineDay(self, ukey_array, time_start, time_end):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.ReqQueryMdKLineDay(ukey_array, time_start, time_end, self.mRequestId)
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncQuoteSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    def ReqQueryMdSnapshotBackward(self, ukey_array, time_end, n):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.ReqQueryMdSnapshotBackward(ukey_array, time_end, n, self.mRequestId)
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncQuoteSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    def ReqQueryMdTransactionBackward(self, ukey_array, time_end, n):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.ReqQueryMdTransactionBackward(ukey_array, time_end, n, self.mRequestId)
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncQuoteSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    def ReqQueryMdOrderBackward(self, ukey_array, time_end, n):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.ReqQueryMdOrderBackward(ukey_array, time_end, n, self.mRequestId)
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncQuoteSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    def ReqQueryMdOrderQueueBackward(self, ukey_array, time_end, n):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.ReqQueryMdOrderQueueBackward(ukey_array, time_end, n, self.mRequestId)
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncQuoteSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    def ReqQueryMdKLineMinuteBackward(self, ukey_array, time_end, n):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.ReqQueryMdKLineMinuteBackward(ukey_array, time_end, n, self.mRequestId)
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncQuoteSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    def ReqQueryMdKLineDayBackward(self, ukey_array, time_end, n):
        self.SyncQuoteSpi.mCondition.acquire()
        ret_code = self.mQuoteApi.ReqQueryMdKLineDayBackward(ukey_array, time_end, n, self.mRequestId)
        if ret_code != 0:
            self.SyncQuoteSpi.mCondition.release()
            return (None, ret_code, Error.GetErrorInfo(ret_code))

        self.SyncQuoteSpi.mCondition.wait()
        self.mRequestId = self.mRequestId + 1

        return (self.SyncQuoteSpi.mResult,
                self.SyncQuoteSpi.mErrorCode,
                self.SyncQuoteSpi.mErrorInfo)

    # def TimeFromString(self, time):
    #     return mQuoteApi.TimeFromString(time)

