#!/usr/bin/python
from transaction.base_task import *
from service.message_define import *
from test_result_enum import *

class StartNetworkTask(BaseTask):
    operate_timeout = 5
    def __init__(self, task_type, messsage_handler,
                 case_manager,logger_name):
        self.case_manager = case_manager
        #logger_name = "task.start_host"
        BaseTask.__init__(self, task_type, RequestDefine.start_network,
                          messsage_handler, logger_name)
        
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.start_network, result_success,
                             self.onStartSuccess)
        self.addTransferRule(state_initial, AppMessage.RESPONSE,
                             RequestDefine.start_network, result_fail,
                             self.onStartFail)
        self.addTransferRule(state_initial, AppMessage.EVENT,
                             EventDefine.timeout, result_any,
                             self.onStartTimeout)        

    def invokeSession(self, session):
        """
        task start, must override
        """        
        request = getRequest(RequestDefine.start_network)
        param = self.case_manager.getParam()
        #session.target = param["host"]
        control_server = param["control_server"]
        uuid = param["id"]
        #request.setString(ParamKeyDefine.uuid, param["id"])
        request.setString(ParamKeyDefine.uuid, uuid)
        self.info("[%08X]request start network"%
                       (session.session_id))
        
        request.session = session.session_id
        self.setTimer(session, self.operate_timeout)
        self.sendMessage(request, control_server)
        
    def onStartSuccess(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]start network success"%
                       (session.session_id))
        
        self.case_manager.finishTestCase(TestResultEnum.success)        
        session.finish()

    def onStartFail(self, msg, session):
        self.clearTimer(session)
        self.info("[%08X]start network fail"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.fail)
        session.finish()
        
    def onStartTimeout(self, msg, session):
        self.info("[%08X]start network timeout"%
                  (session.session_id))
        self.case_manager.finishTestCase(TestResultEnum.timeout)
        session.finish()
