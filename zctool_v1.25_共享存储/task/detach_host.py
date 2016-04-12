#!/usr/bin/python
from transaction.base_task import *
from service.message_define import *
from test_result_enum import *

class DetachHostTask(BaseTask):
    operate_timeout = 5
    def __init__(self, task_type, messsage_handler,
                 case_manager,logger_name):
        self.case_manager = case_manager
        #logger_name = "task.start_host"
        BaseTask.__init__(self, task_type, RequestDefine.detach_host,
                          messsage_handler, logger_name)
        
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.detach_host, result_success,
                             self.onDetachSuccess)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.detach_host, result_fail,
                             self.onDetachFail)
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.timeout, result_any,
                             self.onDetachTimeout)        

    def invokeSession(self, session):
        """
        task start, must override
        """        
        request = getRequest(RequestDefine.detach_host)
        param = self.case_manager.getParam()
        #session.target = param["host"]
        control_server = param["control_server"]
        uuid = param["id"]
        host = param["host"]
        request.setString(ParamKeyDefine.uuid, uuid)
        request.setString(ParamKeyDefine.host, host)
        self.info("[%08X]request detach host host"%
                       (session.session_id))
        
        request.session = session.session_id
        self.setTimer(session, self.operate_timeout)
        self.sendMessage(request, control_server)
        
    def onDetachSuccess(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]detach host success"%
                       (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.success)        
        session.finish()

    def onDetachFail(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]detach host fail"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.fail)
        session.finish()
        
    def onDetachTimeout(self, msg, session):
        self.info("[%08X]detach host timeout"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.timeout)
        session.finish()
