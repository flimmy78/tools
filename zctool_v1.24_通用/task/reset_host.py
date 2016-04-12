#!/usr/bin/python
from transaction.base_task import *
from service.message_define import *
from test_result_enum import *

class ResetHostTask(BaseTask):
    operate_timeout = 5
    def __init__(self, task_type, messsage_handler,
                 case_manager,logger_name):
        self.case_manager = case_manager
        #logger_name = "task.stop_host"
        BaseTask.__init__(self, task_type, RequestDefine.reset_host,
                          messsage_handler, logger_name)
        
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.reset_host, result_success,
                             self.onResetSuccess)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.reset_host, result_fail,
                             self.onResetFail)
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.timeout, result_any,
                             self.onResetTimeout)        

    def invokeSession(self, session):
        """
        task start, must override
        """        
        request = getRequest(RequestDefine.reset_host)
        param = self.case_manager.getParam()
        session.target = param["host"]
        control_server = param["control_server"]
        request.setString(ParamKeyDefine.uuid, param["host"])
        self.info("[%08X]request reset host '%s' to control server '%s'"%
                       (session.session_id, session.target, control_server))
        
        request.session = session.session_id
        self.setTimer(session, self.operate_timeout)
        self.sendMessage(request, control_server)
        
    def onResetSuccess(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]reset host success"%
                       (session.session_id))
        
        self.case_manager.finishTestCase(TestResultEnum.success)        
        session.finish()

    def onResetFail(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]reset host fail"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.fail)
        session.finish()
        
    def onResetTimeout(self, msg, session):
        self.info("[%08X]reset host timeout"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.timeout)
        session.finish()
