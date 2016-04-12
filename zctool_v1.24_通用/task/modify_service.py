#!/usr/bin/python
from transaction.base_task import *
from service.message_define import *
from test_result_enum import *
from ts_format import *

class ModifyServiceTask(BaseTask):
    operate_timeout = 20
    def __init__(self, task_type, messsage_handler,
                 case_manager,logger_name):
        self.case_manager = case_manager
        #logger_name = "task.modify_service"
        BaseTask.__init__(self, task_type, RequestDefine.modify_service,
                          messsage_handler, logger_name)
        
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.modify_service, result_success,
                             self.onQuerySuccess)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.modify_service, result_fail,
                             self.onQueryFail)
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.timeout, result_any,
                             self.onQueryTimeout)        

    def invokeSession(self, session):
        """
        task start, must override
        """
        request = getRequest(RequestDefine.modify_service)
        param = self.case_manager.getParam()
        control_server = param["control_server"]
        type = int(param["type"])     
        request.setUInt(ParamKeyDefine.type, type)
        target = param["target"]
        request.setString(ParamKeyDefine.target, target)
        disk_type = int(param["disk_type"])     
        request.setUInt(ParamKeyDefine.disk_type, disk_type)
        disk_source = param["disk_source"]  
        request.setString(ParamKeyDefine.disk_source, disk_source)
        crypt = param["crypt"]  
        request.setString(ParamKeyDefine.crypt, crypt)
        
        request.session = session.session_id
        self.setTimer(session, self.operate_timeout)
        self.sendMessage(request, control_server)

    def onQuerySuccess(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]modify_service success"%
                       (session.session_id))

        self.case_manager.finishTestCase(TestResultEnum.success)
        session.finish()
    def onQueryFail(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]query server rack fail"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.fail)
        session.finish()
        
    def onQueryTimeout(self, msg, session):
        self.info("[%08X]query server rack tiemout"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.timeout)
        session.finish()
