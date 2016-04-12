#!/usr/bin/python
from transaction.base_task import *
from service.message_define import *
from test_result_enum import *
from ts_format import *

class QueryServiceSummaryTask(BaseTask):
    operate_timeout = 10
    def __init__(self, task_type, messsage_handler,
                 case_manager,logger_name):
        self.case_manager = case_manager
        BaseTask.__init__(self, task_type, RequestDefine.query_service_summary,
                          messsage_handler, logger_name)
        
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.query_service_summary, result_success,
                             self.onQuerySuccess)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.query_service_summary, result_fail,
                             self.onQueryFail)
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.timeout, result_any,
                             self.onQueryTimeout)        

    def invokeSession(self, session):
        """
        task start, must override
        """
        request = getRequest(RequestDefine.query_service_summary)
        param = self.case_manager.getParam()
        control_server = param["control_server"]
        
        target = param["target"]
        targetlist = target.split(',')
        #level = param["level"]
        begin = param["begin"]
        end = param["end"]
        
        request.setString(ParamKeyDefine.target, targetlist)
        #request.setString(ParamKeyDefine.level, level)
        request.setString(ParamKeyDefine.begin, begin)
        request.setString(ParamKeyDefine.end, end)
        
        request.session = session.session_id
        self.setTimer(session, self.operate_timeout)
        self.sendMessage(request, control_server)

    def onQuerySuccess(self, msg, session):
        self.clearTimer(session)
        title = []
        value = []

        title.append("name")
        value.append(msg.getStringArray(ParamKeyDefine.name))
        title.append("uuid")
        value.append(msg.getStringArray(ParamKeyDefine.uuid))
        title.append("cpu_count")
        value.append(msg.getUIntArray(ParamKeyDefine.cpu_count))        
        title.append("total_volume")
        value.append(msg.getUIntArray(ParamKeyDefine.total_volume))
        title.append("used_volume")
        value.append(msg.getUIntArray(ParamKeyDefine.used_volume))
        title.append("cpu_seconds")
        value.append(msg.getFloatArray(ParamKeyDefine.cpu_seconds))             
        title.append("read_bytes")
        value.append(msg.getUIntArray(ParamKeyDefine.read_bytes))
        title.append("write_bytes")
        value.append(msg.getUIntArray(ParamKeyDefine.write_bytes))
        title.append("received_bytes")
        value.append(msg.getUIntArray(ParamKeyDefine.received_bytes))
        title.append("sent_bytes")
        value.append(msg.getUIntArray(ParamKeyDefine.sent_bytes))
        
        self.info("[%08X]query service summary success" % (session.session_id))
             
        #print_one_result(querydata)
        print_one_list(title,value)
        self.case_manager.finishTestCase(TestResultEnum.success)        
        session.finish()

    def onQueryFail(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]query service summary fail"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.fail)
        session.finish()
        
    def onQueryTimeout(self, msg, session):
        self.info("[%08X]query service summary timeout"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.timeout)
        session.finish()
