#!/usr/bin/python
from transaction.base_task import *
from service.message_define import *
from test_result_enum import *
from ts_format import *

class QueryOperateSummaryTask(BaseTask):
    operate_timeout = 10
    def __init__(self, task_type, messsage_handler,
                 case_manager,logger_name):
        self.case_manager = case_manager
        BaseTask.__init__(self, task_type, RequestDefine.query_operate_summary,
                          messsage_handler, logger_name)
        
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.query_operate_summary, result_success,
                             self.onQuerySuccess)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.query_operate_summary, result_fail,
                             self.onQueryFail)
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.timeout, result_any,
                             self.onQueryTimeout)        

    def invokeSession(self, session):
        """
        task start, must override
        """
        request = getRequest(RequestDefine.query_operate_summary)
        param = self.case_manager.getParam()
        control_server = param["control_server"]
        
        target = param["target"]
        targetlist = target.split(',')
        begin = param["begin"]
        end = param["end"]
        
        request.setStringArray(ParamKeyDefine.target, targetlist)
        request.setString(ParamKeyDefine.begin, begin)
        request.setString(ParamKeyDefine.end, end)
        
        request.session = session.session_id
        self.setTimer(session, self.operate_timeout)
        self.sendMessage(request, control_server)

    def onQuerySuccess(self, msg, session):
        self.clearTimer(session)
        title = []
        value = []

        title.append("node_name")
        value.append(msg.getStringArray(ParamKeyDefine.node_name))
        title.append("server_room")
        value.append(msg.getStringArray(ParamKeyDefine.server_room))
        title.append("computer_rack")
        value.append(msg.getStringArray(ParamKeyDefine.computer_rack))
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
       
        
        self.info("[%08X]query operate summary success"% (session.session_id))
        
        print_one_list(title,value)
        self.case_manager.finishTestCase(TestResultEnum.success)        
        session.finish()

    def onQueryFail(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]query operate summary fail"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.fail)
        session.finish()
        
    def onQueryTimeout(self, msg, session):
        self.info("[%08X]query operate summary timeout"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.timeout)
        session.finish()
